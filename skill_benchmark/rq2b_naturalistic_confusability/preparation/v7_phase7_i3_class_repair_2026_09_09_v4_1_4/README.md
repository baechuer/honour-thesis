# V7 Phase-7 I3 V4.1.4 source-only class repair

This prospective repair replays all 3,798 V4.1.3 sources. It expands clearly truncated markdown list evidence, reclassifies evidence by strong enclosing headings and polarity, and supplements bounded source-exact blocks under operational headings. The failed fresh QA v4 is bound and preserved; it is not rewritten or treated as passing.

The transformation does not read queries, labels, acceptable sets, retrieval results, or metrics, and performs no provider, retrieval, or reranking calls. I3C and I3-flat are serialized from the same retained evidence sequence. A new blinded 120-row QA is required.

Create: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_class_repair_v4_1_4.py`.

Exact replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_class_repair_v4_1_4.py --verify`.
