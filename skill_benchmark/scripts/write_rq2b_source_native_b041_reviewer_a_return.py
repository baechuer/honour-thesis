#!/usr/bin/env python3
"""Write the isolated B041 Reviewer A full-source classifications."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
PACKET_DIR = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_creative_design_media_lexical_continuation_b041_2026-09-04/batch_041_full_source_review_packets"
PACKET = PACKET_DIR / "reviewer_a_packet.jsonl"
OUTPUT = PACKET_DIR / "reviewer_a_return.jsonl"
ALLOWED = {
    "PASS_TO_PROMPT_AUTHORING", "REJECT_TOPIC_ONLY", "REJECT_COMPONENT_OR_COMPOSITION",
    "REJECT_GENERIC_SPECIALIST", "REJECT_NEAR_DUPLICATE_OR_FORK", "REJECT_NO_BOUNDED_ENVELOPE",
    "REJECT_NO_MEMBER_LEVEL_PROMPTABILITY", "DEFER_PROVENANCE_OR_LICENSE", "DEFER_INSUFFICIENT_SOURCE_EVIDENCE",
}

# Each entry is keyed only by the blinded family token in Reviewer A's packet.
# Evidence is literal language from the complete original skills in that packet.
REVIEWS = {
    "F-22c5367ab9cc781c": ("PASS_TO_PROMPT_AUTHORING",
        ["S-1: 'Generate Slidev presentations from slide outlines.'", "S-2: 'Generate AI image presentations from slide outlines.'", "S-3: 'generating a two-layer presentation from a slide outline.'"],
        {"S-1": ["Produces a 'Slidev presentation project' with markdown/CSS layouts."], "S-2": ["Renders 'Each slide ... as an image via configurable APIs.'"], "S-3": ["Separates 'AI background images (text-free)' from a 'Slidev project with HTML/CSS text overlay.'"]},
        "The complete originals support one concrete outline-to-presentation objective and three first-route production approaches: Slidev project, rendered-image deck, and two-layer image-plus-overlay deck. Those output and method constraints create plausible alternatives without making any member a prerequisite of another."),
    "F-1c9e1bbeddcf44c7": ("REJECT_GENERIC_SPECIALIST",
        ["S-1: 'build a LinkedIn authority system'; S-2: 'Build a personal brand strategy'; S-3: 'build personal brand ... as a founder on Twitter/X or LinkedIn.'"],
        {"S-1": ["Limits the work to LinkedIn content strategy and posts."], "S-2": ["Supplies the broad personal-brand strategy."], "S-3": ["Restricts the broad activity to founder thought leadership and named channels."]},
        "The originals place a general personal-brand strategy beside LinkedIn-only and founder/channel-specific versions. They do not establish three parallel first routes with member-level operational contrast."),
    "F-6f43ba24f0358e9c": ("REJECT_COMPONENT_OR_COMPOSITION",
        ["S-1: 'PRD/ARD into SPEC.md'; S-2: 'Break a PRD/ARD/SPEC into an implementation plan'; S-3: 'Turn a PRD into an ARD.'"],
        {"S-1": ["Explicitly operates after design and before planning."], "S-2": ["Explicitly operates after design/spec and before build."], "S-3": ["Produces the architecture design artifact before spec."]},
        "The full-source workflow states make the three artifacts sequential design, specification, and planning steps rather than independent alternatives."),
    "F-5a28d796365c10ac": ("PASS_TO_PROMPT_AUTHORING",
        ["S-1: 'Edit and compose video with Python using MoviePy.'", "S-2: 'Transcode, convert, edit, and process audio and video with FFmpeg.'", "S-3: 'Process media files ... using Transloadit.'"],
        {"S-1": ["Uses Python composition, effects, and rendering."], "S-2": ["Uses FFmpeg conversion, filters, codecs, and command-line processing."], "S-3": ["Uses Transloadit's processing robots for hosted file transformations at scale."]},
        "All three independently transform supplied media into edited or converted outputs. Their Python library, native media-tool, and hosted processing-pipeline methods provide source-supported operational contrast for natural requests."),
    "F-74f19b2465822609": ("REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-1: 'create a presentation'; S-2: 'Generate full HTML presentations'; S-3: 'Generate complete presentations with AI.'"],
        {"S-1": ["Plans and authors presentation JSON."], "S-2": ["Adds framework selection and brand context to the same deck-generation task."], "S-3": ["Adds narrative and slide-design guidance to the same deck-generation task."]},
        "The originals repeatedly claim the same general presentation-generation route; framework and workflow detail does not supply member-level task separation."),
    "F-591d63eab46d11cb": ("REJECT_COMPONENT_OR_COMPOSITION",
        ["S-1: 'memory strategies for ... audio engines'; S-2: 'Real-time audio threading'; S-3: 'thread-safe, allocation-free audio-GUI communication.'"],
        {"S-1": ["Covers pre-allocation and pools."], "S-2": ["Covers thread roles, FIFOs, and locks."], "S-3": ["Covers atomics and ring buffers for the same audio runtime."]},
        "These are complementary engineering mechanisms inside one real-time-audio implementation, not separate first routes for a bounded user task."),
    "F-a312ec97749ec5e8": ("REJECT_NO_BOUNDED_ENVELOPE",
        ["S-1: 'long-form YouTube scripts'; S-2: 'opening lines for a written social post'; S-3: 'first 3 seconds of a short-form video.'"],
        {"S-1": ["Explicitly excludes short-form openers."], "S-2": ["Explicitly excludes spoken/on-screen short-video openers."], "S-3": ["Explicitly excludes written-post first lines and long-form introductions."]},
        "The originals expressly partition long-form scripts, written-post hooks, and short-video hooks; a single concrete shared input/output envelope is absent."),
    "F-09b3554c72af80ec": ("REJECT_GENERIC_SPECIALIST",
        ["S-1: 'Tailwind CSS design system'; S-2: 'design system inside an Expo app'; S-3: '@accelint/design-foundation or @accelint/design-toolkit packages.'"],
        {"S-1": ["Is bound to Tailwind and class-variance-authority."], "S-2": ["Is bound to Expo and native styling libraries."], "S-3": ["Is bound to named Accelint packages and their token conventions."]},
        "The shared label is a broad design-system topic, while each full source is ecosystem-bound. The packet lacks three generally interchangeable first-route skills."),
    "F-a022ddb5a6381e0e": ("REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-1: 'modern minimal style with elegant serif typography'; S-2: 'editorial style with serif typography'; S-3: 'editorial layout with refined serif typography.'"],
        {"S-1": ["Offers a refined minimal palette."], "S-2": ["Offers a closely overlapping polished editorial style."], "S-3": ["Offers the same serif/editorial direction with structured grids."]},
        "The full originals offer adjacent stylistic variants but no source-supported operational boundary that would make them distinct task routes."),
    "F-bdbe7e57aacdf730": ("REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-1: 'Extract text and structured data from images using Vision AI (OCR).'; S-3: 'Extract text from complex documents using Chandra OCR.'"],
        {"S-1": ["Reads screenshots, scanned documents, and tables/forms/charts."], "S-2": ["Its complete original presents an OCR/document-extraction capability set."], "S-3": ["Reads scanned documents, tables, forms, handwriting, and layouts."]},
        "The originals converge on document/image OCR extraction. Added provider or layout detail does not establish three independent first-route objectives."),
    "F-3351df1422ba16d5": ("REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-1: 'Design, iterate, test, and version prompts for LLMs'; S-2: 'Writes, refactors, and evaluates prompts for LLMs'; S-3: 'optimize a prompt' and 'design a prompt template.'"],
        {"S-1": ["Covers system prompts, examples, and structured output."], "S-2": ["Covers templates, schemas, rubrics, and test suites."], "S-3": ["Covers the same few-shot, chain-of-thought, structured-output, and optimization patterns."]},
        "Procedural coverage overlaps strongly across all three prompt-engineering originals; no distinct first-route boundary is supported."),
    "F-3c160e4117ef7e06": ("REJECT_COMPONENT_OR_COMPOSITION",
        ["S-1: 'Frame a new design proposal'; S-2: 'write an implementation spec ... from an accepted proposal'; S-3: 'Records an architecture decision ... already made.'"],
        {"S-1": ["Explicitly excludes recording an accepted decision and writing an implementation spec."], "S-2": ["Explicitly begins once the proposal is accepted."], "S-3": ["Explicitly records rather than makes the decision."]},
        "The originals state mutually sequenced lifecycle positions, so the sources are composition steps rather than alternatives."),
    "F-dfb8cbd920829bae": ("REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-1: 'Create professional investor pitch decks'; S-2: 'create investor pitch decks'; S-3: 'High-stakes startup pitch decks.'"],
        {"S-1": ["Covers company-information gathering, narrative, PowerPoint generation, and visuals."], "S-2": ["Outputs slide content, talking points, and optional visuals."], "S-3": ["Changes tone to founder voice and one-claim-per-slide while retaining the same pitch-deck task."]},
        "All three originals route an investor/startup pitch-deck request to the same core output; stylistic and deliverable-detail changes are not independent routes."),
    "F-08e94c5223bedf56": ("REJECT_GENERIC_SPECIALIST",
        ["S-1: 'video ads ... ready to run on Meta, TikTok, or YouTube'; S-2: 'native TikTok video ads'; S-3: 'Make YouTube Shorts.'"],
        {"S-1": ["Covers the cross-platform advertisement."], "S-2": ["Is a vertical TikTok-specific specialization and says to use S-1 for landscape/long-form ads."], "S-3": ["Is a YouTube-Shorts-specific specialization."]},
        "A broad video-ad skill sits beside platform-specialized variants; this is the generic-specialist configuration excluded by the rubric."),
    "F-405432fad4f3983d": ("REJECT_COMPONENT_OR_COMPOSITION",
        ["S-1: 'core game loops ... and game design theory'; S-2: 'Analyzes a game system'; S-3: 'designing game levels ... and spatial layouts.'"],
        {"S-1": ["Frames game-wide design foundations."], "S-2": ["Evaluates an existing system and is used after an MVP plan."], "S-3": ["Designs an individual level/environment layer."]},
        "The sources cover broad design, evaluation, and level design at different lifecycle and abstraction levels, not three first-route alternatives."),
    "F-33c007e11967549f": ("REJECT_GENERIC_SPECIALIST",
        ["S-1: 'Python image processing for microscopy and bioimage analysis'; S-2: 'DL cell/nucleus segmentation'; S-3: 'Cell segmentation in fluorescence microscopy images.'"],
        {"S-1": ["Covers filtering, segmentation, measurement, and detection broadly."], "S-2": ["Specializes to Cellpose DL segmentation."], "S-3": ["Wraps cell segmentation and emits masks, morphology metrics, overlays, and a report."]},
        "The broad bioimage-processing source encompasses more than the two segmentation-specific sources; the packet is generic-plus-specialist rather than parallel routes."),
    "F-fb4b30ded4e8e55e": ("REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-1: 'source-grounded research presentations from papers'; S-2: 'Nature-style Chinese PPTX presentation from a scientific paper'; S-3: 'Nature-style Chinese PPTX presentation from a scientific paper.'"],
        {"S-1": ["Builds paper-to-slides research presentations."], "S-2": ["Creates the PPTX, selects figures, writes notes, and runs QA."], "S-3": ["Creates the same research-paper PPTX with figures, notes, and verification."]},
        "The full-source output contracts overlap on paper-to-PPTX creation; the two Nature-style originals are especially duplicative."),
    "F-b448be44de8a47ca": ("REJECT_COMPONENT_OR_COMPOSITION",
        ["S-1: 'Convert ... files to GitHub-Flavored Markdown'; S-2: 'Convert an attached ... file into local Markdown'; S-3: 'Add local office-document-to-Markdown conversion ... to ... agent containers.'"],
        {"S-1": ["Performs conversion for an active task."], "S-2": ["Performs local attached-file conversion."], "S-3": ["Installs/configures the conversion capability in containers."]},
        "The third original is deployment/setup for the same conversion capability, while the first two overlap as direct conversion routes; this is a component/composition grouping."),
    "F-09966bf48a773317": ("REJECT_COMPONENT_OR_COMPOSITION",
        ["S-1: 'planning a product launch end-to-end'; S-2: 'sales motion ... coherent kit'; S-3: 'turning a positioning statement into actual copy.'"],
        {"S-1": ["Explicitly says to use the messaging source for core message and sales-enablement source for the sales deck/kit."], "S-2": ["Explicitly says to use launch-plan-sequencer for rollout calendar and messaging-hierarchy for value ladder."], "S-3": ["Explicitly says to use launch-plan-sequencer for launch phases."]},
        "The originals explicitly assign complementary launch, enablement, and messaging artifacts to one another, demonstrating composition rather than alternatives."),
    "F-1dd1c181052eab15": ("REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-1: 'structured brainstorming session'; S-2: 'Structured brainstorming and ideation facilitation'; S-3: 'Structured multi-frame ideation.'"],
        {"S-1": ["Diverges then clusters and shortlists."], "S-2": ["Applies standard ideation techniques."], "S-3": ["Generates and scores ideas across creative GTM frames."]},
        "All three are facilitated ideation routes with overlapping divergence/convergence outputs; framing variants do not provide independent task boundaries."),
    "F-83b974b638fcb01d": ("REJECT_GENERIC_SPECIALIST",
        ["S-1: 'finished short-form video ad'; S-2: '60-90 second explainer video'; S-3: 'video production pipeline' with promo, showcase, or tutorial modes."],
        {"S-1": ["Is the advertising specialization."], "S-2": ["Is the explainer specialization."], "S-3": ["Is the broad orchestrator spanning promo, showcase, and tutorial outputs."]},
        "The broad multi-mode director contains the specialist ad/explainer territory instead of standing as a separate first-route alternative."),
    "F-2896e4599ee3baca": ("REJECT_COMPONENT_OR_COMPOSITION",
        ["S-1: 'Gameplay Tags'; S-2: 'Gameplay Abilities'; S-3: 'Animation Montages.'"],
        {"S-1": ["Defines taxonomies, queries, and GAS gating."], "S-2": ["Defines ability lifecycle, activation, costs, prediction, and tasks."], "S-3": ["Defines animation action/timing and GAS montage integration."]},
        "The sources are distinct Unreal subsystems that combine in gameplay implementation; their shared engine topic does not form a common first-route task."),
    "F-007084d4badd9771": ("REJECT_GENERIC_SPECIALIST",
        ["S-1: 'create or optimize an email sequence ... lifecycle email program'; S-2: 'any multi-email automated flow'; S-3: 'email drip sequence for affiliate marketing.'"],
        {"S-1": ["Covers the general lifecycle/email-sequence route."], "S-2": ["Covers the same general automated-flow route."], "S-3": ["Restricts the same sequence output to affiliate marketing."]},
        "Two overlapping general email-sequence sources sit beside an affiliate-specific specialization, not three contrastive first-route skills."),
    "F-53261316777c60f5": ("REJECT_GENERIC_SPECIALIST",
        ["S-1: 'hand-drawn whiteboard infographic prompt'; S-2: 'Create LinkedIn post graphics'; S-3: 'Generate branded infographic specifications from any content or data.'"],
        {"S-1": ["Outputs a Gemini prompt for one whiteboard-infographic style."], "S-2": ["Chooses HTML/CSS or generated-infographic treatment for a LinkedIn post."], "S-3": ["Supplies the broad content/data infographic specification." ]},
        "The broad infographic specification sits beside post- and whiteboard-specific variants; the originals do not support three independent first routes."),
    "F-eb58f2d7c647b1d4": ("REJECT_COMPONENT_OR_COMPOSITION",
        ["S-1: 'Deepfake detection and media safety'; S-2: 'Verify sources, claims, images, video, documents ... with SIFT'; S-3: 'structured verification of sources, claims, images, video, and documents ... using the SIFT framework.'"],
        {"S-1": ["Concentrates on AI-generated-media detection and speaker/source tracing."], "S-2": ["Provides general SIFT evidence verification."], "S-3": ["Provides the same general SIFT verification plus media checks."]},
        "The deepfake tool is a media-verification component while S-2 and S-3 overlap as general verification procedures; this is not a three-route family."),
}


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite reviewer return: {OUTPUT}")
    rows = [json.loads(line) for line in PACKET.read_text(encoding="utf-8").splitlines() if line]
    tokens = [row["family_token"] for row in rows]
    if len(rows) != 25 or set(tokens) != set(REVIEWS) or len(set(tokens)) != 25:
        raise SystemExit("Reviewer A packet/return token set mismatch")
    output = []
    for row in rows:
        decision, envelope, contrasts, rationale = REVIEWS[row["family_token"]]
        if decision not in ALLOWED or set(contrasts) != {member["member_token"] for member in row["members"]}:
            raise SystemExit(f"schema decision/member mismatch: {row['family_token']}")
        output.append({
            "record_type": "source_native_full_source_family_review_return",
            "family_token": row["family_token"],
            "decision": decision,
            "common_envelope_evidence": envelope,
            "member_contrast_evidence": contrasts,
            "rationale": rationale,
        })
    OUTPUT.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in output), encoding="utf-8")
    print(json.dumps({"records": len(output), "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
