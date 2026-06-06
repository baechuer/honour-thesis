# Provider API Baselines

Last checked: 2026-06-05.

This note records optional paid or quota-limited neural baselines for the skill retrieval benchmark. These are not replacements for the local selectors. They are stronger external baselines for testing whether the benchmark still exposes semantic confusion when the selector uses modern embeddings or a neural reranker.

## Why Add Provider Baselines

The current local benchmark already has:

- M0 progressive disclosure: the main agent sees skill cards and decides which full docs to load.
- M1 flat lexical selectors: BM25 and TF-IDF over name, description, and tags.
- M2 local embedding selectors: MiniLM over descriptions or full skill documents.
- M3 structured selectors: schema text over procedural fields.
- M6 local two-stage selectors: first-stage retrieval followed by deterministic schema reranking.

Provider baselines add two stronger families:

- M7 API embedding retrieval: modern provider embedding model over `R1`, `R2`, or full `SKILL.md`.
- M8 API embedding plus neural reranking: retrieve candidates with an embedding model, then rerank the top candidates with a cross-encoder-style reranker.

This matches the current literature direction better than a single embedding baseline. SkillRouter, ToolRerank, and recent retrieval systems generally treat selection as a two-stage problem: cheaply retrieve a candidate set, then rerank with a more expensive relevance model.

## API Keys

Never hard-code keys into scripts or notes. Use the local `.env` file.

1. Copy `.env.example` to `.env`.
2. Fill only the provider keys you want to test.
3. Run `source .env` before API experiments, or rely on `run_provider_selectors.py` reading `.env` by default.

Relevant variables:

- `OPENAI_API_KEY`
- `DEEPSEEK_API_KEY`
- `DEEPSEEK_BASE_URL`
- `DEEPSEEK_MODEL`
- `DASHSCOPE_API_KEY`
- `COHERE_API_KEY`
- `VOYAGE_API_KEY`
- `JINA_API_KEY`
- `HF_TOKEN`

The repo ignores `.env` and `.env.*`, while keeping `.env.example`.

## Implemented Runner

The implemented script is:

```bash
python3 skill_benchmark/scripts/run_provider_selectors.py \
  --embedding-provider qwen \
  --embedding-model text-embedding-v4 \
  --embedding-representation full \
  --reranker-provider qwen \
  --reranker-model qwen3-rerank \
  --scale current_full
```

For OpenAI embedding-only:

```bash
python3 skill_benchmark/scripts/run_provider_selectors.py \
  --embedding-provider openai \
  --embedding-model text-embedding-3-small \
  --embedding-representation full \
  --reranker-provider none \
  --scale current_full
```

The runner caches API responses in `skill_benchmark/runtime/provider_cache/`, so repeated runs should not repeatedly bill for the same uncached inputs.

## Provider Comparison

| Provider | What To Use | Local Or API | Current Pricing Signal | Notes |
|---|---|---|---|---|
| DeepSeek | `deepseek-v4-flash` for model-assisted field verification; `deepseek-v4-pro` only if needed | API | Official docs list OpenAI-format base URL `https://api.deepseek.com`; V4 Flash is the cheap default and supports JSON output. | Recommended for Step 6 public-skill semantic extraction because it is cheap and the task mostly needs evidence-grounded JSON extraction, not the strongest possible reasoning model. |
| OpenAI | `text-embedding-3-small`, `text-embedding-3-large` | API | Official pricing page lists `text-embedding-3-small` at `$0.02 / 1M tokens` and `text-embedding-3-large` at `$0.13 / 1M tokens`. | Strong embedding baseline; no first-party dedicated reranker API exposed in the same way as Qwen/Cohere/Voyage/Jina. |
| Qwen Cloud / DashScope | `text-embedding-v4`, `qwen3-rerank` | API | Qwen docs list `text-embedding-v4` at `$0.07 / 1M input tokens`; `qwen3-rerank` at `$0.10 / 1M input tokens`; new users get temporary free quota, and the reranking FAQ states 1M free rerank tokens for 90 days after activation. | Best first API target because it supports both embedding retrieval and a dedicated reranker. |
| SkillRouter | `pipizhao/SkillRouter-Embedding-0.6B`, `pipizhao/SkillRouter-Reranker-0.6B` | Local first; Hugging Face endpoint only if needed | Model weights are public on Hugging Face under Apache-2.0; local use is free except hardware cost. The embedding model has Hugging Face inference support, but the reranker model is not currently deployed by a Hugging Face Inference Provider, so hosted reranking requires a dedicated endpoint or another GPU host. | Most thesis-relevant because it is specifically about skill/tool routing. Run a local smoke test before paying for hosting. Treat it as a domain-specific retrieve-and-rerank baseline, not as an ablation of the proposed field taxonomy. |
| Cohere | Embed and Rerank families | API | Official docs say trial keys are free but limited; production keys are charged. Public pricing currently emphasizes plan/private-deployment pricing, with Model Vault examples such as Embed 4 and Rerank instances from `$4-$5/hour` or `$2,500-$3,250/month`. | Strong reranking provider, but less convenient as the first pay-as-you-go benchmark unless exact account pricing is visible in your dashboard. |
| Voyage AI | `voyage-4`, `voyage-4-lite`, `voyage-4-large`, `rerank-2.5`, `rerank-2.5-lite` | API | Official docs list embeddings at `$0.02-$0.12 / 1M tokens` for current Voyage 4 models, with 200M free tokens for many models. Rerankers are `$0.02-$0.05 / 1M processed tokens`, also with 200M free tokens. | Very attractive price/free-token option. Worth adding after Qwen if you want another strong neural reranker provider. |
| Jina AI | `jina-embeddings-v4`, `jina-reranker-v3` or hosted reranker API | API or local model weights for some models | Jina's official reranker page says new API keys begin with 10M free tokens; paid usage is token-package based. | Good alternative with dedicated reranking and generous trial tokens. Useful as a robustness check rather than the first implementation target. |

Useful source links:

- DeepSeek API models/pricing: <https://api-docs.deepseek.com/quick_start/pricing>
- DeepSeek chat completion API: <https://api-docs.deepseek.com/api/create-chat-completion>
- OpenAI model pricing: <https://developers.openai.com/api/docs/models/text-embedding-3-small> and <https://developers.openai.com/api/docs/models/text-embedding-3-large>
- Qwen pricing: <https://docs.qwencloud.com/developer-guides/getting-started/pricing>
- Qwen embeddings endpoint and model limits: <https://docs.qwencloud.com/developer-guides/embeddings/text-embedding>
- Qwen embedding/reranking FAQ: <https://docs.qwencloud.com/resources/faq-embedding-reranking>
- SkillRouter embedding model: <https://huggingface.co/pipizhao/SkillRouter-Embedding-0.6B>
- SkillRouter reranker model: <https://huggingface.co/pipizhao/SkillRouter-Reranker-0.6B>
- Cohere pricing behavior and trial/production keys: <https://docs.cohere.com/docs/how-does-cohere-pricing-work> and <https://cohere.com/pricing>
- Voyage pricing: <https://docs.voyageai.com/docs/pricing>
- Jina reranker pricing/free-token note: <https://jina.ai/en-US/reranker/>

## Recommended Experimental Order

1. Run Qwen `text-embedding-v4` on full `SKILL.md` with no reranker.
2. Run Qwen `text-embedding-v4` plus `qwen3-rerank` over top-20 candidates.
3. If budget allows, run OpenAI `text-embedding-3-small` and `text-embedding-3-large` as embedding-only baselines.
4. If the benchmark becomes too easy under Qwen reranking, refine the confusable clusters before adding more providers.
5. Run a local SkillRouter smoke test on a tiny subset: `SR-Emb-0.6B` retrieves top-20, then `SR-Rank-0.6B` reranks those candidates.
6. If the local smoke test is too slow or memory-limited, deploy a paid Hugging Face Inference Endpoint or another GPU-hosted endpoint. Do not start with hosting before the local smoke test.

2026-06-05 local smoke-test note: `HF_TOKEN` access and model-card downloads worked, and `skill_benchmark/scripts/run_skillrouter_selectors.py` was added. However, both MPS/auto and CPU tiny-corpus attempts stalled during local model loading/inference on the 8 GB laptop. Treat local full-scale SkillRouter as impractical for now unless quantization is added or a stronger machine is used.

2026-06-05 hosted run note: a private 5.6 MB benchmark snapshot was uploaded to the Hugging Face dataset repo `baechuer1/honour-thesis-skillrouter-benchmark-snapshot`. The initial `zero-a10g` attempt failed because that hardware was not publicly available, but `t4-small` Hugging Face Jobs succeeded. The full four-condition run used `pipizhao/SkillRouter-Embedding-0.6B` over full skill artifacts and, where enabled, `pipizhao/SkillRouter-Reranker-0.6B` over top-20 candidates. Artifact upload from the remote job failed once because the job token lacked write permission, so the final repeat run printed compact summaries without uploading artifacts.

Hosted SkillRouter results on the 2401-skill benchmark:

| Prompt set | Method | Top-1 | Accept top-1 | Top-5 | Accept top-5 | MRR | Non-main top-1 | Wall time |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Controlled, 137 prompts | SkillRouter full embedding | 73.0% | 75.9% | 94.2% | 94.9% | 0.827 | 14.6% | 48.7s |
| Controlled, 137 prompts | SkillRouter full embedding + SkillRouter rerank top-20 | 83.2% | 83.2% | 97.8% | 98.5% | 0.898 | 4.4% | 116.5s |
| Public-gold, 32 prompts | SkillRouter full embedding | 65.6% | 75.0% | 96.9% | 96.9% | 0.770 | 84.4% | 9.5s |
| Public-gold, 32 prompts | SkillRouter full embedding + SkillRouter rerank top-20 | 65.6% | 68.8% | 93.8% | 96.9% | 0.788 | 87.5% | 34.1s |

Interpretation: SkillRouter is now the strongest controlled retrieve-and-rerank baseline run so far, outperforming generic Qwen full-skill embedding and Qwen reranking on the controlled set. On the public-gold stratum, SkillRouter embedding is already strong; reranking improves MRR slightly but does not improve strict top-1. This means the thesis should compare proposed field-aware methods against SkillRouter as a serious domain-specific baseline, not only against generic embedding models.

## Cost Control

- Start with `--max-prompts 5` to verify the setup.
- Keep `--rerank-candidates 20` unless you are explicitly testing top-k rerank sensitivity.
- Use cached runs for iteration.
- Do not run all providers on all representations until the Qwen smoke test works.

Example smoke test:

```bash
python3 skill_benchmark/scripts/run_provider_selectors.py \
  --embedding-provider qwen \
  --embedding-model text-embedding-v4 \
  --embedding-representation full \
  --reranker-provider qwen \
  --reranker-model qwen3-rerank \
  --scale core \
  --max-prompts 5
```

SkillRouter local smoke-test target:

```bash
python3 skill_benchmark/scripts/run_skillrouter_selectors.py \
  --embedding-model pipizhao/SkillRouter-Embedding-0.6B \
  --reranker-model pipizhao/SkillRouter-Reranker-0.6B \
  --embedding-representation full \
  --scale current_full \
  --rerank-candidates 20 \
  --max-prompts 5
```

This script is implemented. It caches skill embeddings and reranker scores locally and reports the same headline metrics as the Qwen provider runner. On the current laptop, use it only for tiny smoke tests unless a quantized or remote execution path is available.

## How This Fits The Thesis Framing

These provider baselines should be reported as implementation choices inside broader method families:

- Progressive disclosure: main agent decides from visible skill cards.
- Flat retrieval: compressed metadata only.
- Full-document embedding retrieval: vector search over whole skill artifacts.
- Structured/procedural representation: explicit input, output, workflow, dependency, and resource fields.
- Two-stage retrieval plus reranking: candidate subsetting followed by a more expensive relevance model.

The thesis question should remain about what information is preserved and how selection behaves under semantic confusion at scale, not about declaring one commercial API as universally best.
