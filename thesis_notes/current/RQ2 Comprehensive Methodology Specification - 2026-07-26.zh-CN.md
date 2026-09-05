# RQ2 综合方法论规范（中文对照翻译）

> **2026-08-15 状态更正。** RQ2a 已完成并保持关闭。RQ2b 的 base-v1 B0G 全池盲审在机制上已经完成，但最终 acceptable-set 冻结仍被 **检索前阻止**：7,710 个已解决审查单元中，有 14 个 strict-gold 不再 fully acceptable，另有 8 个计分 prompt 在已审候选中没有任何 fully acceptable 候选。随后用户要求只复核这 14 个原 gold label：保留 6 个可作为 gold label skill 的原标签，剔除 8 个存在实质 workflow mismatch 的 prompt；没有替换为新的 gold，也没有重跑 B0G。381-prompt、仅 strict-gold 的 v1.1 manifest 已 materialise，并通过本地 identity/count endpoint verifier 和合成 B1/B2 execution-contract smoke。其后，用户单独批准了 B1R 的本地 I3C 原文提取：57 个 chunks、2,433 条 I3C rows 已通过自动 validation，并生成同证据的 I3C-fielded/I3-flat。首个 120 条盲审包因缺少所需的角色分层覆盖而保留为未审查的 superseded 版本；修正后的 v2 包覆盖 eventual-gold、hard-neighbour 和 background，并由六份各 20 条的本地盲审完成。v2 在检索前拒绝 v1.1：16 个 critical errors、7 个 major-error rows；1,800 个 `background_scale` 源技能均含 benchmark/gold-label 与通用 routing scaffolding，必须先形成新语料版本并重新盲审。没有 RQ2b 检索、embedding、reranking、provider call 或 thesis result。

日期：2026-07-26

状态：RQ2a 的协议、表示构造、development 选择、confirmatory 矩阵、冻结统计分析、成本账本、用户审阅和 thesis 写入均已**完成**并保持关闭。最终 confirmatory study 包含 280 个 clusters、600 个 prompts、22 个 conditions 和 13,200 个对齐 rows。RQ2b 的预定 B2 矩阵包含两个独立 reranker：SkillRouter-Reranker-0.6B 与通用 Qwen `qwen3-rerank`，两者必须对每个 B1 条件的同一份已持久化 Top-20 候选集独立排序。B0F 与 B0F-A1 原生 SkillRouter-embedding amendment 均已获用户批准；v1.1 endpoint verifier、严格 B1/B2 execution-contract 与狭义 strict-contract seal 均已完成，但不运行检索。B1R 的精确原文提取已获用户批准并在本地完成：2,433 条 I3C rows、57 个 chunks 和匹配的 I3C-fielded/I3-flat 自动 gates 全部通过；下一个 gate 是独立完成 120 条盲审。Qwen／SkillRouter 模型适配器、任何科学性 selector run 与 thesis 结果写入仍未获授权。

> **2026-08-02 RQ2b 覆盖说明。** 本中文阅读副本后文原有的 RQ2b `v0.4`、带 tag 的 I1、K=50、scale/confusability parking matrix 等细节均已过时，仅保留作历史阅读背景，不得作为实施指令。当前 RQ2b 的唯一 canonical 执行合同是 `thesis_notes/current/RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md`；高层英文定义已同步在 `RQ2 Comprehensive Methodology Specification - 2026-07-26.md`。科学协议批准、I3C 来源文本传输、Qwen API、hosted SkillRouter 与 thesis 结果写入是五个独立 gate。

翻译说明：本文件是英文规范的中文对照翻译，不替代英文原件。实验标签、模型名称、指标名称、数值和公式均保留原样；如两份文件存在歧义，以经批准并冻结的英文协议为准。

操作状态、实施任务与旧方案取代关系以 `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md` 为准。

2026-08-02 confirmatory 结论：Qwen single-vector 下的主要正向字段组织假设被拒绝，`fielded - flat = -6.7pp`，95% CI 为 `[-9.9pp,-3.6pp]`。冻结的 Qwen `uniform-top-two` field-aware 方法相对 fielded single-vector 恢复 `+6.6pp`，95% CI 为 `[+2.1pp,+11.1pp]`，但其 Top-1 `0.823` 与 flat Qwen `0.824` 基本相同。BM25、Qwen 和 SkillRouter 都表明 operational facts 明显优于 `shared-only`。详细英文分析见 `thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md`。

## 1. 总体决定

RQ2 应继续作为一个与 RQ1 同等重要的核心研究问题，但通过两个相互衔接的子研究来回答：

1. **RQ2a：表示机制（representation mechanism）**使用经过人工审定的真值字段（oracle-controlled field values），隔离检验：当相同的操作性事实被明确组织、压缩，或较少受到信息稀释时，选择器是否能够更有效地利用它们。
2. **RQ2b：端到端检索验证（end-to-end retrieval validation；B0F 已冻结，执行仍按阶段审批）**将检验：当系统必须先从完整技能库中检索出 gold 技能时，所选表示是否仍然有用；同时将测量准确率、候选召回率、延迟和上下文成本。

下游任务成功率只保留为小规模的次要验证。关系感知图、层级遍历、多技能组合和前置条件规划不属于 RQ2 核心范围，因为它们引入了 RQ1 未研究的技能间信息，并且需要对关系敏感的 gold 任务。

## 2. 拟议研究问题

> **RQ2：在存在语义混淆的情况下，技能表示方式和检索流水线的选择，会如何影响 RQ1 所识别的路由相关操作性信息的保留与利用？由此产生怎样的准确率、候选召回率和检索成本权衡？**

### RQ2a：表示机制

> 在查询、候选技能、操作性命题和选择器均相同的条件下，明确的字段组织和受控的信息稀释，会如何影响选择器区分近邻技能的能力？

RQ2a 回答“为什么某种表示有效”。它不是一个全语料库检索基准。实验保证 gold 技能已经位于候选集中，因此候选生成失败不会遮蔽表示本身的影响。

### RQ2b：端到端检索验证

**协议状态：预定 B2 矩阵包含 SkillRouter-Reranker-0.6B 和通用 Qwen `qwen3-rerank` 两个独立 comparator；它们必须对相同 B1 条件的完全相同、已持久化 Top-20 候选集独立评分，不能重建候选集或互相混合分数。v1.1 strict-only endpoint verifier、execution-contract smoke 和本地 implementation seal 已通过，但均不产生科学结果。base-v1 仍因 14 个 strict-gold 及 8 个 fully-acceptable 覆盖问题而阻止；v1.1 只支持 381 个 prompts 的 strict-gold endpoints。2026-08-15 已单独批准并完成 B1R：完整 I3C 语料、I3C-fielded/I3-flat 和 role-stratified 120 条盲审均已建立。该盲审已完成并在检索前拒绝 v1.1（16 个 critical、7 个 major）；必须先获批修正全语料，才可能重新进行 QA。B1 检索、B2 reranking、provider execution 和结果行当前均不可运行。**

> 当系统不能保证候选集中包含 gold 技能时，紧凑元数据、原始完整技能 artifact，以及明确的操作性事实表示，会如何分别与词法检索、稠密检索和重排序交互？

RQ2b 回答“某种表示在实际的先检索、后重排序流水线中是否仍然有用”。它将第一阶段排除 gold 的失败，与后续排序失败明确分开。

## 3. 与 RQ1 的关系

RQ1 提供了一组边界明确、属于单个技能内部的操作性信息：

- 使用条件（use condition）；
- 输入／前置条件（input/precondition）；
- 输出／artifact（output/artifact）；
- 工作流／步骤（workflow/procedure）；
- 依赖／资源或能力兼容性（dependency/resource or capability compatibility）；
- 边界／不适用范围（boundary/not-for）；
- 成功／验证标准（success/verification）。

示例／测试继续作为支持性信息或负对照类别，而不是第八个操作性字段。

RQ2 **不要求** RQ1 证明以上字段涵盖所有可能的路由信号。论文的主张仅限于已经研究的操作性字段，不能宣称这是一个普适或穷尽的技能 schema。

下列信息仍然不属于核心范围：

- 技能之间的前置关系；
- 技能组合关系，以及输出到输入的衔接关系；
- 备选／替代关系；
- 父子分类和多父类别归属；
- 技能历史表现或用户特定偏好；
- 多技能工作流角色；
- 学习得到的图边，或人工编写的 ontology 关系。

这些属于技能间信号或系统上下文信号。若要公平检验它们，需要对关系敏感的 prompts 和一套新的 gold 标准。

## 4. 分析单位

主要统计推断单位是**近邻技能 cluster**，而不是单次重复 prompt 或单次模型调用。

每个 RQ2a 测试单元包含：

- 一个冻结的用户查询；
- 一个含三个同族候选的近邻技能 cluster；
- 一个 gold 技能；
- 两个在主题上合理、但在操作要求上不兼容的同族技能；
- 在所有表示条件下完全相同的候选身份；
- 由确定性规则生成的候选顺序随机化；
- 一个表示条件；
- 一个冻结的选择器及其评分规则。

属于同一个 cluster 的所有 prompt 变体，在重采样和统计分析中必须始终作为一组处理。

RQ2b 以单个查询作为排序单位；如果存在技能 family 标签，则置信区间应按 cluster 或 family 分组计算。

## 5. 数据来源

### 5.1 RQ2a 受控数据来源

复用已经完成的 RQ1 单字段隔离测试套件：

| 字段测试套件 | Clusters | Prompt 变体 |
|---|---:|---:|
| 使用条件 | 50 | 100 |
| 输入／前置条件 | 50 | 100 |
| 输出／artifact | 50 | 100 |
| 依赖／资源 | 50 | 100 |
| 边界／不适用范围 | 50 | 150 |
| 成功／验证标准 | 50 | 100 |
| 工作流／步骤 | 50 | 100 |
| **总计** | **350** | **750** |

在进行任何 RQ2 调参之前，按 cluster 划分 20/80 的协议数据集：

- 开发集：每个字段 10 个 cluster，共 70 个 cluster、约 150 个 prompts；
- 验证性测试集：每个字段 40 个 cluster，共 280 个 cluster、约 600 个 prompts。

这种划分用于约束调参纪律，并不声称测试 cluster 从未被研究者见过。RQ1 已经分析过它们各字段的区分能力；RQ2 检验的是另一种干预，即如何表示这些已经确立的命题。

RQ2a 的 source of truth 是每个 cluster 中经过审阅的 `unit.json`，而不是一次新的模型提取。这些文件已经包含共享的非目标字段，以及各同族技能特有的精确目标值。因此，它们可以构成一个真值表示实验，使提取质量不可能成为结果差异的解释。

受控 `SKILL.md` 已经通过规则化标题明确展示七个字段。因此，它们是结构化的规范卡片，而不是现实中带有噪声的 I2 文档。可以保留它们作为诊断条件，但不能把它们描述成 RQ2b 所使用的自然完整文档基线。

只有在冻结全部主要 RQ2a 决策之后，才可以将 examples/tests 套件加入为负对照诊断。

### 5.2 RQ2b 本地完整技能库数据

RQ2b 以当前冻结的 benchmark manifest 为基础，但必须先通过 provenance gate：

- benchmark：`benchmark-v0.4-2026-06-16`；
- 245 个受控 prompts；
- 144 个 public-gold prompts；
- 12 个低信息量压力测试 prompts，单独报告；
- 2,433 个技能；
- 1,800 个用于规模测试的背景干扰技能；
- 460 个导入的公开技能。

主要结果必须按以下 strata 分开：

- controlled；
- public-gold；
- low-information／underspecified stress。

对于导入的公开技能，I2 来源必须是上游的 `source/SKILL.original.md`，而不是本地标准化 wrapper。受控技能使用其人工编写的源 artifact。如果当前文件与冻结 manifest 不一致，应建立新的 benchmark 版本，而不能静默修改 v0.4。

### 5.3 可选的外部可迁移性数据

SkillRouter-Eval-Core 语料库可用于可迁移性附录：

- 75 个默认计分任务；
- 78,361 个 Easy 技能；
- 79,141 个 Hard 技能；
- 780 个仅在 Hard 中出现的干扰技能；
- 针对 79,141 个技能的完整、已清理 I3C V2 提取。

回答核心 RQ2 不依赖该外部语料库。完整的神经检索重跑成本很高，并且当前 I2 神经检索对照尚不完整。已有 FTS/BM25 结果和恢复得到的神经检索结果行，必须根据其真实完成状态和 provenance 准确标注。

## 6. 表示条件

所有新表示 artifact 都必须具备独立的 manifest、serializer 版本、源文件 hash 和身份对齐检查。

通用身份规则：

- 每一种候选表示都保留相同的技能名称，或中性的受控标识符；
- 候选 ID、gold／alternative 角色和 benchmark 标签绝不能写入选择器可见文本；
- 受控技能名称必须保持语义中立；
- RQ2b 的 I3C 与 I3-flat 使用相同的技能名称标题，从而使匹配比较只改变字段组织；
- 如果某个提取字段为空，则 I3C 和 I3-flat 都省略它；只有当来源明确陈述否定值时才保留，不能人为插入“none”之类的合成陈述。

在进行任何字段顺序诊断之前，规范字段顺序为：使用条件、输入／前置条件、输出／artifact、工作流／步骤、依赖／资源、边界／不适用范围、成功／验证标准。

### 6.1 RQ2a 人工审定事实控制表示

| 标签 | 定义 | 用途 |
|---|---|---|
| `shared-only` | 同族技能共享的中性技能描述／上下文；除身份外完全相同。 | 不包含决定性操作差异的歧义锚点。 |
| `same-facts-fielded` | 将 `unit.json` 中经过审阅的精确值，以明确字段标签和字段边界序列化。 | 在没有提取误差的情况下，检验明确的操作性事实表示。 |
| `same-facts-flat` | 使用中性分隔符拼接完全相同的值，并移除字段标签和标题。 | 隔离字段标签和字段边界的作用。 |
| `same-facts-prose` | 使用确定性的自然语言模板表达相同的人工审定命题，不能增加或遗漏任何命题。 | 将明确字段与简洁 prose 进行比较。 |
| `same-facts-order-controlled` | 使用相同的字段化值，但通过冻结的随机种子，在 cluster 之间平衡字段顺序。 | 检测位置偏差。 |
| `same-facts-diluted-1x/2x/4x` | 使用相同的字段化值，并逐级添加共享且不具区分性的执行支持文本。 | 测量信息稀释。 |

现有受控完整 `SKILL.md` 是 oracle 字段的一种诊断性序列化，而不是自然 I2 基线。

`shared-only` 复现 RQ1 已经确立的共享上下文歧义，只作为锚点；它不是 same-information representation comparison。RQ2a 真正新增的证据来自 `same-facts-fielded`、`same-facts-flat`、`same-facts-prose` 和 `same-facts-diluted` 之间的比较。

#### 6.1.1 每一种 RQ2a representation 的完整示例

以下 worked example 使用经过审阅的真实 RQ1 cluster：
`skill_benchmark/rq1a_field_discriminability/input_precondition/clusters/ip01_pdf_scanned_tables/unit.json`。
它用于说明每种 information treatment 的含义，目前还不是已经冻结的 byte-level serializer 规范。在评分之前，仍须对精确模板、分隔符、空白、候选标识符和 padding blocks 进行版本化并冻结。

冻结的 direct query：

```text
Extract the invoice table rows from this scanned PDF image and return the shared structured report.
```

三个候选的全部非目标事实完全相同，只有经过审阅的 input/precondition 值不同：

| 候选 | 角色 | Input/precondition |
|---|---|---|
| A | Gold | scanned or image-based PDF invoice packet |
| B | 不兼容的同族技能 | native PDF invoice packet with embedded selectable text |
| C | 不兼容的同族技能 | photographed invoice images supplied as separate image files |

**`shared-only`**

选择器看到的 Candidate A：

```text
Skill: Candidate A
PDF invoice table normalization skill.
```

Candidates B 和 C 具有相同描述，仅中性候选标识符不同。决定性的输入事实完全缺失，因此该条件是 ambiguity anchor，而不是 matched-content representation comparison。

**`same-facts-fielded`**

选择器看到的 Candidate A：

```text
Skill: Candidate A

Use Condition
Use when the user needs pdf invoice table normalization skill over a provided input artifact.

Input / Precondition
scanned or image-based PDF invoice packet

Output Artifact
A structured result report with normalized findings, evidence references, input-fit notes, and unresolved assumptions.

Workflow / Procedure
1. Confirm that the provided material matches the stated input/precondition.
2. Inspect the provided material for the shared task without changing the task scope.
3. Extract or assess the relevant information using the same analysis checklist.
4. Return the shared structured result report with evidence references and caveats.

Success / Verification
- The report addresses the requested task using only the provided material.
- The report cites the evidence used for each finding or extracted record.
- The report flags missing or mismatched input instead of silently switching tasks.

Boundary / Not For
- Do not select this skill when the provided material does not match its input/precondition.
- Do not change the requested output format or workflow because of the input variant.

Dependency / Resource
- Access to the provided artifact or data source.
```

Candidates B 和 C 使用完全相同的 headings 和非目标值；只有 `Input / Precondition` 下方的文字，替换为上表中相应的人工审定值。

**`same-facts-flat`**

选择器看到的 Candidate A 包含完全相同的字段值，并保留相同的规范顺序，但没有任何字段名称或标题：

```text
Skill: Candidate A
Use when the user needs pdf invoice table normalization skill over a provided input artifact. |
scanned or image-based PDF invoice packet |
A structured result report with normalized findings, evidence references, input-fit notes, and unresolved assumptions. |
Confirm that the provided material matches the stated input/precondition. Inspect the provided material for the shared task without changing the task scope. Extract or assess the relevant information using the same analysis checklist. Return the shared structured result report with evidence references and caveats. |
The report addresses the requested task using only the provided material. The report cites the evidence used for each finding or extracted record. The report flags missing or mismatched input instead of silently switching tasks. |
Do not select this skill when the provided material does not match its input/precondition. Do not change the requested output format or workflow because of the input variant. |
Access to the provided artifact or data source.
```

中性分隔符保留 value boundaries，以便确定性解析，但不说明哪一个值属于 input、output、boundary 或 dependency。Candidates B 和 C 仍然只改变经过审阅的输入值。

**`same-facts-prose`**

选择器看到的 Candidate A 使用一个冻结的自然语言模板表达完全相同的人工审定命题：

```text
Candidate A is used when the user needs pdf invoice table normalization skill over a provided input artifact. It accepts a scanned or image-based PDF invoice packet and returns a structured result report with normalized findings, evidence references, input-fit notes, and unresolved assumptions. It first confirms that the material matches the stated input/precondition, inspects it without changing task scope, extracts or assesses the relevant information using the shared checklist, and returns the report with evidence references and caveats. Success requires the report to address the requested task using only the provided material, cite the evidence used for each finding or extracted record, and flag missing or mismatched input rather than silently switching tasks. It must not be selected when the material does not match its input/precondition, and it must not change the requested output format or workflow because of the input variant. It requires access to the provided artifact or data source.
```

Prose 模板只增加 “accepts”“returns”“requires”等语法连接词，不能增加新的操作性命题。由于这些连接词本身也传达语义角色，所以该条件属于次要比较。

**`same-facts-order-controlled`**

该条件使用相同的 fielded 文本和完全相同的值，但按照冻结的 counterbalancing schedule 只改变字段顺序。一个说明性顺序是：

```text
Skill: Candidate A
Workflow / Procedure: [the same four reviewed steps]
Boundary / Not For: [the same two reviewed boundaries]
Output Artifact: [the same reviewed output value]
Dependency / Resource: [the same reviewed dependency]
Input / Precondition: scanned or image-based PDF invoice packet
Success / Verification: [the same three reviewed criteria]
Use Condition: [the same reviewed use-condition value]
```

以上方括号内容只是帮助理解的简写，不是实际 selector-visible text。实现后的 serializer 必须填入 `same-facts-fielded` 中展示的完整值；只能改变字段顺序。

**`same-facts-diluted-1x/2x/4x`**

每个 diluted 条件都从完整的 `same-facts-fielded` 文本开始，然后增加冻结数量、可读、同族技能完全相同且不具区分性的支持文本。说明性的 padding blocks 为：

```text
P1: Review the provided material carefully and preserve evidence references in the final report.
P2: Record unresolved assumptions and note any limitations affecting interpretation.
P3: Use a consistent reporting structure and check the report for internal consistency.
P4: Avoid unsupported claims and retain traceability from findings to source material.
```

- `same-facts-diluted-1x` 添加 P1；
- `same-facts-diluted-2x` 添加 P1 和 P2；
- `same-facts-diluted-4x` 添加 P1 至 P4。

最终 padding 必须与全部同族特有的决定性值和 leakage terms 自动比对。同一个 cluster 的所有同族技能接收 byte-identical padding。因此，该处理改变的是信息稀释程度，而不是候选相关性。

在全部 same-facts 条件中，底层操作性命题和候选身份保持不变。受控改变的变量只有字段标签、discourse form、字段顺序，或共享支持文本的数量。

### 6.2 RQ2b 实际表示

| 标签 | 定义 | 所隔离的问题 |
|---|---|---|
| `I1` | 冻结的扁平卡片：名称、简短描述，以及规范 exporter 已包含的类别／标签元数据。 | 紧凑的 progressive-disclosure 基线。 |
| `I2` | 按照获批来源规则取得的完整原始技能 artifact。 | 最大自然信息量与自然噪声基线。 |
| `I3C-fielded` | 从完全相同的 I2 artifact 中，进行具有原文证据支撑的七字段 Codex/ChatGPT 式提取。空字段保持为空。 | 明确的操作性事实表示。 |
| `I3-flat` | 使用中性分隔符拼接与 I3C 完全相同的字段值，并移除全部字段标签和标题。 | 在提取事实完全相同的情况下，明确标签／边界是否带来额外帮助？ |
| `I2+I3C` | 原始 artifact 后附明确的字段卡片。 | 当原始文本仍然保留时，明确字段是否增加价值？ |

`same-facts-diluted` 不能使用随机字符、无意义文字，或只属于某一候选的独特填充。填充内容必须是可读的支持文本，在同一个 cluster 的同族技能之间完全相同，并且已经验证不会提及决定性字段值。

Matched-content 指命题相同，而不是机械地保证 token 数完全相同。字段标签本身属于结构干预，因此必然会增加少量 token。必须报告每个条件精确的 token／字符分布。如果 fielded 与 flat/prose 在测试单元的中位长度上相差超过 10%，则应按照预注册协议，使用共享中性文本增加一个长度匹配的敏感性条件；不能静默地只为预期表现较差的条件填充文本。

### 6.3 提取 provenance 规则

现有本地 frozen-v0.4 的 `R2/I3` 条件是启发式提取 `I3H`；本地付费模型 artifact 是 `I3M`。两者都不能重新标注为 `I3C`。

在运行新的本地 RQ2 主要矩阵之前：

1. 使用冻结的 V2 提取 prompt，从经过批准的精确 I2 artifacts 生成本地 I3C；
2. 每个技能必须且只能生成一行；
3. 保留 `skill_id` 和来源身份；
4. 验证 JSON 解析和 schema；
5. 对照源文档验证每一个 evidence span；
6. 允许字段稀疏或为空，不能为了填满字段而产生幻觉；
7. 记录字段级 missing、generic 和 uncertainty 标志；
8. 从这一个 I3C artifact 确定性地产生 `I3-flat`；RQ2a 使用 oracle-controlled 变体，而不是模型提取的变体。

## 7. 选择器与流水线条件

### 7.1 RQ2a 选择器

主要选择器：

- Qwen `text-embedding-v4`，冻结配置，使用余弦相似度，不进行查询改写。

必须进行复现的选择器：

- BM25 词法排序；
- 一个冻结、适用于技能的 cross-encoder reranker，优先使用 `pipizhao/SkillRouter-Reranker-0.6B`，直接为固定候选集中的每个候选评分。

必须进行的次要机制选择器：

- 在 `same-facts-fielded` 上运行一个 Qwen 语义 field-aware selector。

仓库中已经存在 M6-v1 和 M6-v2 两个 field-aware 原型，但两者都不是符合 RQ2a 协议的选择器。M6-v1 是词法方法，并依赖持久化的第一阶段候选。M6-v2 会分别嵌入部分字段，但它使用旧的 frozen-v0.4 表示、请求字段解析、经过校准的字段权重、boundary penalty，以及第一阶段分数混合。因此，RQ2a 将复用并改造 M6-v2 的组件，而不能直接把旧 M6-v2 结果当作新证据，也不能声称该方法完全从零实现。

RQ2a field-aware adapter 必须：

1. 直接读取 `same-facts-fielded`；
2. 分别嵌入全部七个 operational fields；
3. 只嵌入原始用户 query，不能接收 benchmark 的 target-field 标签；
4. 直接为三个固定候选评分，不进行候选排除，也不混合第一阶段分数；
5. 不接收 gold、candidate role、cluster field 或 alternative metadata；
6. 输出各字段相似度、一个聚合候选分数、最终选择、rank margin 和 latency；
7. 缓存每一个唯一 query embedding 和 field embedding；
8. 对七个字段套件统一使用一个 target-agnostic 聚合规则。

只允许在 70-cluster development split 上比较两个聚合候选：最大字段相似度，以及相似度最高两个字段的无权重平均。随后必须只选一个规则，记录并冻结。验证性实验禁止使用字段特定权重、target-field oracle scoring 或 confirmatory-set tuning。

对于 RQ2a BM25，每种表示只建立一个索引，并包含全部 RQ2a 候选文档；不能针对每个查询或每个三候选 cluster 分别重算 IDF。评估时，只在该测试单元冻结的候选 ID 之间比较已持久化的分数。Qwen 文档 embeddings 同样对每种表示只计算一次，并在所有查询中复用。

可选诊断：

- 使用一个冻结的 LLM 选择器 prompt，一次查看所有同族候选。这是推理诊断，不是主要 leaderboard 结果行。

不能在验证性 clusters 上训练或调优任何选择器。所有模板、截断策略、pooling、字段顺序和并列处理规则，都必须在开发阶段结束后冻结。

### 7.2 RQ2b 第一阶段检索

必需：

- BM25；
- Qwen `text-embedding-v4`；
- 通过前瞻性 amendment 加入的 `pipizhao/SkillRouter-Embedding-0.6B` 必做次要 replication。

SkillRouter-embedding replication 使用发布版 query instruction、last-token pooling、1,024 维 L2-normalized vectors、cosine scoring，以及在固定模型配置 32,768-token 上限内的一份完整 representation。禁止 truncation 与 chunk aggregation；任何超长文本必须中止运行。必须绑定精确 model/revision/file hashes、cache、latency 与 zero-forward warm reproduction。

Qwen `text-embedding-v4` 与 `SkillRouter-Embedding-0.6B` 都属于 query／document 分开编码的 embedding retriever，但它们是训练目标与参数不同的模型。Qwen 是通用 provider 的 max-chunk primary dense condition；SkillRouter embedding 是面向技能调优的 full-context 必做次要 replication，不进入冻结的八项 primary hypothesis multiplicity family。B2 的预定比较同时包含 `SkillRouter-Reranker-0.6B` 与通用 Qwen `qwen3-rerank`；二者联合读取 query 与 candidate、逐对评分，不生成可复用的 document embedding，且都只能对同一份已持久化 Top-20 候选排序。

### 7.3 RQ2b 重排序

每个 B1 条件的预定 B2 comparator set 有三个分支：

- 仅第一阶段检索；
- 第一阶段检索加 `SkillRouter-Reranker-0.6B`；
- 第一阶段检索加通用 Qwen `qwen3-rerank`。

两个 reranker 是独立 comparator，不是 ensemble。对同一个 B1 条件，它们必须接收完全相同的 raw query、representation text、已持久化 Top-20 candidate IDs、候选顺序与 `K`；不得重建候选集、改写 query、读取 label metadata 或悄悄采用不同截断策略。候选集必须先持久化。

主要重排序预算：

- `K=20`。

`K=5` 只允许通过切片已经持久化的 K=20 分数完成，不产生新的 forward pass。`K=50` 不属于最小研究，除非未来先修订协议并另行授权。

retrieval-only 与 retrieval-plus-reranker 分支必须复用第一阶段各自的 query／document embeddings 或 lexical scores 以及已持久化候选集。SkillRouter reranker 与 Qwen reranker 都必须对同一 B1 条件下完全相同的冻结 Top-20 候选集评分，并分别持久化分数、tokens、latency、成本账本和 warm-cache verification。Qwen 执行仍以 B0F-A2 审查、批准与匹配 implementation seal 为前提。

## 8. RQ2a 实验矩阵

### 8.1 验证性核心矩阵

| 轴 | 验证性条件 |
|---|---|
| Prompt 集 | 280 个测试 clusters，约 600 个 prompts |
| 候选机制 | 仅包含三个同族技能 |
| 表示 | shared-only、same-facts-fielded、same-facts-flat、same-facts-prose、same-facts-diluted-2x |
| 核心选择器 | Qwen single-vector embedding；BM25；固定 cross-encoder |
| 必须的次要选择器 | 在 `same-facts-fielded` 上运行 Qwen 语义 field-aware adapter |
| 推理诊断 | 一个冻结的 LLM A/B/C/ABSTAIN selector；不属于核心 leaderboard 条件 |
| Gold | 现有 cluster gold |
| 主要结果 | 配对 top-1 accuracy |
| 次要结果 | MRR、近邻混淆、排名分差、选择器可见 tokens |

预计评分量：

- 600 prompts x 5 种表示 x 3 个候选 = 每个选择器 9,000 个 query-candidate 分数；
- 三个核心选择器合计 27,000 个分数；
- `same-facts-fielded` 上必须的 field-aware 对比另外产生 1,800 个候选分数；该数字不包括七个 component-field similarities，也不包括可选 LLM 诊断。

无需构建新语料库即可完成该实验。

### 8.2 RQ2a 诊断

只有在核心矩阵完成后才运行：

| 诊断 | 条件 | 目的 |
|---|---|---|
| 字段顺序 | same-facts-fielded 规范顺序与 same-facts-order-controlled | 检测位置偏差。 |
| 稀释曲线 | 0x、1x、2x、4x 填充 | 估计对逐渐增加的上下文噪声的稳健性。 |
| 无关候选 | 三个同族技能加五个固定无关技能 | 检查广义干扰项是否改变表示效果。 |
| 受控完整卡片 | 现有受控 `SKILL.md` 与 oracle-fielded 序列化 | 验证人工编写的规范卡片是否按预期表现；不能将其解释为自然 I2。 |
| 负对照信息 | 仅提供通用 examples/tests | 检验支持文本能否提供稳定的路由价值。 |

### 8.3 RQ2a 主要比较

预注册一个主要对比：

> 在验证性测试 clusters 上，使用 Qwen embedding 比较 `same-facts-fielded` 与 `same-facts-flat`。

必须复现：

- 在 BM25 下进行相同的配对比较；
- 在固定 cross-encoder 下进行相同的配对比较。

关键次要比较：

- same-facts-fielded 与 same-facts-prose；
- same-facts-fielded 与 same-facts-diluted-2x；
- same-facts-fielded 与 shared-only；
- 在完全相同的 `same-facts-fielded` 文本上，Qwen field-aware 与 Qwen single-vector。

## 9. RQ2b 实验矩阵（已冻结核心）

本节原来的宽泛 parking design 已缩减为最小 B1／B2 研究。精确表示 bytes、acceptable-set closure、分块、假设、推断、审批与停止规则均以 `RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md` 为准；当本概览不够具体时，该 B0F 哈希冻结的执行协议具有最高权威。

### 9.1 阶段 B1：完整技能库的第一阶段检索

| 轴 | 条件 |
|---|---|
| 语料库 | 经过批准的 2,433 技能完整库 |
| Prompt strata | 当前 v1.1 strict-gold execution overlay：243 个 controlled；138 个 public-gold；12 个 stress 单独报告 |
| 表示 | I1、I2、I3C-fielded、I3-flat |
| Retrievers | BM25；Qwen max-chunk embedding；SkillRouter full-context embedding 次要 replication |
| 候选预算 | 排名位置 1、5、20、50、100 |
| 主要指标 | strict Recall@20 与 strict Hit@1；v1.1 不提供 acceptable endpoints |
| 次要指标 | strict MRR@10、strict Recall@5/50/100、近邻漏检、无关技能误检 |

全部检索排名只持久化一次，并在后续阶段复用。

### 9.2 阶段 B2：对持久化候选进行固定重排序

| 轴 | 条件 |
|---|---|
| 第一阶段 | BM25；Qwen embedding；SkillRouter embedding |
| 表示 | I1、I2、I3C-fielded、I3-flat |
| 主要 K | 20 |
| 敏感性 K | 仅通过切片 K=20 已有分数得到 K=5；最小研究不运行 K=50 |
| Rerankers | SkillRouter cross-encoder 与通用 Qwen `qwen3-rerank`；两者对完全相同的已持久化 Top-20 候选集独立排序。Qwen 是预定的必做 comparator，但须等待 B0F-A2 审查/批准/seal 后才可执行。 |
| 指标 | conditional strict Hit@1、端到端 strict Hit@1/MRR、reranker gain/regression、重排序延迟／tokens；v1.1 不提供 acceptable endpoints |

最小 RQ2b 排除 nested-scale pools、graph／tree routing、外部 SkillRouter-Eval-Core portability、I2+I3C、下游任务执行与 K=50 reranking。原生 SkillRouter embedding 通过 B0F-A1 纳入；预定 B2 矩阵把 SkillRouter 与通用 Qwen `qwen3-rerank` 作为两个独立 reranker comparator，均对同一份 Top-20 排序。Qwen 通过 B0F-A2 等待审查、批准与 seal，不属于冻结 primary hypothesis family，且在此之前不得运行；其他扩展只有在完整 B1／B2 分析经审阅后才可提出。

### 9.3 历史可选扩展：分离规模与语义混淆（不属于当前核心）

使用现有技能构建确定性的嵌套候选池。

无关规模轴：

- 只包含 gold 和必要近邻；
- 加 100 个无关干扰技能；
- 加 500 个无关干扰技能；
- 加全部 1,800 个背景规模干扰技能；
- 自然完整技能库。

近邻轴：

- 没有已标注 hard neighbour；
- 一个已标注 hard neighbour；
- 两个或更多已标注 hard neighbours；
- 全部已知可接受和不兼容 alternatives。

所有表示必须使用固定随机种子和完全相同的候选池。主要 factorial analysis 在 controlled prompts 上运行，因为其同族 alternatives 已被明确标注。public-gold 版本仅作为探索性分析，因为自然编写的语料库中可能存在未标注但功能等价的技能。该分析检验性能下降主要来自一般性的技能库规模，还是来自局部语义竞争。

### 9.4 历史可选扩展：提取保真度诊断（不属于当前核心）

建立一个至少包含 100 个本地技能、经过人工审阅的分层样本，覆盖：

- gold 和 hard-negative 角色；
- controlled 和 public-original 来源；
- 短文档和长文档；
- 稀疏和密集的 I3C 卡片；
- 检索成功和检索失败案例。

只修正有源文档依据的遗漏，或没有证据支持的提取项；保留完整审计轨迹；并在受影响的查询和候选池上比较原始 I3C 与修正后 I3C。这可以估计观察到的路由表现，有多大程度受到提取问题，而不是表示或检索问题的限制。

### 9.5 阶段 B5：可选的外部可迁移性验证

只有在本地验证性研究完成后，才使用外部 SkillRouter-Eval-Core：

- 比较 I1、I2、I3C-fielded 和派生的 I3-flat；
- 复用现有完整 I3C 和 I2 源 artifacts；
- 首先运行基于磁盘的词法检索；
- 只有在每个条件完成后都能持久化 embeddings 和部分 summary 时，才运行神经检索条件；
- 在 Easy 和 Hard 的 embedding 与 reranker 结果行全部具备之前，不能宣称已经获得完整的 I2 与 I3C 神经检索矩阵。

## 10. Gold 与歧义规则

### Controlled clusters

- 保留冻结的 RQ1 gold；
- 候选身份保持不变；
- prompt 变体继承相同的 cluster 身份；
- 如果 prompt 不包含决定性要求，不能人为制造唯一 gold。

### Public-gold

- strict gold：指定的源技能；
- acceptable gold：strict gold 加上有文档依据、在功能上同样有效的 alternatives；
- ambiguous：多个候选同样合适，而且不存在可用于打破平局的条件；
- no-valid-skill：没有候选满足已记录的前置条件／输出要求。

Public gold 根据操作适用性定义，而不是根据词汇相似度定义。

理想的有效性标准是由两名独立标注者分别标注，并对分歧进行裁决。如果伦理审批、时间或招募条件不允许，则使用有记录的研究者人工审计，并明确将其报告为研究限制。不能把 agent 生成的标签描述为独立人类验证。

### 低信息量 prompts

将其作为拒答／请求澄清压力测试单独报告，不能合并到普通 top-1 accuracy 中。

## 11. 指标

### RQ2a 主要指标

- 配对 top-1 accuracy 差值；
- 95% cluster-bootstrap 置信区间。

### RQ2a 次要指标

- MRR；
- gold 与最高分同族技能之间的分数差；
- 近邻混淆率；
- 按 RQ1 字段划分的表现；
- 按 direct／paraphrase／contextual／implicit-authority 变体划分的表现；
- 选择器可见 tokens 或字符；
- 各选择器延迟。

### RQ2b 第一阶段指标

- strict 与 acceptable Hit@1；
- strict 与 acceptable Recall@5/20/50/100；
- MRR；
- 当存在多个可接受技能时的候选完整覆盖率；
- 错误去向：已标注近邻、无关干扰技能，或 gold 缺失。

### RQ2b 重排序指标

- 当 top-K 中至少包含一个有效 gold 时的 conditional Hit@1；
- 端到端 strict 与 acceptable Hit@1；
- 端到端 MRR；
- reranker 相对于其精确、已持久化第一阶段候选列表带来的提升；
- reranker regression rate：第一阶段 top-1 本来有效，但被 reranker 移走。

### 成本与效率

- 源文档和表示的字符数／token 数；
- 离线提取调用次数、tokens、时间和失败数；
- 文档 embedding 计算时间；
- 索引构建时间和索引大小；
- 查询 embedding 延迟；
- 搜索延迟；
- reranker pair 数、tokens 和延迟；
- 选择器可见 tokens；
- 在线路由时间的中位数和 p95；
- 冷缓存与热缓存测量。

必须区分三类 token：

- **index-visible tokens**：在文档 embedding 或词法索引阶段处理的全部表示文本；
- **reranker-visible tokens**：每次请求中，reranker 处理的查询和 top-K 候选表示文本；
- **agent-visible tokens**：路由结束后，为执行任务而加载的被选中完整技能 artifact。

不能把这三类统称为“selector tokens”。RQ2 主要比较 index-visible 和 reranker-visible 成本。除非加载策略本身发生变化，否则 agent-visible tokens 属于次要的引入／执行阶段。

货币成本可以作为带日期的补充指标报告，但不能作为主要效率指标。

## 12. 成本模型

将一次性成本与每查询成本分开。

设：

- `C_extract` = 一次性 I3C 提取成本；
- `C_doc_embed` = 一次性文档 embedding 成本；
- `C_index` = 一次性索引构建／存储成本；
- `C_query_embed` = 每次查询的 embedding 成本；
- `C_search` = 每次查询的检索成本；
- `C_rerank(K)` = 候选预算为 K 时，每次查询的重排序成本；
- `N` = 固定技能库版本所服务的查询数量。

则：

```text
amortised_cost_per_query(N)
= (C_extract + C_doc_embed + C_index) / N
  + C_query_embed
  + C_search
  + C_rerank(K)
```

应在一系列合理的 `N` 值上报告 break-even curves，而不是假设唯一的使用量。源技能发生变化时重新计算离线成本；只要表示版本仍然有效，就可以跨查询复用这些离线结果。

## 13. 假设

### RQ2a 假设

**H2a-Content。** 与 `shared-only` 相比，保留 RQ1 操作性事实的人工审定表示，将在近邻区分任务上表现更好，尤其是在 RQ1 中区分能力较强的字段上。

**H2a-Organisation。** 当选择器能够利用字段边界时，`same-facts-fielded` 将优于 `same-facts-flat` 和 `same-facts-prose`。该效应可能很小或只对特定模型成立；零结果则说明大部分价值来自事实本身，而不是字面字段标签。

**H2a-Explicit field use。** 在完全相同的 `same-facts-fielded` 文本上，如果分别计算字段分数能够保留被单向量 pooling 稀释的 query-to-field 匹配，那么 target-agnostic field-aware Qwen selector 应优于 Qwen single-vector selector。零结果表示：在当前聚合规则下，明确字段分段并未在“显示字段文本”之外带来可测量价值。

**H2a-Dilution。** 在决定性事实保持不变时，随着不具区分性的支持文本增加，路由准确率和分数差将下降。

**H2a-Reasoning interaction。** 与词法检索或单向量 embedding 检索相比，boundary、success/verification 和 workflow/procedure 更可能从 cross-encoder 或推理型选择器中获益。

**H2a-Field interaction。** input/precondition、use condition 和 output/artifact 预计在 paraphrase 条件下仍较稳健；隐式 boundary 以及细粒度 workflow/success 区分预计仍然更困难。

**H2a-Oracle validity。** 由于 RQ2a 使用经过审阅的 oracle 值，fielded、flat、prose 和 diluted 条件之间的任何性能差异，都可以归因于表示，而不是提取质量。

### RQ2b 假设（B0F 已冻结／尚未执行）

**H2b-Compression。** 在 Qwen max-chunk retrieval 下，I3C 的 acceptable Recall@20 将在已批准的实用边界内不劣于 I2，同时减少 index-visible 和 reranker-visible 文本。

**H2b-Discovery。** 在完整 controlled 与 public-gold strata 中，I3C 的 acceptable Recall@20 将优于 I1；本研究不声称存在一个未经标注的 “description lacks evidence” 子集。

**H2b-Organisation。** 因为字段边界会改变相同证据的编码方式，Qwen 下的 I3C-fielded 与 I3-flat 可能不同；不预设方向。

**H2b-Pipeline decomposition。** Reranking 会改善候选集内部的条件排序，但当有效技能不在候选集中时，它无法修复该查询。

**H2b-Retriever interaction。** BM25 对直接术语更强；稠密检索对 paraphrase 更稳健。因此，不同 retriever 下的表示排序可能不同。

**H2b-Efficiency。** I3C 预计比 I2 使用显著更少的 index-visible 与 reranker-visible tokens；其提取成本必须单独报告，并按重复查询量进行摊销。

### 次要下游假设

**H2-Downstream。** 正确路由应与更高的任务成功率相关，但路由准确率不会完全决定执行成功，因为技能质量、agent 推理、工具和环境也会产生影响。

## 14. 预期结果模式

以下是预注册的结果解释，而不是声称这些结果已经发生。

| 可能出现的模式 | 解释 |
|---|---|
| same-facts-fielded > same-facts-flat 且 > same-facts-prose | 在事实本身之外，明确字段组织提供了选择器可利用的结构。 |
| same-facts-fielded 约等于 same-facts-flat，且两者都 > shared-only | 操作性内容很重要；字面字段标签并非必要。 |
| same-facts-fielded 约等于 same-facts-prose | 紧凑事实很重要，但 schema 格式没有带来可测量的额外价值。 |
| field-aware Qwen > single-vector Qwen，且两者使用相同 same-facts-fielded | 明确的逐字段利用，在仅仅展示字段边界之外提供了额外价值。 |
| field-aware Qwen 约等于 single-vector Qwen | 分别计算字段分数及 target-agnostic 聚合，在当前设置中没有增加可测量价值。 |
| I2 > I3C | 提取／压缩移除了有用证据，或自然上下文提供了字段未捕获的交互信息。 |
| I3C > I2，同时 tokens 显著更少 | 明确保留事实减少了信息稀释，并改善准确率与成本之间的权衡。 |
| I3C 帮助 cross-encoder，但不帮助 BM25／Qwen embedding | 结构需要交互建模或字段敏感推理，而不是简单匹配。 |
| 稀释曲线基本平坦 | 选择器对新增支持文本稳健；在该设置中，完整文档噪声不是主要瓶颈。 |
| Recall 提高，但 Hit@1 没有提高 | 表示帮助候选生成，但未帮助最终消歧。 |
| Conditional reranking 提高，但端到端表现没有提高 | 第一阶段排除 gold 是瓶颈。 |
| 增加无关规模影响很小，但 hard-neighbour 数量增加会伤害表现 | 真正驱动失败的是语义混淆，而不只是语料库规模。 |
| 没有任何表示稳定获胜 | 不存在普适最优表示；应根据 retriever、字段类型和成本预算选择表示。 |

基于现有探索性证据，混合结果比“I3C 普遍获胜”更可信。目前本地 controlled 结果通常把 I3H 排在 I1 与 I2 之间，而 public-original 完整文本可能很强。相反，外部 79K 技能词法检索结果显示，已清理的 I3C 在若干指标上达到或超过 I2，而 token 量约为 I2 的十分之一。这些观察为新的 matched-content 实验提供动机，但不能回答该实验的问题。

## 15. 统计分析

### 验证性分析

- 保持 cluster 分组；
- 针对每个表示对比，计算配对 top-1 差值；
- 使用至少 10,000 次重采样的 cluster bootstrap；
- 报告以百分点表示的效应量和 95% 置信区间；
- 对预先声明的关键次要比较 family 使用 Holm correction；
- 报告全部零结果和负结果。

建议的最小实际重要效应：

- top-1 相差 3 个百分点；在验证性分析开始前，仍需由 supervisor 批准。

### 敏感性分析

- mixed-effects logistic regression：表示作为固定效应，cluster 作为随机截距；
- representation-by-selector interaction；
- representation-by-field interaction；
- 分别报告 direct、paraphrase、contextual 和 implicit-authority strata；
- strict 与 acceptable public-gold 评分；
- 按文档长度和提取完整度分层。

重复 API 调用不会产生独立观察。如果使用随机性选择器，应先在测试单元内部对重复调用求平均，并继续以 cluster 作为统计推断单位。

## 16. 次要下游验证

不要删除现有任务成功率和执行时间证据，但也不能将其作为表示质量的主要证据。

如果 provenance 可靠，则运行或保留一个小型分层子集：

- 30–50 个任务；
- 优先选择两个路由流水线选出不同技能的任务；
- 冻结 agent 模型、工具环境、技能 artifact、执行预算和 evaluator；
- 在执行之前比较路由得到的技能身份；
- 测量任务成功率、端到端时间、环境交互次数和失败类型；
- 在路由是否正确的条件下分析任务成功率。

分开记录：

- 路由延迟；
- 技能加载／上下文时间；
- 技能执行时间；
- 总任务完成时间。

下游章节回答路由改进能否转化为实际收益，但它不能确立表示效果的因果关系。

## 17. 图、树和关系方法的范围

### 不属于核心范围

- 带类型的前置／组合关系图；
- DAG 规划；
- 多技能检索；
- ontology 构建；
- 学习式关系提取；
- 层级训练；
- 分支路由优化。

这些方法携带或构造了超出 RQ1 单技能字段的信息。

### 允许的可选扩展

只有满足以下条件时，才允许进行一个小规模的 graph-as-index 实验：

- 节点暴露的表示与扁平基线获批的表示完全相同；
- 图边由完全相同的信息通过确定性规则派生；
- 不加入额外的人工关系标签或模型生成关系标签；
- 任务仍然是单技能路由；
- 结论仅限于搜索效率、分支／候选召回率和早期排除失败。

不能把它描述为“已经解决关系感知技能路由”的证据。

## 18. 创新性评估

最接近的工作构成了真实的研究重叠风险：

- [SkillRouter](https://arxiv.org/abs/2603.22455) 表明完整技能正文可能具有决定性作用，并提出了大规模先检索、后重排序的路由器。
- [SSL](https://arxiv.org/abs/2604.24026) 提出 Scheduling-Structural-Logical 表示，并评估结构化技能发现和风险评估。
- [Tool-DE](https://arxiv.org/abs/2510.22670) 使用结构化字段扩展工具文档，并分析各字段的独立贡献。
- [ToolRet](https://aclanthology.org/2025.findings-acl.1258/) 表明，通用信息检索能力并不保证良好的 capability retrieval 表现。
- [SkillRet](https://arxiv.org/abs/2605.05726) 提供一个包含标签、taxonomy 和检索训练数据的大规模公开技能 benchmark。
- [Skill Retrieval Augmentation](https://arxiv.org/abs/2604.24594) 将更广泛的流水线分解为 retrieval、incorporation 和 application。
- [SkillNet](https://arxiv.org/abs/2603.04448) 通过 ontology 和丰富关系组织技能。
- [Task Decomposition-Guided Reranking](https://arxiv.org/abs/2607.06283) 使用子任务／状态分解，以及 DAG 风格的技能重排序框架，并进行下游环境评估。

论文不能声称：

- 首个结构化技能表示；
- 首次为 capability retrieval 进行字段扩展或字段消融；
- 首个先检索、后重排序的技能路由器；
- 首个大规模技能 benchmark；
- 首个技能图、层级或 DAG 表示；
- 七个操作性字段具有普适充分性；
- I3C 是普遍优越的表示。

可以辩护的候选创新点是：

> 对单技能、执行前路由进行一种受控且以字段为依据的评估：在刻意构造的近邻技能混淆下，分别隔离操作性事实内容、明确字段组织、信息稀释、第一阶段候选召回和条件重排序。

更具体地说，贡献来自以下组合：

1. 使用 RQ1 得出的操作性差异，而不是通用元数据类别；
2. 使用事实相同的 matched-content controls；
3. 明确分离候选生成失败与 reranker 失败；
4. 分别操纵无关技能规模与近邻密度；
5. 使用摊销后的离线／在线成本模型；
6. 进行有源文档证据支撑的提取保真度分析。

在最终论文完成最后一次系统性文献检查之前，不能使用“first”一词。

## 19. 研究问题评估

| 标准 | 评估 | 原因 |
|---|---|---|
| 重要性 | 高 | 技能库正在扩大，而仅靠主题匹配无法可靠解决近邻技能的适用性区分。 |
| 内部连贯性 | 高 | RQ1 识别有用信息；RQ2 检验系统如何暴露并利用这些信息。 |
| 可回答性 | 范围受控时为高 | 主要变量可以利用现有 clusters 和技能库 artifacts 进行操纵。 |
| 创新性 | 中等至较强的诊断性创新 | 相关工作已经涵盖完整正文、结构化层、文档扩展和重排序；创新来自因果隔离和 matched controls。 |
| 可行性 | RQ2a 高；RQ2b 尚未作为获批协议评估 | 现有 RQ1a 数据和 selector 组件足以支持 RQ2a；RQ2b 仍未审阅。 |
| 外部有效性 | 中等 | 公开原始技能和可选外部 SkillRouter 数据有所帮助，但受控 clusters 仍然是合成的。 |
| 风险 | 可管理 | 主要风险是 provenance、提取错误、public gold 歧义和过宽主张。 |

如果把图／树构建、新的公开 benchmark、完整 80K 技能神经检索重跑、多种 rerankers 和大规模下游执行都设为必做，研究问题就会变得不可行。

## 20. 可行性与工作量估计

### 已经具备

- 350 个 RQ1 受控 clusters 和 750 个 prompt 变体；
- frozen-v0.4 本地 benchmark；
- BM25 和 Qwen 检索 runners；
- Qwen 和 SkillRouter 风格的重排序基础设施；
- I1、I2、I3H 和本地 I3M artifacts；
- 完整的外部 79,141 行 I3C V2；
- 当前结果汇总与失败模式工具。

### 缺失的 RQ2a 关键工作

- 确定性的 RQ2a same-facts fielded／flat／prose／order／dilution serializers；
- 表示等价性 validator；
- 固定候选 RQ2a runner 或 adapter；
- 从 M6-v2 组件改造得到、无泄漏的 RQ2a 语义 field-aware adapter；
- RQ2a 成本与延迟 ledger；
- 验证性统计脚本；
- 更新论文表格和结果解释。

### RQ2b 当前工作状态（协议已冻结，执行按阶段审批）

- 来源、prompt、provenance 与 legacy-drift audit：`COMPLETE / PASS`；
- B0F 科学协议：`COMPLETE / USER-APPROVED`；
- B1X I3C 传输包：`COMPLETE / 2,433 ROWS / 57 CHUNKS / UNTRANSMITTED`；
- B1S 本地 I1／I2 与流水线实现：`PRE-V1.1/PRE-A2 SCOPE COMPLETE / V17 SMOKE PASS / 独立 PASS 13 合格 / IMPLEMENTATION SEAL VERIFIED`；v1.1 strict schemas、BM25 serializer、shared rerank aggregator、strict analysis binding 及其 synthetic smoke 均为 `COMPLETE / ZERO NETWORK / NOT SCIENCE`。首次 v1.1 独立审查失败，rank／binding／reporting／finite-score 缺陷已在本地修复；新的独立复审无 P0/P1，狭义 strict-contract seal 已完成。Qwen／SkillRouter adapters 是之后 B1/B2 的独立要求；
- V3 I3C integrity：`AUTOMATIC INTEGRITY FROZEN / 2,433 ROWS / 57 CHUNKS`；在整块 root-coverage 修正后，冻结报告重放 source hash、exact evidence、heading exclusion、identity、serialisation、root coverage、duplicate observation 与 scaffold lint。V3 的 120-row manual-QA 尝试因协议不足被 quarantine 且不计分；用户明确不再进行替代盲审，因此这不是独立语义完整性声明；
- B1L local BM25：`COMPLETE / POST-RUN INTEGRITY VERIFIED / USER RESULT REVIEW REQUIRED`；获批 packet `caf10c...e8ec` 与 receipt `def03cd...f255` 已生成四个 V3 绑定的 2,433-row indexes，以及 381 条 prompts 的 1,524 条 strict rankings。每条 Top-100 均已持久化；独立 verifier 重新验证全部 rows 和全部 1,524 个 disk-index replays（`3ec257...77cc`、`029b80...3506`）。这只是本地 lexical baseline：没有 network、external API、embedding、reranking、provider call 或 thesis-result writing；
- embeddings、reranking 与最终 cost ledger：`NOT STARTED / NOT AUTHORISED`。

### 预计计算规模

- RQ2a 核心：三个核心选择器合计约 27,000 个 query-candidate 分数，另加 field-aware 必须对比的 1,800 个候选分数；
- RQ2b 文档 embeddings：最多 4 x 2,433 = 9,732 个文档表示，可在所有查询之间复用；
- 本地主要 prompts：389 个 controlled 加 public-gold 查询，另有 12 个 stress prompts 单独处理；
- 两个第一阶段、四种表示下的 top-20 reranking：在分阶段缩减之前，最多 62,240 个 query-candidate pairs；
- 在敏感性运行中只重排 I2／I3C，可将高成本部分减半。

只要缓存 embeddings、分阶段运行条件，并确保可选的外部／下游／图扩展不阻塞核心工作，该方案在 honours thesis 范围内可行。

## 21. 有效性威胁与缓解措施

| 威胁 | 后果 | 缓解措施 |
|---|---|---|
| 合成的受控语言 | 规则性和词汇重叠被夸大 | 将 public-original RQ2b 分开；独立报告 controlled 与 public strata。 |
| Public gold 歧义 | 产生假阴性 | 同时使用 strict 和 acceptable gold；记录操作适用性理由；尽可能裁决。 |
| 提取幻觉／遗漏 | I3C 效果与提取质量混杂 | 精确 evidence 验证；允许稀疏字段；使用人工修正的分层子集。 |
| I3C 格式偏好 | 某个模型可能偏好 Markdown／JSON | 使用事实相同的 flat／prose controls；在 BM25、dense 和 cross-encoder 下复现。 |
| 信息长度混杂 | 较短文档可能看似更好 | Matched-content controls、token 报告、稀释曲线、按长度分层分析。 |
| 字段顺序偏差 | 较早字段得到不成比例的注意 | 使用平衡顺序诊断。 |
| 查询泄漏 | Prompts 重复精确字段措辞 | 使用 direct 和 paraphrase strata；不能根据被评估的序列化文本生成查询。 |
| Target-field oracle 泄漏 | Field-aware selector 被告知应优先考虑哪个 suite 或字段 | 只提供原始 query 和候选的七个字段；统一使用一个在 development clusters 上冻结的 target-agnostic 聚合规则。 |
| 候选集漂移 | Reranker 比较不公平 | 在重排序之前持久化候选身份和分数。 |
| 截断 | 较长 I2 或 I3C 文本静默丢失证据 | 记录模型限制；只有在冻结策略下才允许分块／聚合；报告截断率。 |
| Provider／模型漂移 | 结果无法复现 | 记录模型标识、日期、API 设置、代码 hash 和 cache key。 |
| 将重复 prompts 当作独立样本 | 置信区间过窄 | 使用 cluster-level inference。 |
| 成本测量不一致 | 产生误导性效率结论 | 分离冷／热缓存、离线／在线、检索／重排序／执行。 |
| 研究者设计表示 | 确认偏差 | 评分前冻结 serializers；保留零结果和负结果。 |

## 22. 质量关卡

### Gate 0：冻结协议

- 批准 RQ 的精确措辞；
- 批准核心与可选实验的边界；
- 冻结主要比较和指标；
- 设计变更期间不得查看验证性结果。

### Gate 1：来源 provenance

- 每个技能只有一个获批 I2 来源；
- 使用公开原文，而不是 wrappers；
- 技能身份与 hash manifest 完整；
- 声明 benchmark 版本。

### Gate 2：I3C 提取

- 2,433/2,433 行身份对齐；
- 100% JSON 解析成功；
- 重复或缺失 skill IDs 为零；
- 精确验证源文档 evidence；
- 允许并记录空字段；
- 冻结提取 prompt 和 schema 版本。

### Gate 3：matched-content 等价性

- same-facts-fielded、same-facts-flat 和 same-facts-prose 携带完全相同、经过审阅的字段值命题；
- 任何 serializer 都不能创造或遗漏事实；
- 字段标签／顺序是唯一预期的结构变化；
- 稀释填充不能包含可区分同族技能的线索。

### Gate 4：候选身份

- 所有表示条件使用相同候选 IDs；
- 保存确定性的顺序随机种子；
- 验证 gold 和 acceptable alternatives。

### Gate 5：runner 可复现性

- 保存查询和文档 caches；
- 记录模型与截断设置；
- reranker 使用已持久化的第一阶段列表；
- RQ2a field-aware selector 看不到 target-field、gold、role 或 alternative metadata，并使用一个冻结的聚合规则；
- 完整运行前通过 smoke tests。

### Gate 6：分析可复现性

- 保留逐行结果；
- aggregation script 能重新生成每张表；
- 冻结 cluster bootstrap 和多重比较规则；
- 不能混合 strict 与 acceptable 指标。

## 23. 停止规则

满足以下条件时，停止扩展实验：

- RQ2a 核心矩阵、必须的 field-aware 对比和必须复现的条件已经完成；
- RQ2a 成本 ledger 和失败分解已经完成；
- 在已声明的敏感性检查下，结果结论保持稳定。

RQ2b 已有冻结的 canonical 停止规则，覆盖来源 hashes、selector-visible leakage、无损分块覆盖、不可变候选集、外部调用上限、checkpoint 有效性与完整矩阵分析。B0F 已批准，B1X 已在零传输状态完成，B1S 本地 smoke 已通过；在独立审查、seal 与逐阶段授权全部通过前，不得开始科学性运行。

除非某项新增实验能够解决一个明确、尚未解决的主张，否则不要加入图／树、ToolRet transfer、另一个 reranker、另一个 embedding 模型，或一次 80K 技能神经检索重跑。

如果出现以下情况，停止托管运行：

- 源文件或表示 hash 与 manifest 不匹配；
- 进度日志无法识别当前正在运行的条件；
- embeddings 被重新计算，而不是复用；
- 每个条件完成后没有 checkpoint 结果；
- 预计剩余成本超过批准预算。

## 24. 必需 artifacts 与交付物

当前 RQ2a 交付物：

1. RQ2a 协议 manifest。
2. Same-facts fielded／flat／prose／dilution serializers。
3. 表示等价性 QA 报告。
4. RQ2a development／test cluster manifest。
5. BM25、Qwen single-vector、cross-encoder 和 field-aware Qwen 的固定候选逐行排序结果。
6. Field-aware 聚合 development 报告和冻结规则。
7. 成本与延迟 ledger。
8. Cluster-bootstrap 与敏感性分析报告。
9. 包含精确 query／skill evidence 的失败模式示例。
10. 可直接用于论文的 RQ2a 方法与结果表格。
11. 主张边界与局限性表格。

RQ2b 已批准协议下的交付物；具体执行仍按阶段审批：

1. 带有提取 QA 的本地 I3C JSONL。
2. RQ2b I1／I2／I3C／I3-flat serializers。
3. 完整技能库逐行检索结果。
4. 持久化的 top-5／top-20／top-50 候选文件。
5. Reranker 逐行输出。
6. 嵌套 scale／confusability manifests。
7. 可直接用于论文的 RQ2b 结果表格。
8. 可选下游验证附录。

## 25. 论文章节结构

### 方法论

1. RQ2 范围及其与 RQ1 的关系。
2. 源语料库与 provenance。
3. 表示构建。
4. RQ2a 固定候选设计。
5. RQ2b 先检索、后重排序设计；只有在对应阶段另行授权后才执行。
6. Gold 与歧义规则。
7. 指标、统计和成本模型。
8. 次要下游验证。
9. 有效性威胁。

### 结果

1. 表示完整性与 token 统计。
2. RQ2a matched-content 结果。
3. 字段特定和选择器特定的交互。
4. 稀释与顺序诊断。
5. RQ2b 第一阶段候选召回，仅在该阶段另行授权、完成并经用户审阅后加入。
6. 条件重排序与端到端准确率，仅在 RQ2b 完成后加入。
7. 无关规模与近邻密度，仅在 RQ2b 完成后加入。
8. 准确率、上下文和延迟的 Pareto 分析。
9. 提取保真度与失败分析，仅在 RQ2b 完成后加入。
10. 次要下游验证，如最终保留。

### 讨论

1. 收益是由操作性内容还是明确结构解释。
2. 什么时候完整文本值得其成本。
3. Reranking 在哪里有帮助，以及第一阶段召回在哪里占主导地位。
4. 哪些 RQ1 字段需要推理能力更强的选择过程。
5. 对技能作者和路由系统设计者的启示。
6. 为什么关系感知图路由仍属于未来工作。

## 26. 主张纪律

如果结果支持，可以提出以下主张：

- 与紧凑元数据相比，所研究的操作性事实改善近邻路由；
- 在 matched-content 下，明确字段组织可能增加价值、没有效果，或只对特定模型有效；
- 完整文本和结构化事实处于不同的准确率－成本位置；
- reranking 无法补救第一阶段缺失的候选；
- 近邻密度和无关技能库规模产生可区分的失败模式；
- 提取保真度为结构化表示性能设定上限。

禁止提出以下主张：

- 已经识别所有与路由相关的信息；
- I3C 总是优于完整文档；
- 结构化字段是唯一正确的技能表示；
- 在没有运行关系敏感测试的情况下，声称图／树方法更差；
- 路由改善即可证明任务执行改善；
- provider 定价的货币成本跨时间稳定；
- 不完整的外部神经检索结果行构成完整比较。

## 27. 批准状态与剩余决策点

RQ2a 的下列设计决策已经完成审批并用于最终实验：

1. RQ2 的精确措辞；
2. 将 RQ2a／RQ2b 作为同一个 RQ2 的子研究，而不是新的正式 RQ3；
3. 使用 Qwen embedding 作为 RQ2a 主要选择器；
4. 所选择并冻结的 cross-encoder reranker；
5. 20/80 cluster 划分；
6. 将 same-facts-fielded、same-facts-flat、same-facts-prose 和 same-facts-diluted 设为核心 matched controls；
7. RQ2a field-aware adapter 的要求，以及在 development split 上从 maximum 与 uniform top-two aggregation 中选择一个并冻结；
8. 下游执行只作为次要验证；
9. 图／树和外部 80K 神经检索重跑只作为可选／未来工作。

RQ2b 的语料库、表示定义、第一阶段方法、reranker、指标与成本协议已在 B0F 冻结。该批准不自动授权 I3C 原文传输、Qwen API、hosted SkillRouter 或 thesis 结果写入；这些仍是 canonical RQ2b ledger 中彼此独立的后续 gate。

## 28. 最终评估

该 RQ2 足以支撑一篇有雄心的 honours thesis，因为它提出了一个清晰的机制问题，并在实际检索流水线中验证答案。它的创新性属于诊断性创新，而不是架构创新：它并不发明首个结构化技能 schema 或路由器，但能够辨别观察到的收益分别来自操作性内容、明确组织、较少的信息稀释、候选召回，还是重排序。

RQ2a 可以利用经过审阅的 RQ1a clusters 和现有 selector 组件完成。当前阻塞项是 matched-content serializers、等价性 validator、固定候选 adapters、field-aware adapter，以及协议冻结。只有在 RQ2b 日后获批时，provenance 正确的本地 I3C 提取才会成为阻塞项。论文不应直接进入另一轮宽泛的 I1／I2／I3 矩阵。RQ2a 的零结果同样有信息价值：如果 fielded、flat 和 prose 变体等价，则说明保留事实比字面字段组织更重要；如果 field-aware selector 没有增益，则说明在被测试的聚合规则下，明确分段本身并不充分。
