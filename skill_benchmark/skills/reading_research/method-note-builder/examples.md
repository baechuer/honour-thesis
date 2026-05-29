# Method Note Builder Examples

## Example 1

User ask:

`Extract method notes from this paper so I can compare its setup with another system later.`

Example output:

- Task or problem setting: Multi-step tool-using agent benchmark with long-horizon tasks.
- Method or procedure: The system first decomposes the task, retrieves tools, and then executes stepwise with intermediate state tracking.
- Evaluation setup: Compared against direct prompting baselines on benchmark success rate and completion reliability.
- Important assumptions or limitations: The benchmark tasks are structured and may not reflect noisy real user environments.

## Example 2

User ask:

`Give me notes on how this paper's method actually works.`

Example output:

- Task or problem setting: Personal-agent skill retrieval under semantic overlap.
- Method or procedure: The paper constructs confusable skill clusters and evaluates skill selection under controlled prompts.
- Evaluation setup: Measures top-1 selection, nearby skill consultation, and downstream output quality.
- Important assumptions or limitations: Results depend on skill metadata quality and the benchmark's chosen prompt set.
