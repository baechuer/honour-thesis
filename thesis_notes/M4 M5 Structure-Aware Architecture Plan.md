# M4/M5 Structure-Aware Architecture Plan

Date: 2026-06-01

Purpose: define how tree and graph methods should use the proposed skill information without drifting into vague "structure-aware" language.

## Core Distinction

The thesis separates:

- **Information fields:** what must be preserved about a skill, such as use condition, input/precondition, output, workflow, dependency, resource, boundary, and success criterion.
- **Architecture:** how a selector uses those fields, such as dense retrieval, reranking, tree routing, or graph retrieval.

M4 and M5 are architecture tests. They should not be used to smuggle in extra information. They should operate over the same extracted fields used by R2/R3/R4.

## Current R4 Edge Export

The current graph export is `skill_benchmark/representations/R4_graph_edges.jsonl`.

It already contains these edge types:

| Edge | Meaning | Retrieval Use |
|---|---|---|
| `belongs_to_family` | skill belongs to a domain/family | coarse routing or weak prior |
| `triggered_by` | use-when/routing condition | strong positive match |
| `avoid_when` | not-for/boundary condition | negative penalty, not positive text |
| `has_precondition` | required input state or assumption | positive only when request implies it |
| `has_workflow_step` | procedural step the skill performs | strong procedural discriminator |
| `produces_output` | expected output artifact or fields | strong procedural discriminator |
| `follows_writing_rule` | response/output style constraints | weak secondary signal |
| `requires_dependency` | tool/API/platform/runtime required | conditional feasibility signal |
| `has_resource_signal` | files, examples, references, linked resources | conditional context-loading signal |
| `uses_resource` | actual resource file under the skill | conditional context-loading signal |
| `derived_from_public_skill` | public-source provenance | audit/provenance only, not ranking evidence |

Current edge-count snapshot:

- `has_workflow_step`: 13764
- `has_resource_signal`: 12017
- `requires_dependency`: 10105
- `triggered_by`: 8503
- `has_precondition`: 5137
- `follows_writing_rule`: 4343
- `avoid_when`: 2771
- `produces_output`: 2771
- `belongs_to_family`: 2401
- `uses_resource`: 969
- `derived_from_public_skill`: 460

## M4: Tree Routing

M4 is a compressed hierarchy, not a full graph.

Proposed tree:

```text
root
  -> family
      -> optional cluster/subfamily
          -> skill
```

Tree edges:

| Edge | Meaning | Example |
|---|---|---|
| `root_to_family` | broad domain route | `root -> pdf_document_operations` |
| `family_to_cluster` | optional near-domain grouping | `pdf_document_operations -> extraction_ocr_conversion` |
| `cluster_to_skill` | candidate skill leaf | `extraction_ocr_conversion -> pdf-table-extractor` |
| `parent_to_atomic_skill` | optional public broad-skill decomposition | `figma -> figma-implement-design` |

Retrieval procedure:

1. Parse the request into a compact query representation.
2. Score families using family summaries or aggregated skill cards.
3. Route to top-1 family and top-n families.
4. Rank skills only inside the chosen branch or branches.
5. Report branch accuracy and final skill accuracy separately.

What M4 tests:

- Whether hierarchy reduces candidate set size and context cost.
- Whether early routing errors exclude the gold skill.
- Whether multi-branch routing reduces exclusion failures.

M4 does **not** mainly answer which procedural fields matter. It answers whether hierarchical routing is an efficient scalable architecture.

Required metrics:

- family top-1 accuracy
- family top-n recall
- final top-1/top-5/MRR
- gold-excluded-by-branch rate
- candidate reduction ratio
- latency/context cost

## M5: Graph-Based Skill Retrieval

M5 is a heterogeneous graph over skills and extracted information nodes.

Node types:

| Node Type | Source Field | Purpose |
|---|---|---|
| `skill` | skill name/id | candidate target |
| `family` | family/category | coarse domain prior |
| `trigger` | `use_when` | when to use the skill |
| `input_or_precondition` | `preconditions` and inferred inputs | whether request state fits |
| `output` | `output_shape` | expected deliverable |
| `workflow_step` | `workflow` | procedural behavior |
| `dependency` | tools/APIs/platforms | feasibility condition |
| `resource` | files/references/examples | context-loading condition |
| `avoid_condition` | `not_for` | negative boundary |
| `success_criterion` | extracted or inferred success condition | what completion means |
| `public_source` | public import metadata | provenance only |

Core edge types:

| Edge | Direction | Score Role |
|---|---|---|
| `belongs_to_family` | skill -> family | weak positive prior |
| `triggered_by` | skill -> trigger | strong positive |
| `expects_input` / `has_precondition` | skill -> input/precondition | positive when request requires it |
| `produces_output` | skill -> output | strong positive |
| `has_workflow_step` | skill -> workflow step | strong positive |
| `requires_dependency` | skill -> dependency | positive only if request/tool context requires it |
| `uses_resource` | skill -> resource | positive only if request asks for examples/files/references |
| `optimized_for` | skill -> success criterion | positive when success condition matches |
| `avoid_when` | skill -> avoid condition | negative penalty |
| `is_parent_of` / `delegates_to` | broad skill -> atomic skill | hierarchy handling; usually penalize broad parent as final answer |
| `derived_from_public_skill` | skill -> public source | provenance only |

Important rule:

Do **not** use benchmark-only `confusable_with` edges for final retrieval if they are derived from gold labels or alternatives. They are useful for analysis, but they can leak benchmark structure. If used at all, they must be created only from unsupervised similarity over public metadata and reported separately.

## M5 Retrieval Procedure

Proposed graph retrieval has two variants.

### M5a: Graph-Only Retrieval

1. Parse the request into requirement nodes:
   - action/trigger
   - input/precondition
   - desired output
   - workflow/procedure
   - dependency/tool/platform
   - resource/reference need
   - boundary/avoid condition
   - success criterion
2. Match request nodes to graph attribute nodes using lexical similarity or embeddings over node text.
3. Score each skill by its matched typed edges.
4. Return ranked skills.

This tests whether graph structure alone can retrieve the right skill.

### M5b: Hybrid Dense + Graph Rerank

1. Use dense retrieval or flat retrieval to get top-50/top-100 candidates.
2. Build a subgraph containing those skills and their adjacent attribute nodes.
3. Match request nodes to candidate skill edges.
4. Rerank candidates using graph score plus normalized first-stage score.

This is the more realistic final comparison because graph matching is used as a precision layer after broad recall.

## Proposed Graph Score

Start with a transparent weighted score:

```text
graph_score(skill) =
  0.20 * trigger_match
+ 0.20 * output_match
+ 0.20 * workflow_match
+ 0.15 * input_precondition_match
+ 0.10 * success_criterion_match
+ 0.05 * family_match
+ conditional_dependency_bonus
+ conditional_resource_bonus
- avoid_boundary_penalty
- broad_parent_penalty
```

For hybrid M5b:

```text
final_score =
  0.35 * normalized_first_stage_score
+ 0.65 * normalized_graph_score
```

The exact weights should be treated as a first transparent baseline, then tested with ablations. Do not tune weights repeatedly on final test results.

## Edge Ablations

To answer the thesis question, M5 should run edge ablations:

| Ablation | Purpose |
|---|---|
| family only | tests hierarchy/category prior |
| trigger only | tests use-condition value |
| trigger + output | tests output as procedural discriminator |
| trigger + output + workflow | tests main procedural hypothesis |
| + input/precondition | tests feasibility/input-state information |
| + dependency/resource | tests external context signals |
| + avoid penalties | tests boundary handling |
| full graph | tests combined graph representation |

Expected pattern:

- `trigger + output + workflow` should provide the largest stable gain.
- Dependencies/resources should help only when the request actually makes them relevant.
- `avoid_when` should reduce plausible-but-wrong false positives, but may hurt if extraction is noisy.
- Family-only/tree-only should be efficient but vulnerable to branch errors.

## How This Supports The Thesis

M3/M6-v1/M5 answer different questions:

| Method | Same Information? | Architecture Question |
|---|---|---|
| M3 structured-card retrieval | R2 serialized as text | Does exposing fields help at all? |
| M6-v1 field-aware rerank | R2/R3 fields | Does request-to-skill field matching improve precision? |
| M5 graph retrieval | R4 edges from the same fields | Does explicit relational structure improve over serialized fields? |

If M3, M6-v1, and M5 all improve when `output` and `workflow` are included, the thesis can claim those information types are important.

If M5 improves over M6-v1, the thesis can additionally claim graph structure is useful.

If M5 does not improve over M6-v1, the thesis can still claim the information matters, while graph architecture may be unnecessary overhead for this benchmark.

## Implementation Status

Current:

- R4 edge export exists.
- M4 tree routing is not implemented.
- M5 graph retrieval/reranking is not implemented.

Recommended order:

1. Implement `M6-v1` first, because it directly tests field-to-field matching.
2. Implement M5b hybrid dense + graph rerank using the same request parser and field nodes.
3. Implement M5 edge ablations.
4. Implement M4 tree routing only if a scalability/branch-exclusion comparison is needed.

