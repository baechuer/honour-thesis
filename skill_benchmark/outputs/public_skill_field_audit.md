# Public Skill Field Audit

This report audits imported public `SKILL.md` artifacts for representation-field evidence.

Statuses:

- `explicit`: field appears in frontmatter or a clear heading.
- `extractable`: field is not clearly structured, but keywords/body evidence suggest it can be parsed or inferred.
- `missing`: no strong evidence detected by this heuristic audit.

Important limitation: this is a heuristic audit. It should be followed by a small manual sample review before final thesis claims.

## Corpus

- Public skills audited: 460
- Original public `SKILL.md` files used: 460/460
- Mean words per skill: 1194.02
- Median words per skill: 1141
- Skills with scripts directory: 0/460
- Skills with references directory: 0/460
- Skills with assets directory: 0/460

## Origins

| Origin | Count |
|---|---:|
| `claude-office-skills/skills` | 136 |
| `akillness/oh-my-skills` | 127 |
| `GeniusHTX/SWE-Skills-Bench` | 49 |
| `openai/skills` | 41 |
| `mattpocock/skills` | 25 |
| `addyosmani/agent-skills` | 23 |
| `anthropics/skills` | 17 |
| `huggingface/skills` | 15 |
| `addyosmani/web-quality-skills` | 6 |
| `numman-ali/n-skills` | 5 |
| `kepano/obsidian-skills` | 5 |
| `lbussell/agent-skills` | 4 |
| `wshobson/agents via SkillRet preview` | 2 |
| `obra/superpowers via SkillRet preview` | 2 |
| `K-Dense-AI/scientific-agent-skills via public skill directory` | 1 |
| `tmchow/agent-skills` | 1 |
| `vercel-labs/skills` | 1 |

## Field Prevalence

| Field | Explicit | Extractable | Missing | Explicit % | Explicit or Extractable % |
|---|---:|---:|---:|---:|---:|
| `routing_trigger` | 460 | 0 | 0 | 100.0% | 100.0% |
| `input_precondition` | 116 | 259 | 85 | 25.2% | 81.5% |
| `output_artifact` | 208 | 184 | 68 | 45.2% | 85.2% |
| `workflow_procedure` | 330 | 58 | 72 | 71.7% | 84.4% |
| `constraints_boundaries` | 190 | 167 | 103 | 41.3% | 77.6% |
| `dependencies_tools` | 335 | 56 | 69 | 72.8% | 85.0% |
| `resources_references` | 307 | 70 | 83 | 66.7% | 82.0% |
| `examples_tests` | 292 | 140 | 28 | 63.5% | 93.9% |
| `safety_side_effects` | 52 | 118 | 290 | 11.3% | 37.0% |
| `portability_environment` | 286 | 85 | 89 | 62.2% | 80.7% |
| `hierarchy_links` | 116 | 27 | 317 | 25.2% | 31.1% |

## Provisional Interpretation

- `routing_trigger`: common or broadly extractable.
- `input_precondition`: common or broadly extractable.
- `output_artifact`: common or broadly extractable.
- `workflow_procedure`: common or broadly extractable.
- `constraints_boundaries`: common or broadly extractable.
- `dependencies_tools`: common or broadly extractable.
- `resources_references`: common or broadly extractable.
- `examples_tests`: common or broadly extractable.
- `safety_side_effects`: rare under current heuristic.
- `portability_environment`: common or broadly extractable.
- `hierarchy_links`: rare under current heuristic.

## Manual Review Sample Candidates

These examples are useful for checking whether the heuristic labels are reasonable.

| Skill | Origin | Explicit/Extractable Fields | Missing Fields |
|---|---|---:|---|
| `public-mattpocock-edit-article` | `mattpocock/skills` | 1 | constraints_boundaries, dependencies_tools, examples_tests, hierarchy_links, input_precondition |
| `public-anthropic-internal-comms` | `anthropics/skills` | 2 | constraints_boundaries, dependencies_tools, examples_tests, hierarchy_links, input_precondition |
| `public-mattpocock-grill-me` | `mattpocock/skills` | 2 | constraints_boundaries, dependencies_tools, examples_tests, hierarchy_links, output_artifact |
| `public-mattpocock-obsidian-vault` | `mattpocock/skills` | 2 | constraints_boundaries, dependencies_tools, hierarchy_links, input_precondition, output_artifact |
| `public-mattpocock-zoom-out` | `mattpocock/skills` | 2 | dependencies_tools, examples_tests, hierarchy_links, input_precondition, output_artifact |
| `public-office-layout-analyzer` | `claude-office-skills/skills` | 9 | hierarchy_links, safety_side_effects |
| `public-office-lead-qualification` | `claude-office-skills/skills` | 9 | hierarchy_links, resources_references |
| `public-office-lead-routing` | `claude-office-skills/skills` | 9 | constraints_boundaries, safety_side_effects |
| `public-office-linear-automation` | `claude-office-skills/skills` | 9 | constraints_boundaries, safety_side_effects |
| `public-office-mailchimp-automation` | `claude-office-skills/skills` | 9 | safety_side_effects, workflow_procedure |
| `public-oh-my-system-environment-setup` | `akillness/oh-my-skills` | 11 |  |
| `public-oh-my-video-production` | `akillness/oh-my-skills` | 11 |  |
| `public-openai-cli-creator` | `openai/skills` | 11 |  |
| `public-openai-hatch-pet` | `openai/skills` | 11 |  |
| `public-openai-screenshot` | `openai/skills` | 11 |  |
