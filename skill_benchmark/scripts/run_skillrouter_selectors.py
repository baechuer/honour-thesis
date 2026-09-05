#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any

import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_offline_selectors import (  # noqa: E402
    approximate_tokens,
    build_scale_skill_names,
    evaluate_rows,
    instruction_text,
    load_acceptables,
    load_full_skill_texts,
    load_jsonl,
    load_prompts,
)


QUERY_INSTRUCTION = (
    "Instruct: Given a task description, retrieve the most relevant "
    "skill document that would help an agent complete the task\nQuery:"
)


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def slug(value: str) -> str:
    return "".join(char if char.isalnum() or char in "-._" else "_" for char in value).strip("_")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def select_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def model_dtype(device: str) -> torch.dtype:
    if device == "cuda":
        return torch.bfloat16
    return torch.float32


def last_token_pool(last_hidden_states: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    left_padding = bool(attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    seq_lens = attention_mask.sum(dim=1) - 1
    batch = last_hidden_states.shape[0]
    return last_hidden_states[torch.arange(batch, device=last_hidden_states.device), seq_lens]


def docs_for_representation(
    representation: str,
    skill_names: list[str],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    full_skill_texts: dict[str, str],
) -> list[str]:
    if representation == "r1":
        return [r1[name]["text"] for name in skill_names]
    if representation == "r2":
        return [r2[name]["text"] for name in skill_names]
    if representation == "full":
        return [f"{name} | {r1[name].get('description', '')} | {full_skill_texts.get(name) or r2[name]['text']}" for name in skill_names]
    raise ValueError(f"Unknown representation: {representation}")


def rank_with_scores(skill_names: list[str], scores: list[float]) -> list[tuple[str, float]]:
    return sorted(zip(skill_names, scores), key=lambda item: (-item[1], item[0]))


def prompt_skill_subset(prompts: list[dict[str, Any]], available: set[str]) -> list[str]:
    names: set[str] = set()
    for prompt in prompts:
        if prompt.get("gold_skill") in available:
            names.add(prompt["gold_skill"])
        for name in prompt.get("closest_alternatives", []):
            if name in available:
                names.add(name)
    return sorted(names)


class SkillRouterEmbedder:
    def __init__(
        self,
        model_id: str,
        cache_dir: Path,
        device: str,
        max_length: int,
        token: str | None,
        quiet: bool = False,
    ) -> None:
        self.model_id = model_id
        self.cache_dir = cache_dir / "skillrouter" / "embeddings" / slug(model_id)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.device = device
        self.max_length = max_length
        self.quiet = quiet
        self.cache_hits = 0
        self.encoded_items = 0
        print(f"Loading SkillRouter embedder {model_id} on {device}...", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            trust_remote_code=True,
            padding_side="left",
            token=token,
        )
        self.model = AutoModel.from_pretrained(
            model_id,
            trust_remote_code=True,
            torch_dtype=model_dtype(device),
            token=token,
        ).eval()
        self.model.to(device)
        print("Loaded SkillRouter embedder.", flush=True)

    def cache_path(self, text: str) -> Path:
        return self.cache_dir / f"{sha256_text(text)}.pt"

    def encode(self, texts: list[str], batch_size: int) -> torch.Tensor:
        vectors: list[torch.Tensor | None] = [None for _ in texts]
        missing: list[tuple[int, str, Path]] = []
        for index, text in enumerate(texts):
            path = self.cache_path(text)
            if path.exists():
                vectors[index] = torch.load(path, map_location="cpu")
                self.cache_hits += 1
            else:
                missing.append((index, text, path))

        for start in range(0, len(missing), batch_size):
            batch = missing[start : start + batch_size]
            batch_number = start // max(batch_size, 1) + 1
            should_log = start == 0 or batch_number % 100 == 0 or start + len(batch) >= len(missing)
            if not self.quiet and should_log:
                print(f"Encoding embeddings {start + 1}-{start + len(batch)} of {len(missing)} uncached items...", flush=True)
            encoded = self.tokenizer(
                [text for _, text, _ in batch],
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt",
            )
            encoded = {key: value.to(self.device) for key, value in encoded.items()}
            with torch.no_grad():
                outputs = self.model(**encoded)
                embs = last_token_pool(outputs.last_hidden_state, encoded["attention_mask"])
                embs = F.normalize(embs, p=2, dim=1).detach().cpu()
            for row_index, (index, _text, path) in enumerate(batch):
                vector = embs[row_index]
                vectors[index] = vector
                torch.save(vector, path)
                self.encoded_items += 1

        return torch.stack([vector for vector in vectors if vector is not None])


class SkillRouterReranker:
    def __init__(
        self,
        model_id: str,
        cache_dir: Path,
        device: str,
        max_length: int,
        token: str | None,
        quiet: bool = False,
    ) -> None:
        self.model_id = model_id
        self.cache_dir = cache_dir / "skillrouter" / "rerank" / slug(model_id)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.device = device
        self.max_length = max_length
        self.quiet = quiet
        self.cache_hits = 0
        self.scored_items = 0
        print(f"Loading SkillRouter reranker {model_id} on {device}...", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            padding_side="left",
            token=token,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=model_dtype(device),
            token=token,
        ).eval()
        self.model.to(device)
        self.token_yes = self.tokenizer.convert_tokens_to_ids("yes")
        self.token_no = self.tokenizer.convert_tokens_to_ids("no")
        print("Loaded SkillRouter reranker.", flush=True)

    def cache_path(self, query: str, doc: str) -> Path:
        payload = query + "\n---\n" + doc
        return self.cache_dir / f"{sha256_text(payload)}.json"

    def build_input_ids(self, prompt: str) -> list[int]:
        prefix = (
            "<|im_start|>system\nJudge whether the Document meets the requirements "
            'based on the Query and the Instruct provided. Note that the answer can '
            'only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
        )
        suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
        prefix_tokens = self.tokenizer.encode(prefix, add_special_tokens=False)
        suffix_tokens = self.tokenizer.encode(suffix, add_special_tokens=False)
        budget = max(32, self.max_length - len(prefix_tokens) - len(suffix_tokens))
        tokens = self.tokenizer(
            prompt,
            padding=False,
            truncation=True,
            max_length=budget,
            return_attention_mask=False,
        )["input_ids"]
        return prefix_tokens + tokens + suffix_tokens

    def format_prompt(self, query: str, doc: str) -> str:
        instruction = (
            "Given a task description, judge whether the skill document "
            "is relevant and useful for completing the task"
        )
        return f"<Instruct>: {instruction}\n\n<Query>: {query}\n\n<Document>: {doc}"

    def score_many(self, query: str, docs: list[str]) -> list[float]:
        scores: list[float] = []
        for doc in docs:
            path = self.cache_path(query, doc)
            if path.exists():
                scores.append(float(json.loads(path.read_text(encoding="utf-8"))["score"]))
                self.cache_hits += 1
                continue
            if not self.quiet:
                print(f"Scoring rerank item {len(scores) + 1} of {len(docs)}...", flush=True)
            prompt = self.format_prompt(query, doc)
            input_ids = torch.tensor([self.build_input_ids(prompt)], device=self.device)
            attention_mask = torch.ones_like(input_ids)
            with torch.no_grad():
                logits = self.model(input_ids=input_ids, attention_mask=attention_mask).logits[:, -1, :]
            score = float((logits[0, self.token_yes] - logits[0, self.token_no]).detach().cpu())
            path.write_text(json.dumps({"score": score}), encoding="utf-8")
            scores.append(score)
            self.scored_items += 1
        return scores


def render_markdown(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    lines = [
        "# SkillRouter Selector Evaluation Report",
        "",
        "This report evaluates the released SkillRouter Hugging Face embedding/reranker models.",
        "",
        "## Configuration",
        "",
        f"- Embedding model: `{report['embedding_model']}`",
        f"- Reranker model: `{report['reranker_model'] or 'none'}`",
        f"- Embedding representation: `{report['embedding_representation']}`",
        f"- Scale: `{report['scale']}` ({metrics['scale_skill_count']} skills)",
        f"- Device: `{report['device']}`",
        f"- Rerank candidates: {report['rerank_candidates']}",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Top-1 accuracy | {metrics['top1_accuracy']:.1%} |",
        f"| Acceptable top-1 accuracy | {metrics['acceptable_top1_accuracy']:.1%} |",
        f"| Top-5 recall | {metrics['top5_recall']:.1%} |",
        f"| Acceptable top-5 recall | {metrics['acceptable_top5_recall']:.1%} |",
        f"| MRR | {metrics['mrr']:.3f} |",
        f"| Non-main top-1 | {metrics['non_main_top1_rate']:.1%} |",
        f"| Approx selector-visible tokens | {metrics['selector_visible_tokens_approx']} |",
        "",
        "## Local Runtime",
        "",
        f"- Embedding cache hits: {report['runtime']['embedding_cache_hits']}",
        f"- Embedding items encoded this run: {report['runtime']['embedding_items_encoded']}",
        f"- Rerank cache hits: {report['runtime']['rerank_cache_hits']}",
        f"- Rerank items scored this run: {report['runtime']['rerank_items_scored']}",
        f"- Elapsed ms: {report['elapsed_ms']}",
        "",
        "## Prompt-Level Results",
        "",
        "| Prompt | Gold | Rank | Top-1 | Status | Top-5 |",
        "|---|---|---:|---|---|---|",
    ]
    acceptable_by_prompt = report.get("acceptable_alternatives", {})
    for row in report["results"]:
        ranking = [item["skill"] for item in row["ranking"]]
        gold = row["gold_skill"]
        prompt_acceptables = acceptable_by_prompt.get(row["prompt_id"], {})
        acceptable = {gold, *prompt_acceptables.get("acceptable", [])}
        borderline = set(prompt_acceptables.get("borderline", []))
        rank = ranking.index(gold) + 1 if gold in ranking else "-"
        top1 = ranking[0] if ranking else "-"
        if top1 == gold:
            status = "gold"
        elif top1 in acceptable:
            status = "acceptable"
        elif top1 in borderline:
            status = "borderline"
        else:
            status = "wrong"
        lines.append(
            f"| `{row['prompt_id']}` | `{gold}` | {rank} | `{top1}` | {status} | {', '.join(ranking[:5])} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SkillRouter Hugging Face selector smoke tests.")
    parser.add_argument("--prompts", default="skill_benchmark/prompts/*.json")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--r2", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--skills-root", default="skill_benchmark/skills")
    parser.add_argument("--acceptable-alternatives", default="skill_benchmark/annotations/acceptable_alternatives.json")
    parser.add_argument("--scale", default="core", choices=["core", "current_full"])
    parser.add_argument(
        "--skill-subset-from-prompts",
        action="store_true",
        help="Smoke-test mode: evaluate only gold and closest-alternative skills for the selected prompts.",
    )
    parser.add_argument("--embedding-representation", default="full", choices=["r1", "r2", "full"])
    parser.add_argument("--embedding-model", default="pipizhao/SkillRouter-Embedding-0.6B")
    parser.add_argument("--reranker-model", default="pipizhao/SkillRouter-Reranker-0.6B")
    parser.add_argument("--no-reranker", action="store_true")
    parser.add_argument("--rerank-candidates", type=int, default=20)
    parser.add_argument("--embedding-batch-size", type=int, default=1)
    parser.add_argument("--embedding-max-length", type=int, default=2048)
    parser.add_argument("--reranker-max-length", type=int, default=2048)
    parser.add_argument("--cache-dir", default="skill_benchmark/runtime/provider_cache")
    parser.add_argument("--dotenv", default=".env")
    parser.add_argument("--max-prompts", type=int)
    parser.add_argument("--ranking-limit", type=int, default=20)
    parser.add_argument("--device", choices=["auto", "cpu", "mps", "cuda"], default="auto")
    parser.add_argument("--output-md", default="skill_benchmark/outputs/skillrouter_selector_smoke.md")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/skillrouter_selector_smoke.json")
    parser.add_argument("--quiet-progress", action="store_true")
    args = parser.parse_args()

    load_dotenv(Path(args.dotenv))
    token = os.environ.get("HF_TOKEN")
    device = select_device() if args.device == "auto" else args.device

    prompts = load_prompts(args.prompts)
    if args.max_prompts:
        prompts = prompts[: args.max_prompts]
    r1_rows = load_jsonl(Path(args.r1))
    r2_rows = load_jsonl(Path(args.r2))
    r1 = {row["name"]: row for row in r1_rows}
    r2 = {row["name"]: row for row in r2_rows}
    skill_names = build_scale_skill_names(args.scale, r1_rows)
    if args.skill_subset_from_prompts:
        subset = prompt_skill_subset(prompts, set(skill_names))
        if not subset:
            raise SystemExit("--skill-subset-from-prompts produced an empty skill set.")
        skill_names = subset
    full_skill_texts = load_full_skill_texts(Path(args.skills_root), sorted(r1))
    docs = docs_for_representation(args.embedding_representation, skill_names, r1, r2, full_skill_texts)
    acceptable_by_prompt = load_acceptables(Path(args.acceptable_alternatives) if args.acceptable_alternatives else None)
    cache_dir = Path(args.cache_dir)

    start = time.perf_counter()
    embedder = SkillRouterEmbedder(
        model_id=args.embedding_model,
        cache_dir=cache_dir,
        device=device,
        max_length=args.embedding_max_length,
        token=token,
        quiet=args.quiet_progress,
    )
    reranker = None
    if not args.no_reranker:
        reranker = SkillRouterReranker(
            model_id=args.reranker_model,
            cache_dir=cache_dir,
            device=device,
            max_length=args.reranker_max_length,
            token=token,
            quiet=args.quiet_progress,
        )

    doc_embeddings = embedder.encode(docs, args.embedding_batch_size)
    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        query_text = QUERY_INSTRUCTION + query
        query_embedding = embedder.encode([query_text], 1)[0]
        first_stage_scores = (query_embedding.unsqueeze(0) @ doc_embeddings.T).squeeze(0).tolist()
        first_stage = rank_with_scores(skill_names, [float(score) for score in first_stage_scores])
        gold_skill = prompt["gold_skill"]
        first_stage_ranking = [skill for skill, _score in first_stage]
        gold_first_stage_rank = (
            first_stage_ranking.index(gold_skill) + 1 if gold_skill in first_stage_ranking else None
        )

        if reranker is not None:
            candidate_count = min(args.rerank_candidates, len(first_stage))
            candidate_names = [name for name, _score in first_stage[:candidate_count]]
            candidate_docs = [docs[skill_names.index(name)] for name in candidate_names]
            rerank_scores = reranker.score_many(query, candidate_docs)
            ranked = rank_with_scores(candidate_names, rerank_scores)
        else:
            candidate_count = len(first_stage)
            ranked = first_stage

        final_ranking = [skill for skill, _score in ranked]
        gold_final_rank = final_ranking.index(gold_skill) + 1 if gold_skill in final_ranking else None
        rows.append(
            {
                "prompt_id": prompt["id"],
                "family": prompt["family"],
                "gold_skill": gold_skill,
                "closest_alternatives": prompt.get("closest_alternatives", []),
                "instruction_text": query,
                "gold_first_stage_rank": gold_first_stage_rank,
                "gold_final_rank": gold_final_rank,
                "first_stage_top1": first_stage[0][0] if first_stage else None,
                "candidate_count": candidate_count,
                "ranking": [
                    {"skill": skill, "score": round(float(score), 6)}
                    for skill, score in ranked[: args.ranking_limit]
                ],
            }
        )

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    selector_visible_tokens = sum(approximate_tokens(doc) for doc in docs)
    if reranker is not None:
        selector_visible_tokens += sum(approximate_tokens(row["instruction_text"]) * args.rerank_candidates for row in rows)
        selector_visible_tokens += sum(
            approximate_tokens(docs[skill_names.index(item["skill"])])
            for row in rows
            for item in row["ranking"][: min(args.rerank_candidates, len(row["ranking"]))]
            if item["skill"] in skill_names
        )
    metrics = evaluate_rows(rows, r1, len(skill_names), selector_visible_tokens, acceptable_by_prompt)
    report = {
        "embedding_model": args.embedding_model,
        "reranker_model": None if args.no_reranker else args.reranker_model,
        "embedding_representation": args.embedding_representation,
        "scale": args.scale,
        "device": device,
        "rerank_candidates": 0 if args.no_reranker else args.rerank_candidates,
        "elapsed_ms": elapsed_ms,
        "metrics": metrics,
        "runtime": {
            "embedding_cache_hits": embedder.cache_hits,
            "embedding_items_encoded": embedder.encoded_items,
            "rerank_cache_hits": reranker.cache_hits if reranker else 0,
            "rerank_items_scored": reranker.scored_items if reranker else 0,
        },
        "acceptable_alternatives": {
            prompt_id: {
                "acceptable": sorted(values.get("acceptable", set())),
                "borderline": sorted(values.get("borderline", set())),
            }
            for prompt_id, values in sorted(acceptable_by_prompt.items())
        },
        "results": rows,
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(
        f"SkillRouter + {'none' if args.no_reranker else 'reranker'}: "
        f"top1={metrics['top1_accuracy']:.1%}, top5={metrics['top5_recall']:.1%}, "
        f"mrr={metrics['mrr']:.3f}, non_main_top1={metrics['non_main_top1_rate']:.1%}"
    )


if __name__ == "__main__":
    main()
