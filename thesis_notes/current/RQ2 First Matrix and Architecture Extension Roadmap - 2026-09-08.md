# RQ2：先完成核心矩阵，再扩展架构，最后设计小系统

Date: 2026-09-08

Status: APPROVED_RESEARCH_PLAN / V7_BENCHMARK_FROZEN / LOCAL_PHASE7_PREPARATION_STARTED

> 正式主计划：`RQ2 Approved Research Plan - 2026-09-08.zh-CN.md`，以及 `skill_benchmark/rq2b_naturalistic_confusability/preparation/rq2_approved_research_plan_2026_09_08_v1/plan_freeze.json`。研究者已要求本版定稿。当前是 3,798 候选上的全库检索，不只是 cluster 内选择；约 20,000 个额外 background sources 的 nested scale-out 属未来，不是当前候选准入或必做矩阵。不能提前宣称大规模 scalability 已验证，也不能假定 graph/pure LLM 不可扩展。

> 本地准备进展：I1 3,798 行、byte-exact I2 3,798 行已生成并机械 replay；详见 `skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_2026_09_08_v1/`。I3C/I3-flat、语义 QA、dependency/exposure 与 runtime/预算 seal 仍待完成；没有执行 selector。

## 1. 本轮决定与已经完成的部分

用户明确要求将 V7 已完成冻结合并到 GitHub main，并采用以下顺序：核心矩阵 → wiki/graph/tree 可行性与扩展 → 自研小系统。现有 ECR 草案是候选设计，不是先跑核心矩阵的前提。

远端同步后，实际 final-freeze 来源为 `codex/rq2b-v7-sealed-coordinator-reconciliation` 的 `fad26f1673afb5d5c15b29a0bfc1d9bd4d9d5c6e`。它包含原 main `2a5f54172a01e4f5c566b0d97bdae1c1b6bcbf59`，可 fast-forward；不需要覆盖、squash 或改写审查历史。早先原 checkout 停在 `a95bd97` 所造成的“未找到 1,077 freeze”不代表审查未完成。

本轮 exact replay 已确认：

| 冻结对象 | 实际值 |
| --- | --- |
| V7 原审查范围 | 1,226 prompt groups |
| 最终保留 | 1,077 prompts/groups；不是 1,077 个独立 source clusters |
| 已知 acceptable 分区 | 881 strict singleton；196 multi-acceptable |
| 保留范围分层 | 714 NC；363 parent-delta |
| 排除/延期 | 149：108 no acceptable main、18 external singleton、22 positive-tail gate、1 U0323 |
| 候选源库 | 3,798 source-hash-unique primary Markdown documents |
| 审查主池/尾部 | 原 V7 K=6 / two-tail 合同不变 |
| 528-group successor | deferred，不能混入本轮结果 |

权威 final package：`skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/`。

- Final prompt manifest SHA-256: `3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128`。
- Final integrity report SHA-256: `f77df13f55fd151a2831ba448c6efa4bf760942f9e925f837eeb9a365c8eed4a`。
- Source union SHA-256: `5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b`。

标签冻结与运行输入冻结分开：前者已 PASS，后者尚需四表示 materialisation/QA、执行 root 与预算 seal。不要再次重开 acceptable-set 审查，也不要把这个准备状态报告成已经跑出 V7 结果。

## 2. First matrix：只做已确定的主问题

| 轴 | 首轮范围 |
| --- | --- |
| 表示，4种 | I1 discovery、I2 original、I3C fielded、I3-flat matched facts |
| First-stage，3种 | BM25、Qwen generic dense、SkillRouter dense |
| 排序末端，3种 | 原始顺序、Qwen reranker、SkillRouter reranker |
| 总量 | 12 first-stage runs，产生 36 个端到端配置；不重复召回来冒充更多实验 |

完成 36 配置后，再做 6 个 fixed-candidate bridge 配置：固定 B05（I2 + Qwen dense）的候选列表，改变 reranker 可见表示；I2 的两个配置复用 B05-GQ/GS。它帮助区分“没找回来”与“找回来了却排错”，但不能替代端到端召回评价。

候选生成面向全部 3,798 sources，不局限于六个审查候选。审查 K=6 和拟继承的运行时 Top-20 是两个不同概念。未审候选仍为 unknown，不是错误标签。

新准备包生成了机器可读的 36+6 condition manifests，但 `execution_authorised=false`：

`skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1/`

模型具体身份、tokenizer/window policy、语义 QA 和 compute/transfer 预算仍须执行前绑定；这里不从旧 alias 自动推定当前服务完全相同。完整定稿、结果解释和未来 scale-out 边界见 `RQ2 Approved Research Plan - 2026-09-08.zh-CN.md`。

## 3. 文献不是只有 skill papers：按设计问题组织

现有仓库基础包括 `thesis_notes/literature/Comprehensive Related Work Sweep - 2026-06-26.md`、`thesis_notes/literature/Reranking and Skill Retrieval Literature Refresh 2026-05-25.md`、`thesis_latex/chapters/02_literature_review.tex`。本节是这些材料的设计映射，不宣称已经完成对所有近期论文的系统综述。以下主来源页面于 2026-09-08 重新核对；跨任务迁移是本 thesis 的设计推论，不是原论文已经证明 skill routing 有效。

| 文献线 | 对我们有什么用 | 不能直接照搬什么 | 本轮位置 |
| --- | --- | --- | --- |
| [DPR](https://arxiv.org/abs/2004.04906)、[BEIR](https://arxiv.org/abs/2104.08663) | dense candidate generation；异质任务上保留 lexical 强基线和效率分析 | passage QA 排名不等于 skill adequacy；BEIR 是 benchmark，不是另一个 selector | 支撑首轮三类 first-stage 选择与限制 |
| [ColBERT](https://arxiv.org/abs/2004.12832) | token-level late interaction 说明信息匹配不止单向量 | 现有 Qwen chunk-max 不等于 ColBERT；不同 checkpoint 不构成纯结构消融 | 分析与未来 baseline，首轮不临时加一整轴 |
| [ToolRet](https://arxiv.org/abs/2503.01763) | 最近的 tool retrieval 评价问题；把通用相关性与工具选择需求分开 | ToolRet 的 benchmark 不能当作待复现的一套架构；tool/API 与完整 skill 文档不同 | 强化缺口与外推边界 |
| [ToolRerank](https://aclanthology.org/2024.lrec-main.1413/) | adaptive truncation 与 hierarchy-aware reranking 提供候选组织/截断的对照思路 | multi-tool diversity 不自动适合单 skill 近邻辨别；我们没有声称复现该方法 | 分析、后续小系统与截断诊断 |
| SkillRouter（仓库 pinned checkpoints）、[Skill Retrieval Augmentation](https://arxiv.org/abs/2604.24594) | 最近的 skill-specialised retrieval，以及 retrieval/incorporation/end-task 分阶段评价 | routing 命中不能证明 downstream execution success；模型训练来源仍是限制 | SkillRouter 进入核心；执行阶段只讨论边界 |
| [Adaptive-RAG](https://aclanthology.org/2024.naacl-long.389/)、[Self-RAG](https://arxiv.org/abs/2310.11511) | 何时多花一次检索/推理成本、证据是否足够 | 前者有复杂度分类器，后者有训练/反思 token 机制；随便加一句 prompt 不叫完整复现 | 后续有预算上限的检索策略设计 |
| [RAPTOR](https://arxiv.org/abs/2401.18059)、[GraphRAG](https://arxiv.org/abs/2404.16130) | 树摘要和 source-derived graph/community structure 改变证据组织 | 长文 QA 或全局总结的收益不保证近邻 skill 选择收益；摘要可能丢掉否定/边界 | 核心后适配 feasibility，不称现有四表示包含这些架构 |
| [LLM-Wiki](https://arxiv.org/abs/2605.25480)、[ReAct](https://arxiv.org/abs/2210.03629) | 可读页面/链接、search/read/follow 与根据新观察决定下一步 | Wiki 编译、交互与自我修正是多个变化，不是单纯 representation；ReAct 不是直接可替换的 retriever | 与静态表示、控制策略分开评价 |

需要补强的是每篇文献到“我们采用/没有采用什么、为什么”的连接，以及最近邻工作的公平适配，而不是用论文数量代表 literature review 足够。原研究成绩、数据规模、信息字段不能跨任务挪作我们的结果。

## 4. Agentic RAG：可以考虑，但先限制在 retrieval

概念上分开两件事：wiki/graph/tree 是证据如何组织；agentic policy 是何时检索、再读哪里、何时停。二者可以组合，也可以独立存在。一次 LLM reranking 本身不构成有新观察反馈的 agentic loop。

后续小系统最小候选范围：请求 → 初始候选 → 检查输入/输出/前提/边界的证据 → 如有信息缺口，进行有上限的 search/read → 停止并输出 skill ranking。它只读冻结源库，不执行 skill、不操作外部服务、不引入多 agent 分工、不让会话记忆带入其他测试题答案。保留显式动作、源引用、停止原因和费用记录，不要求获取模型隐式思维链。

只有进入该扩展时才冻结具体最大轮数、总 tokens、失败回退和停止规则。比较必须至少有同模型的固定流程基线，报告实际多花的 calls/tokens/latency；“agentic 更贵所以更准”不是免费的机制解释。先固定候选测试额外阅读，再把可重检索的完整流程作为另一项对照，避免把更好召回误认为更好推理。

不在本 thesis 的当前 endpoint 上评估完整 agent skill system：技能执行、环境成功、恢复重试和多技能组合会需要新的任务与执行 gold。若将来做，只能另立问题，不由当前 acceptable-set Hit@1 推出执行有效。

## 5. 架构扩展与自研的准入/退出

1. 核心 B+C 完成并通过 valid-run QA；不根据输赢删掉配置。
2. 对 wiki/tree/graph 做一页 evidence/input/cost mapping，先判断是否需要新关系或额外源资料，再选择有限适配。无需承诺三个完整系统都实现。
3. 所有节点/摘要/边来自允许的源材料；benchmark clusters、targets、acceptable sets、review rationales 和 `confusable_with` labels 不能用于索引或图边。
4. 对 source-only 编译后的摘要/关系做 fidelity QA；复用模型/候选时明确复用条件，新 evidence 时明确 whole-pipeline effect。主评测不跨 query 自我修改 Wiki；若研究在线 self-evolution，另开顺序/记忆/污染协议。
5. 小系统按核心失败证据选择一个有限机制，例如 constraint checking 或 adaptive evidence reading；此前 ECR 只是草案。实现失败、无优势或不做均可退出，不影响核心比较研究交付。
6. 如果设计看过本轮 V7 结果，再在 V7 测试是 exploratory 内部评价。要作独立 confirmatory claim，需要新的 source-disjoint 未见过评价范围；不通过改称版本或重新划分旧题清除 exposure。

## 6. 现在具体还差什么

- 已完成：final acceptable-set replay；3798 primary sources 可移植性；36+6 机器可读规划；原文 SHA 全匹配；旧 return/label 没有修改。
- 接着做：V7 全量 I1/I2/I3C/I3-flat materialisation 与 master-SOP QA，dependency/exposure ledger，准确模型/窗口/统计和预算的 execution seal。
- 然后才开始核心模型运行；本轮没有 retrieval、embedding、reranking、provider call、新 adequacy 判断或 V7 metrics。

3,167 个原文补齐约束来自冻结的 source resolution ledger，不是扩库。总 source bytes 为 19,662,831。只提交这些精确 primary Markdown，不把 cache、模型权重或原工作目录其余未跟踪文件顺手纳入。

主文暂不改成新实验已完成，也不更新 thesis PDF 结果。此 roadmap 是推进顺序与准备记录，不是实验发现。
