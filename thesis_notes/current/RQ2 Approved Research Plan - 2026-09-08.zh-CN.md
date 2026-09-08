# RQ2 正式研究计划：语义混淆下的全库技能路由

日期：2026-09-08  
版本：rq2-approved-research-plan-v1  
状态：`FINAL_APPROVED_RESEARCH_PLAN / LOCAL_EXECUTION_PREPARATION_STARTED`  
目的：一份即使不开发新系统、或新系统没有胜出，也能独立完成研究问题的实验设计。

本文件由研究者于 2026-09-08 明确要求正式定稿，成为新 RQ2 的主研究计划；它取代 discussion-spec-v2 的规划地位，不回写历史 RQ1/RQ2a/V3 结果、master SOP 或 V7 benchmark/label freeze。当前必做范围为 B36+C6、P1–P5、§10–14 的指标/统计/解释规则。§8 的 ECR 是可退出设计草案，wiki/graph/tree 与约 20,000 个额外 background sources 属未来扩展，不是当前必须运行的条件。计划已批准，不再作为待逐项审批的草稿；具体 runtime root、模型/窗口可用性、源传输与预算仍须按 master SOP 绑定后启动正式 selector。

## 0. 先说结论

正式计划把贡献放在三个可以分别成立的层次：

1. **信息证据**：RQ1 判断哪些操作信息在规定条件下有区分价值，不宣称七个字段是新发明或具有普适排名。
2. **方法评价**：RQ2a 隔离表示与信息利用机制；RQ2b 检验这些能力进入完整库后是否仍成立，以及代价、失效位置和适用条件。这是必须能独立完成的核心。
3. **可选方法**：实现一个小型操作约束感知路由器，检验一个有限假设。有效、无明显优势、明显退步，均如实报告；未通过实现有效性检查，则不能当作算法的负面科学结果。

不把“提出新系统且必须比所有系统好”写成 thesis 成立条件。也不把任何失败都包装为贡献：只有实验有效、反例可复现、解释有证据并能限定既有假设时，负结果才有研究价值。

冻结核心规模：36 个端到端配置 + 6 个新增固定候选诊断配置，共 42 个新配置。SSL-style 比较、既有 field-aware 迁移、小系统分别是可退出模块；不要求把所有扩展交叉成巨大矩阵。

用户本轮确定的顺序：先完成 B 的 36 配置，再做 C 的 6 个诊断；随后依据文献与可行性评估 wiki/graph/tree 扩展，最后设计可退出的小系统。下文 ECR 只是候选设计，不是必须先于主矩阵实现的任务。若小系统设计已受到本轮 V7 结果影响，其 V7 评价应标 exploratory；不能继续声称未见过这些结果。

## 1. 研究问题与可回答边界

### 1.1 总 RQ2

> 在语义相近但操作要求不同的技能选择中，不同技能表示与路由机制如何影响选择质量，并产生什么准确性、上下文与计算成本权衡？

正式英文研究问题：

> How do skill representations and routing mechanisms affect the selection of operationally suitable skills under semantic confusability, and what accuracy–context–cost trade-offs arise?

### 1.2 两个相互支持、不能混为一个实验的部分

| 部分 | 保持不变/引入的困难 | 问的是什么 | 不证明什么 |
| --- | --- | --- | --- |
| RQ1，保留已完成结论 | 配对暴露/移除特定操作信息 | 这些信息在规定干预下有没有区分价值？ | 所有模型都需要显式字段；全球字段重要性排名 |
| RQ2a，保留已完成 matched-content 研究 | 同一请求、同一三成员候选、同一组 reviewed propositions | 同样信息怎么表达、怎么使用，能否影响辨别？ | 完整库召回、真实执行成功 |
| RQ2b，本稿主要新执行范围 | 完整冻结库；候选不保证出现；长度、成本与未审候选问题 | 信息价值能否经受完整库的检索和重排？ | 开放世界通用最优、多技能工作流执行成功 |

RQ2b 包含普通 lexical/dense baseline，不要求每种方法显式消费七个字段。原文与 embedding 可能隐式携带同样信息；是否利用成功由实验判断。

### 1.3 四个 analysis questions

- AQ1：源生简述、完整原文、抽取事实、事实的显式字段组织，各自保留了什么选择价值？
- AQ2：失败发生在候选生成，还是正确/可接受候选已出现后的排序？
- AQ3：哪类方法更能避免“主题像，但输入、输出、前提或边界不适合”的选择？
- AQ4：质量变化需要多少离线处理和在线开销，何时值得？

新系统只增加一个 optional question：在相同候选、模型与源证据下，显式核对请求约束是否优于一般相关性评分？


### 1.4 规模是动机与待验证维度，不是提前成立的结论

当前研究并非只在一个三成员 cluster 内选择：RQ2a 隔离局部混淆，RQ2b 则对同样来源的请求在 **3,798 个候选**中检索，再按固定候选预算排序。1,077 是 query/group 数，3,798 是候选库大小，K=6 是标签审查主池大小；三个数字不能互换。

| 范围 | 定稿中的地位 | 能作的结论 |
| --- | --- | --- |
| 当前 V7，3,798 candidates / 1,077 queries | 必做 B36+C6，保持 frozen sources 与 labels | 指定库规模上的质量、信息负担、成本和失败位置 |
| wiki/graph/tree 与可选自研小系统 | 核心之后的有条件扩展 | 只有执行并验证后才有架构/机制结果；不做也不影响核心完成 |
| 额外约 20,000 background sources 的 scale-out | 明确 FUTURE / NOT_EXECUTED / NOT_IN_CURRENT_MATRIX | 未来测库规模增长时质量–成本曲线；现在不作数万级 scalability claim |

论文可使用“面向增长中的技能库的检索问题”作为动机。当前结果措辞应是“在受测规模下的全库技能路由”，不能写成已证明 large-scale scalability，更不能仅因当前规模未达数万就判某方法 not scalable。

“直接把库放进 context”是有效的替代思路，不应先行排除。但源数量不等于 token 数，完整原文与简述也不等价；能装入窗口不等于准确、便宜或低延迟。长上下文位置效应与 RAG/long-context 的质量–成本交换已有研究，但它们不是当前 skill benchmark 的结果。[Lost in the Middle](https://arxiv.org/abs/2307.03172)、[RAG or Long-Context LLMs?](https://arxiv.org/abs/2407.16833)

纯 LLM 全库逐项打分、一次全库 in-context 选择、检索后 Top-20 LLM 重排是三种不同方案；不能都归为“pure LLM 不可扩展”。同理 graph 的离线构图成本和在线局部检索成本分开测，不能预设 graph 一定不适合大规模。

## 2. 证据状态与冻结边界

### 2.1 已完成远端同步后的实际核验

初读时原工作目录停在 `a95bd97`，没有同步后续远端提交；不能把该 checkout 的缺失说成最终 freeze 未完成。同日 fetch 后，在保留原目录未提交文件的干净 main worktree 中核验 `fad26f1673afb5d5c15b29a0bfc1d9bd4d9d5c6e`。V7 final-freeze verifier 与上游 acceptable-set audit verifier 均 replay PASS。较早“找不到 1,077 closure”的表述已由本节明确纠正。

| 对象 | 本次核对到的状态 | 本稿如何处理 |
| --- | --- | --- |
| RQ2a matched-content | canonical analysis 记录 350 source clusters，70 development / 280 confirmatory clusters；600 confirmatory prompts、22 conditions、13,200 aligned rows | 保留历史冻结与结论，不因新方法而重写或重新称为 untouched test |
| 旧 RQ2b V3 | tracker/protocol 记录 2,433 candidates、381 strict prompts、四表示/三 first stages/两 rerankers 已完成 | 只作历史证据与可复用实现，不复制为 V7 结果 |
| V7 audit package | 当前用户指定的 operative library/audit lineage | 继续采用，不切换到 deferred 528-group successor |
| 1,077-group acceptable-set freeze | final prompt manifest、排除账本、amendment、完整 verifier replay PASS；881 strict、196 multi-acceptable，149 excluded/deferred | **已验证的 canonical 范围**，不重新开启审查 |
| V7 source union | 3,798 个 source-hash-unique primary Markdown；原目录全部 hash 匹配；干净 checkout 补齐 3,167 个缺失文件后全量 replay PASS | 仅补齐已绑定的原始 bytes，不增加 library 成员；辅助资源/许可 byte replay 单独说明 |
| master SOP | 2026-09-05 文本可读取，规定 Phase 7 表示 QA 与 Phase 8 根冻结 | 保留其非冲突质量门槛；用户后续 V7 scope amendment 必须一同绑定 |

结论是 **benchmark/acceptable-set 已冻结；V7 全量四表示与运行输入的 seal 尚未完成**。下一步是 Phase 7 表示 QA、Phase 8 execution-root 与具体预算/模型绑定，而不是重新审 1,077 组。禁止拿 528 或 V3 的文件凑成 V7 runtime。最终 prompt manifest SHA-256：`3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128`；source union SHA-256：`5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b`。准备包与复现命令见同目录的 `RQ2 First Matrix and Architecture Extension Roadmap - 2026-09-08.md`。

### 2.2 不可变规则

1. V7 原始 manifest、K=6 main、两个 sealed tails、returns、reissue、coordinator、排除记录永远保留。
2. 用户已决定的 U0323 defer/exclude 保留；不为本稿或新系统重新打开。
3. 528-group successor 保留但 deferred；本轮结果不覆盖其新增项。
4. 本稿没有重新筛题、改 prompt、改 acceptable sets 的授权；新方法不能影响 benchmark 准入。
5. `K_audit=6` 是审查主池大小；`k_route=20` 是拟继承的运行时重排候选预算；两者用途不同。全库检索不是只在六个审查候选里挑答案。
6. 未审候选不是负例；bounded audit 的 singleton 不是全库唯一正确性的证明。
7. 不使用 cluster membership、target、acceptable labels、review rationales、tail proposal rank 或 benchmark-derived `confusable_with` 边来构造任何 selector 输入。

### 2.3 执行前必须绑定的数据

- 一个 source-hash-unique candidate manifest 和源文件/许可/provenance hashes。
- V7 final prompt inventory；逐行有 `prompt_id`、lineage、origin、stratum、dependency_group、文本 hash。
- `A_q`：已审的 fully acceptable candidates；`J_q`：已有有效最终判断的候选；每条判断的 lineage。
- strict singleton、multi-acceptable、excluded/deferred 分区；target join 仅在离线 scorer。
- Phase 7 的 I1/I2/I3C/I3-flat 及自动 integrity、至少 120 行分层 blinded QA。
- 历史结果暴露和 development/test overlap ledger。

本轮已重算 N=1,077、M=3,798。任何后续差异都先报 hash/coverage drift，不静默抽取或补足。714 个 NC prompts 与 363 个 parent-delta prompts 分层报告；它们不是 1,077 个相互独立的 clusters，dependency/exposure ledger 仍须按实际共享源关系构造。

## 3. 已知结果如何影响新设计

已完成 RQ2a 的主比较中，Qwen fielded 相对同事实 flat 为 -6.7 percentage points，95% cluster-bootstrap CI [-9.9, -3.6]；field-aware 相对 fielded single-vector 恢复约 +6.6 points，但和 flat 的总体点估计近似。

这说明不能写一个假装尚未见过方向的“显式字段必胜”假设。新的合理问题是：组织方式与 selector 是否匹配，抽取压缩是否丢掉信息，以及更强 selector 能否利用同一事实。以上是旧 RQ2a 的证据，不是 V7 效果预测或新系统已成功的证据。

旧 RQ2b/M6/field-aligned 试验也已经影响设计。新 V7 执行最多称为**在历史探索背景下，前瞻冻结的新版本内部评价**。重新分割旧题不能消除 exposure。任何在结果见到后增加的比较标为 post-hoc exploratory。

## 4. Representation layer：保留四个核心，扩展单列

| 本稿代号 | Canonical 名称 | Selector 能看到什么 | 比较含义 |
| --- | --- | --- | --- |
| R1 | I1-discovery | 源生 name + short description；不加 tags、人工 cluster 描述或 benchmark metadata | 低成本 discovery interface |
| R2 | I2-original | 同一 source policy 下的完整原始 skill document | 自然信息最全，也保留噪声和长度代价 |
| R3 | I3C-fielded | 源生 identity/description 与按七类组织的原文 evidence spans，遵循实际冻结 serializer | 显式操作证据 |
| R4 | I3-flat | 与 R3 相同 evidence-span multiset、相同 identity policy，去掉字段标题/边界 | 隔离显式标签与组织方式 |
| R5，可选 | SSL-style Rich view | 从相同允许源文档生成的 SSL-derived structured view | 最近相关文献的表示适配，不是天然 matched-content |
| 延后 | graph/tree/wiki | 可能含额外关系、分组、摘要或多轮信息读取 | 不在本轮核心 42 配置内 |

七类顺序：use condition、input/precondition、output/artifact、workflow/procedure、dependency/resource、boundary/not-for、success/verification。它们是一个 literature-informed operationalisation，不是唯一可能的 schema。

严格解释边界：

- R3 对 R4：同事实的 field-label/organisation treatment。标题也增加 token，不能宣称纯粹零长度差异。
- R3 对 R2：抽取、压缩、组织及信息遗漏的联合 pipeline effect，不是单因素“结构效果”。
- R3 对 R1：更丰富源证据加组织的联合 effect，不是“多几个 JSON keys”的作用。
- R2 的全文只指冻结 source policy 允许的 primary artifact；未绑定附加资源不自动属于 full-library evidence。
- R5 若使用生成式 paraphrase，与 R3 exact-span 提取存在额外差异，必须明示并做 source fidelity QA。

R3/R4 每个 source 的 evidence multiset 和 identity 必须完全 replay。空字段不补成“none”，不根据 test query 定制 extraction。原文中的否定、条件和操作对象不能被切断；exact substring 是必要条件，不足以证明语义完整。

## 5. Retriever 与 reranker：具体是什么

### 5.1 First-stage retrievers

| ID | 方法 | 拟继承配置 | 重要限制 |
| --- | --- | --- | --- |
| TB | BM25 | 全局每表示一个索引；`[a-z0-9]+`、lowercase、k1=1.5、b=0.75；原始 query | 不截原文；词项统计依当前全库重建 |
| TQ | Qwen generic dense | `text-embedding-v4`，1024 dimensions，raw query，cosine；长文 lossless max-chunk | 这是可能多向量的 pipeline，不叫全条件 single-vector |
| TS | SkillRouter dense | `pipizhao/SkillRouter-Embedding-0.6B`；released query instruction、last-token pooling、1024维 L2-normalised | 与 SkillRouter reranker 是两个模型 |
| TF，可选诊断 | Qwen field-aware | raw query 与七个 I3C fields 分别匹配，继承 uniform-top-two aggregation | 不加入 test-tuned weights、query target-field oracle 或旧 M6 的隐含混合参数 |

计划继承的 TQ chunk 参数：7,500 proxy tokens、256 overlap，完整覆盖、heading/paragraph-aware split、max cosine；同时报告一窗/多窗和 mean-chunk sensitivity。必须在本次实际 sources 上重新 token-audit，不能沿用 V3 的长文数量。

计划继承的 TS revision：`c03c9bcee9fce92ab0262bb6dcf54d174a8ba558`；原实验使用 pinned model config 的 32,768-token ceiling，不截断、不自动改为 chunk。超过边界先暂停适配，不能仅删除不利长文。

这些是旧协议参数的明确拟继承值，不等于本次已验证 provider capability。执行 seal 必须绑定当前可用 endpoint/模型身份、tokenizer、版本与 smoke。如果 alias 已变，不得静默替换模型后叫精确复现。

### 5.2 Rerankers

| ID | 方法 | 输入/操作 |
| --- | --- | --- |
| G0 | 不重排 | 保留 B1 排序 |
| GQ | generic Qwen `qwen3-rerank` | 独立重排该条件已持久化的同一 Top-20 |
| GS | `pipizhao/SkillRouter-Reranker-0.6B` | 固定 query-candidate joint scoring；yes-minus-no score |

GS 拟继承 revision `78986e1142d12857cfd85b8005e62902cd42d858`，prompt contract SHA `face140f238119fc19ba12de90131d1031ada388f08f73e641d0dffd6a00817e`。长文按原协议 query-specific 2,048-token 输入预算、128-token overlap、max-window aggregation；所有 windows 完整覆盖。GQ 的实际长度/窗口策略同样必须绑定，不能假装两个模型的原生上下文和实现成本相同。

每个 B1 条件输出 Top-100；B2 固定使用前 20 个。k=5 仅在独立 pair scoring 成立时由已保存 score 截取作 sensitivity；listwise LLM 的 k=20 输出不能当作真实 k=5 推理结果或延迟。

同一个 B1 条件下，GQ 和 GS 输入的候选 IDs、顺序、query 和表示 bytes 必须一致。不能各自重新召回。不同 retriever 的 checkpoint、训练、长度策略均不同，跨 retriever 结论是受测 pipeline 对比，不是模型架构的干净因果实验。

## 6. 完整实验矩阵与优先级

### 6.1 A：已完成的 RQ2a，保留不重跑

报告实际冻结的 22-condition、600-prompt 结果，而不是用早期 5×3 计划覆盖实际最终矩阵。新 LLM 方法如果后来跑旧 280 clusters，只能叫 post-hoc mechanism extension；不加入旧 confirmatory family。

### 6.2 B：核心完整库比较，36 配置

每行三个末端：G0 / GQ / GS。B1 只跑一次并复用，不能把 reranker 复用误计为重复 B1 工作。

| B1 cell | 表示 | First stage | 末端配置 |
| --- | --- | --- | --- |
| B01 | R1 | TB | B01-G0 / B01-GQ / B01-GS |
| B02 | R1 | TQ | B02-G0 / B02-GQ / B02-GS |
| B03 | R1 | TS | B03-G0 / B03-GQ / B03-GS |
| B04 | R2 | TB | B04-G0 / B04-GQ / B04-GS |
| B05 | R2 | TQ | B05-G0 / B05-GQ / B05-GS |
| B06 | R2 | TS | B06-G0 / B06-GQ / B06-GS |
| B07 | R3 | TB | B07-G0 / B07-GQ / B07-GS |
| B08 | R3 | TQ | B08-G0 / B08-GQ / B08-GS |
| B09 | R3 | TS | B09-G0 / B09-GQ / B09-GS |
| B10 | R4 | TB | B10-G0 / B10-GQ / B10-GS |
| B11 | R4 | TQ | B11-G0 / B11-GQ / B11-GS |
| B12 | R4 | TS | B12-G0 / B12-GQ / B12-GS |

含 12 first-stage 条件和 24 reranked 条件。每个配置都运行全部冻结 scoring scope，不按表现筛选来源或 prompt strata。

### 6.3 C：固定候选 bridge，6 个新增配置

仅靠 B 矩阵不能区分“R3 更会召回”与“R3 更适合给 reranker 看”。因此额外冻结：

`C*(q) = B05（R2 + TQ）实际持久化的 Top-20 IDs/order`

这个 first stage 是**现在就选定的 reference**，不是根据 V7 结果挑 best retriever。它不保证召回充分，也不被称为 oracle。

| ID | 固定候选 | Reranker 看到的表示 | Reranker | 新工作 |
| --- | --- | --- | --- | --- |
| C1-Q / C1-S | C* | R1 | GQ / GS | 2 配置 |
| C2-Q / C2-S | C* | R2 | GQ / GS | 精确复用 B05-GQ / B05-GS |
| C3-Q / C3-S | C* | R3 | GQ / GS | 2 配置 |
| C4-Q / C4-S | C* | R4 | GQ / GS | 2 配置 |

总计 8 个可比较条件，但只有 6 个新增配置。输入候选顺序不变，各表示按同一候选映射加载。

其中 C3 对 C4 是同证据组织比较；C2 对 C3 是完整文本与抽取表示的联合效果。后者不能归因于字段标签。

### 6.4 可退出模块，不与所有核心条件做全交叉

| 模块 | 条件 | 新配置数 | 定位 |
| --- | --- | ---: | --- |
| L，可选文献扩展 | R5 SSL-style Rich + TQ + {G0,GQ,GS} | 3 | 核心后与其他架构一起评估优先级；无可复现实现时退回 critical literature analysis |
| F，既有机制诊断 | R3 + TF + G0 | 1 | 检验旧 field-aware 思路的迁移，不当作新发明 |
| N，可选小系统 | N0、N1、N2、N3，全部使用 C* | 4 | 其中 3 个需推理，N2 复用 N1 judgement 改聚合 |

推荐交付级别：

- **最低完整核心：B+C = 42 配置**，不需要开发新 routing architecture。
- **一种可选增强：核心 + L = 45 配置**，不是用户已决定的必跑扩展。
- **全部本稿模块都通过 gate：42+3+1+4 = 50 配置**，不是必须完成的硬目标。
- 只完成 B 的 36 配置，也能报告端到端系统比较，但必须明确缺少 C 的归因检查，不把它叫本稿完整核心。

图、树、wiki、按需读附加文件、多技能编排，不计入此处 50 配置的草案。按用户新顺序，图/树/wiki 在核心完成后另做可行性与实验设计，不临时混入第一矩阵；完整技能执行/编排仍不在本次 endpoint 内。

### 6.5 工作量，不等于 API calls

令 N 为最终可评分 prompt groups，每 group 一条冻结 query；M 为 source-unique candidates。若实际 schema 不是一对一，必须按 query 数另算。

| 范围 | 对齐结果行 | 逻辑 query-candidate 评分任务（未去重、未展开长文） |
| --- | ---: | ---: |
| B1 | 12N | 依索引实现；不是 12N 次 embedding calls |
| B2 | 24N | 24×20×N = 480N |
| B 合计 | 36N | 见上；B1+重排分账 |
| C 新增 | 6N | 120N |
| B+C | 42N | 重排合计 600N |
| L 新增 | 3N | 另加离线 SSL extraction、TQ index 和 40N rerank pairs |
| F 新增 | N | 至多约七个 field vectors/source；按真实非空字段/长字段计算 |
| N 新增 | 4N outcomes | 正常 3N listwise LLM calls；N2 无新 LLM call，重复性诊断另计 |

若 N=1,077：B 有 38,772 outcomes；B2 有 516,960 logical pairs；C 新增 6,462 outcomes 和 129,240 pairs；B+C 共 45,234 outcomes 和 646,200 logical rerank pairs。pair cache 可以减少 forwards；长文 windows 又可增加 forwards，不能将这组数当成 provider requests 或时间报价。

## 7. 假设：比较研究需要什么、不需要什么

不必为每个矩阵单元编一个“预期胜出”假设。必须预先定义问题、主要比较、估计对象、实用差异和解释规则；有依据时提出可证伪预测。无方向比较完全合法。

### 7.1 五个核心主要比较（本计划固定，不回写旧八假设）

主要推断范围是冻结 **NC lane**；parent lane 作为历史迁移/稳健性复现，另分 public-original 与 controlled 来源报告。所有 strata 均运行，不能因为不显著而隐藏。

| ID | 具体对照 | Endpoint | 假设/问题 | 哪种结果能推翻预期 |
| --- | --- | --- | --- | --- |
| P1，内容 | B08-G0 对 B02-G0：R3 vs R1，同 TQ | Known-A CandidateHit@20 | 操作证据能否增加已审可接受候选的召回？无必胜承诺 | 无明确差异、或 R1 更好；须看 description 已有信息与抽取遗漏 |
| P2，压缩 | B08-G0 对 B05-G0：R3 vs R2，同 TQ | Known-A CandidateHit@20 | R3 是否在最多 3pp 可容忍下降内保留召回？ | non-inferiority 未建立；明确下降超过容忍边界则不适合该替代用途 |
| P3，组织 | B08-G0 对 B11-G0：R3 vs R4，同 TQ | Known-A Hit@1 | 同事实显式标签/边界是否改变 top-1？双侧，不预设正方向 | R4 更好、或差异不确定，均是答案 |
| P4，重排 | B05-GQ 对 B05-G0，同一 C* | Known-A Hit@1 | Joint scoring 是否改善完整 pipeline 的 top-1？ | 净回归、无差异、成本不值得 |
| P5，组织定位 | C3-Q 对 C4-Q，同一 C*、同 GQ | Known-A Hit@1 | 固定候选后，R3/R4 的组织效果是什么？双侧 | 与 B1 不同方向，支持 representation–selector interaction 而非普适结构效应 |

P2 的质量判定不自动构成性价比优势；还必须报告成本。以上 Known-A 是 bounded judged-set endpoint，不是未知全库真实 adequacy 的估计。

所有 TB/TS/GS 复现、stratum interactions、SSL 和新系统结果完整展示，但不事后塞进五个主要检验来改变显著性门槛。

### 7.2 可选小系统假设

N1 对 N0：在固定候选、相同事实、相同 LLM 下，显式要求核对能否改善 Known-A Hit@1，并减少已审、操作上不适合的近邻被选中？这是 secondary prospective hypothesis；不承诺成立。

N2/N3 用于定位冲突处理与字段标签的作用。若没有新系统，这部分标为 `NOT_ATTEMPTED`，不影响 P1–P5。

## 8. 可选小系统：Evidence–Constraint Router，ECR-v1

### 8.1 最小结构与输入边界

`同一全库 reference retrieval → 固定 Top-20 C* → 请求要求/源证据核对 → 确定性排序`

不训练新模型，不改候选生成，不联网补知识，不读 benchmark review，不执行技能。核心 ECR-v1 不实现按需读全文；这样先检验“会不会用已有证据”，避免把信息量扩张混进去。

输入：完整 raw query、二十个 per-query opaque candidate tokens、对应 R3 text。所有姓名/description exposure 遵循核心协议，不额外隐藏某一方身份。LLM 不接触 target、family、A_q、J_q 或 candidate role。

LLM slot `L*` 是一个在 development smoke 后固定的 instruction model；N0/N1/N3 必须同 checkpoint/endpoint、temperature、context budget、candidate order 与输出上限。当前没有绑定可用模型和费用授权，故模块是设计完成但不可执行；禁止用方便的 reviewer 返回替代 selector 运行。

### 8.2 单次 listwise 判断 contract

每条 query 正常一次 call；不在内部循环到答案满意为止。

1. 从完整请求列出有限个明确的任务要求，保留否定、条件、对象和适用范围；不凭常识生成新需求。
2. 每个要求引用 raw-query exact span；最多 12 条。若请求超出容量或 requirements 无法完整表达，标记 `UNSUPPORTED_REQUEST_SHAPE` 并采用预定 fallback，不截掉后半段要求。
3. 每个候选对每个要求输出 `SUPPORTED / CONFLICT / UNKNOWN`。
4. SUPPORTED/CONFLICT 必须附该候选可见文本的 exact evidence span；UNKNOWN 允许无 span。
5. 缺字段属于 UNKNOWN，不等于 CONFLICT。技能未提及某要求，不足以断言其不能满足。
6. 本地 validator 检查 JSON、token membership、无候选遗漏、引用边界、所有要求覆盖。substring 成功不代表语义解释正确，语义错误仍由 failure audit 检查。
7. 不请求或保存隐藏思维链；只保存可核对的 requirements、标签、短理由和源锚点。

### 8.3 确定性决策规则与明确假设

对 candidate c，令 `C(c)` 为明确冲突的要求数，`S(c)` 为得到支持的要求数。排序键：

`(C(c) 升序, S(c) 降序, 原 first-stage rank 升序, opaque-token 升序)`。

这是有意提出、可能失败的 conflict-first heuristic：它假设明确违反要求比缺少证据更严重。它会有“稀疏文档逃过冲突惩罚”“重复要求重复计票”“一个误判冲突压过多个真支持”的风险；不把该规则说成正确性定理。

不按字段手工调不同权重，不删除候选，不从 query 判定 benchmark target-field。所有候选仍保留完整排名。全部 UNKNOWN 时自然回到原 first-stage 顺序。

schema/锚点/候选完整性失败时，整个该 query 采用原 C* 排序作公开 fallback，并记录失败原因。N0 采用相同 fallback 政策。不能自动补写 anchors 或不透明 retry。

### 8.4 四个必配条件（选择做 N 模块时）

| ID | 方法 | 新推理 | 用途 |
| --- | --- | --- | --- |
| N0 | 同 L* 的 generic listwise relevance baseline：每候选 0–3 整体适配评分、短理由和 exact source evidence；分数降序、原始 rank tie-break | 是 | 排除“只是用了 LLM”这项混淆 |
| N1 | ECR-v1 完整 request requirements + support/conflict/unknown + conflict-first | 是 | 提议方法 |
| N2 | 精确复用 N1 judgements，只按 S(c) 降序再 first-stage rank，忽略 conflict penalty | 否 | 仅测试聚合规则，不叫重新进行无冲突推理的消融 |
| N3 | 与 N1 相同，但候选显示 R4，即相同 evidence 去掉字段 labels | 是 | 判断 ECR 是否依赖显式 schema 提示 |

N0、N1、N3 每条 query 的候选内容差异只按上表；不能给 N1 更多源文档。相同模型与候选不等于相同 FLOPs，额外输出成本必须记账。

主要比较 N1–N0；N2/N3 是解释性消融。还必须把 N1 放到 GQ/GS 的质量–成本图上。只胜过 N0 而输给常规 reranker，不叫新 SOTA。

### 8.5 开发、稳定性与退出规则

- 不从 V7 1,077 测试组临时抽题调参。优先使用既有 RQ2a 70 development clusters 中与 V7 测试 family/source 不重叠的部分；这些开发例子是 controlled，须披露 domain mismatch。
- 如无足够不重叠自然开发材料，使用与评估源不重叠的 source-grounded development examples，或承认只做 controlled-dev 方法。不能把已看过标签的 V7 部分改名成 fresh dev 后保持原 test claim。
- 工程预算建议最多 2 个工作日、2 个有记录的 prompt/schema revisions，不以“直到胜出”为停止规则。实际日程由研究者决定，这不是耗时预测。
- development 输出结构与 anchors 的 query-level 合格率至少 95%，critical leakage/identity error 为 0；未达标一次版本化修复后仍不过，则退出 N。
- 语义 smoke 检查否定、前提、缺字段、相同事实不同 label、错误 quote、全 UNKNOWN fallback；不能只检查 JSON。
- 成功返回但判断错误属于方法误差；无法可靠运行属于工程失败，二者分别记录。
- 正式执行前固定一次主运行。另按不含 labels/outcomes 的 hash 排序预选 60 个完整 dependency groups（不足则全选）做 N0/N1/N3 三次独立重复；包含主运行再补两次，报告变异，不挑最好一次。该重复不是新独立样本。
- 如果新系统退步，完成预定反例审计后停止优化本版本；不把 test 错例反馈后再报“同一冻结实验”的改善。

## 9. 文献方法如何纳入

### 9.1 SSL：可选的相近对照，不是逐层检索系统

SSL 将技能信息组织为 scheduling/structural/logical 层；其 discovery 实验比较不同文本视图，使用固定 embedding 与 FAISS 排名。若启用 R5，可适配论文的 rich discovery view 到本冻结源库，并保留 extraction/schema 差异记录；不因此将 tool retrieval 与其他架构文献排除在考虑之外。[SSL 原文 §4.1](https://arxiv.org/html/2604.24026v1)

L 模块的最低 contract：

1. 固定原作者实现/论文版本、view definition、normalizer、source budget 和代码 revision。
2. 只读本轮允许的源文件；不读 query、cluster、labels、review results。
3. 生成整库 R5、完整 source grounding/provenance；身份字段用同一 source identity policy，不暴露 benchmark IDs。
4. unsupported 内容、抽取覆盖、生成 paraphrase、长度/额外结构全部报告；至少使用与核心同等级的 120 行分层 blinded fidelity QA。
5. 固定 TQ 与 GQ/GS，比较 R5 与核心 R1/R2/R3；不拿 SSL 原论文自己的数字和本库数字直接排 leaderboard。
6. 我们的 embedding/benchmark 与作者不同，称为 `SSL-style representation adaptation under a shared routing pipeline`。只有验证完整复现 contract 后才使用 reproduction 一词。

若实现或资源不满足，报告可复现性障碍并做方法层面的 literature comparison；不能编造 empirical baseline，也不因此宣布所有表示方法都已比较。

### 9.2 Graph/tree/wiki：本轮如何讨论

AgentSkillOS 的 capability tree retrieval 与 DAG orchestration 是不同组件；本 benchmark 可评估前者产生的单技能选择，不足以评价完整多技能编排。[AgentSkillOS](https://arxiv.org/abs/2603.02176)

如以后增加 graph 方法，至少分开：同源操作事实的图编码；额外跨技能关系；遍历/扩展算法。关系来源只能是允许源数据，不能来自 benchmark 的 confusable clusters 或 acceptable sets。匹配关系内容的文本 baseline 才能帮助隔离 traversal 收益。

Progressive disclosure 是 metadata → SKILL.md → linked resources 的按需信息加载原则，不直接等价于 tree traversal。[Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

“按需深读”未来应至少有 never-read / selective-read / always-read 三种预算对照，但不属于 ECR-v1，不作为本轮未完成任务。文献中存在某架构不意味着 honours thesis 必须逐个实现。

## 10. 指标：先保证不知道的东西没有被算错

### 10.1 四个集合与主报告口径

对 query q：

- `A_q`：冻结审查确认的 fully acceptable source IDs。
- `J_q`：已有有效最终 adequacy disposition 的 source IDs，含 A_q。
- `U_q = L \ J_q`：库里其余未审/没有可用最终标签的 candidates。
- `C_q(k)`：某 retriever 实際持久化的前 k 个候选。

PARTIALLY_ADEQUATE 不给 fully acceptable credit，但不写成“完全没有用”。实际 enum 如何映射由 canonical schema adapter hash 固定；不凭名称猜 MOST_SUITABLE 或旧 labels。

### 10.2 主要量

| 指标 | 定义 | 高/低是什么意思 |
| --- | --- | --- |
| Known-A Hit@1 | `1[top1 ∈ A_q]` 的均值 | 找到已审可接受路线的频率，不是全库真实正确率 |
| Known-A CandidateHit@20 | `1[C_q(20) ∩ A_q ≠ ∅]` 的均值 | 至少一个已知可接受候选是否存活；旧单 gold 的 Recall@20 在此必须明确重命名 |
| Known-A SetRecall@20 | `|C_q(20) ∩ A_q| / |A_q|` | 找到了多少已审 acceptable members；不要和 CandidateHit 混用 |
| Known-A MRR@20 | Top-20 内第一个 A_q 的 reciprocal rank，未出现为 0 | 已审可接受候选是否靠前 |
| Conditional Known-A Hit@1 | 仅在 C_q(20) 含 A_q 的组中计算成功比例 | 召回成功后的排序能力，不代表端到端能力 |
| Unjudged@1 / @20 | top-1 属于 U_q 的比例；Top-20 未审比例 | 标签覆盖范围，不是模型错误率 |
| Singleton designated Hit@1 | 仅 frozen singleton scope 选中那个已审候选 | 对照 endpoint，不宣称全库唯一性 |
| Regression / rescue | 同候选下已知成功变失败 / 失败变已知成功 | 重排造成的净得失；未审终点单列 |

所有集合 membership 在离线 scorer 中计算，selector 永不接触。对称比较使用同一 query scope。

### 10.3 未审候选的 bounds

真实 fully acceptable Top-1（相对于冻结 rubric）的可识别范围：

`lower = Known-A Hit@1`  
`upper = Known-A Hit@1 + Unjudged@1`。

这是由缺失判断造成的 identification interval，不是 confidence interval。采样不确定性 CI 另算。对方法差异要逐 query 计算最有利/最不利的未知标签边界，不能只把两个独立总区间随意比较。

若 M 比 B 的 Known-A 高，但 M/B 的未审返回差异足以翻转实际适配排名，只能说“在 frozen judged set 上更高”，不能宣称整体 routing correctness 更高。不同方法可能受到 pooled judgments 的不同覆盖偏差。

本版本不根据新系统返回哪些未审项就自动扩充 A_q。若将来需要 outcome-triggered judging，必须保持 v1 不变、统一覆盖各方法输出、盲审并出单独补充分析；该补充不是原始 outcome-blind freeze。

### 10.4 语义混淆诊断不能只看总体 Hit@1

预先由 source-grounded relation/审查记录定义合法评估用近邻集合 D_q；这个集合只在 scorer，可包含已审但非 fully acceptable 的 confusable candidates。没有可用关系证据时，不把所有 wrong candidates 都称作 semantic confusion。

在 reference C* 同时含 A_q 与 D_q 的预定义 diagnostic slice，报告：

- top-1 被已审操作不适合近邻占据的比例；
- acceptable-to-neighbour regression 与 neighbour-to-acceptable rescue；
- input、output、dependency、boundary、workflow 等有证据的错误类型；
- 此 slice 的组数和覆盖率，以及未进入 slice 的原因。

C* membership 在运行后机械计算，但 slice 规则现在固定；不按某个 reranker 输赢挑题。这属于由固定 first stage 条件化的诊断，不称作独立代表性子样本。

近邻 top-1↓但 Unjudged@1↑，不自动意味着混淆解决；可能只是改选了尚未审的候选。

## 11. 统计与“高/低”的预先解释标准

### 11.1 单位与分层

- 逐 query 配对比较，point estimate 采用各报告 stratum 内 prompt-weighted 均值，便于继承旧 RQ2b estimand。
- 重采样单位是预先绑定的 family/dependency group，而不是每个 paraphrase、模型调用或 candidate pair。
- group 连接同一 authored family、重复/近重复 prompt、共用目标/核心成员源的依赖；不要用所有审查 distractors 连边，否则共享背景会把整库错误并成一个 group。
- 报告独立组数、组大小分布和最大组；若依赖成分过大、有效组数过少，保留描述性结果，不硬造精确推断。
- 同时给 equal-group-weighted sensitivity。NC、parent-public、parent-controlled 分开；综合数仅为带权组成说明。
- singleton/multi、cue level、prompt stratum、长短源、稀疏字段作预先冻结 secondary slices；缺 metadata 的记录显式 unknown，不从结果推断 stratum。

### 11.2 新推断提案

这是研究者批准的前瞻 V7 analysis amendment；在本轮 selector outcomes 前固定，不回写旧 RQ2a/V3 的统计 contract。

- 10,000 whole-group percentile bootstrap，seed `2026090801`；报告配对差值的 two-sided 95% descriptive CI。
- P1/P3/P4/P5 使用 100,000 次 whole-group paired sign-flip、seed `2026090802`，双侧检验；每次整组翻转，再计算 prompt-weighted 差值。近似交换性假设和历史探索限制一起披露。
- 五个主要决策以 Bonferroni 分配每项 alpha=0.01：四个 effect tests 要求 p<0.01；P2 使用 one-sided 99% grouped-bootstrap lower bound 对 -0.03 margin。
- 这种调整不让已探索数据变成 untouched confirmatory evidence。除五个已固定比较外，CI/p-values 是探索性稳定性描述，不对全矩阵几十个点作新胜者发现宣称。
- N1–N0 的主比较在 optional secondary family 内预先固定；N2/N3 不用于把不利结果改成主结论。若报告该模块三项检验，模块内统一 Holm 校正，仍明确 secondary。

### 11.3 实用阈值与不确定性

本计划采用 **3 percentage points** 作为主质量最小有意义差异/非劣容忍值；这是研究者的应用取舍，不是学校评分标准。另报告 1pp/5pp sensitivity，但不改主结论。

| 结果 | 允许使用的措辞 | 禁止推论 |
| --- | --- | --- |
| 点估计 ≥+3pp，CI 方向稳定，主要检验通过 | 在指定 endpoint/scope 上有实用幅度的支持性改善 | 普遍更好、因果机制已证明 |
| 点估计正但 <3pp，即使 p 很小 | 小幅但可检测差异，未达本稿 practical bar | 显著所以很重要 |
| CI 同时含有有意义改善和下降 | 结果不确定/精度不足 | 两者相同 |
| 整个 95% CI 落在 [-3pp,+3pp] | 在该估计框架下支持 practical similarity；正式 equivalence claim 需相应预先检验 | 完全等价、所有场景相同 |
| P2 99% lower bound > -3pp | 支持已声明容忍范围内的 non-inferiority | 优于 R2、免费无损 |
| P2 没通过，但 CI 没显示明确损害 | 未能建立 non-inferiority | 已证明 inferior |
| 区间在负方向且效果达到实用量级 | 该配置/范围存在有意义退步 | 信息本身没用、所有同类方法失败 |

“改善稳定”与“最小改善至少 3pp”不同：后者需要整个适当下置信界超过 +3pp，不能只看点估计。

不设“达到 90% 才能毕业”等绝对阈值。不同集合难度、审查覆盖和来源构成不同，跨 benchmark 绝对数值不能当标准线。

### 11.4 必须自动检查的恒等关系

同一 candidate list、scope 与权重下：

`end-to-end Known-A Hit@1 = CandidateHit@20 × Conditional Known-A Hit@1`。

当分母为零，conditional 为 NA，不伪造零精度；分层加权不能随意混用。有效重排只重排候选，CandidateHit@20 必须不变。违反这些条件优先判为 join/denominator/runner defect，不解释成模型现象。

## 12. 结果模式解释表：先写标准，再看结果

| 观察到的模式 | 可以说什么 | 必须进一步查什么 / 不可以说什么 |
| --- | --- | --- |
| R3 > R1，但 R3≈R4 | 抽取出来的操作事实有用；显式标题没有额外明显收益 | 不是证明显式 schema 必需 |
| R4 > R3 | 这类 labels/组织可能与受测 selector 不匹配 | 查顺序、长度、generic heading、field assignment；不能说操作信息没价值 |
| R2 > R3 | 全文 pipeline 在此保留了更多可用选择信号 | 查 extraction omission、否定/条件断裂、分布式证据、chunk机会数；单看总分不能断言原因 |
| R1≈R3 且 CI 足够窄 | 简述对这个 scope 可能已经足够 | 查 description availability strata；不推广到所有 skill libraries |
| R3 略低但明显便宜 | 可能存在质量–成本交换 | 必须满足预设 loss tolerance 才推荐替代；低于容忍值就诚实展示代价 |
| R5 SSL-style 胜 | 该 richer view/pipeline 在同库有效 | 其额外信息、normalizer、长度也是 treatment，不能只归功于三层图形式 |
| SSL-style 不胜 | 在本适配与库中未复现预期收益 | 优先查 fidelity/implementation；不能据此否定原论文在原条件下的结果 |
| CandidateHit@20 高，但 Hit@1 低 | 已知可接受技能已到候选集，排序是重要瓶颈 | 是否被已审操作不适合近邻击败，还是选了未审项？ |
| CandidateHit@20 低，conditional 很高 | 排序器在存活子集上好，端到端受召回限制 | 不能用 conditional 高分宣称完整系统强 |
| 重排提升很小，B1 本已很高 | 可能接近 endpoint ceiling | 报告剩余错误数、CI 与成本，不把无空间改善当算法失败 |
| 只在 singleton 好、multi 差 | 对多条可接受路线的覆盖/排序可能有限 | 同时看 SetRecall 与 Unjudged；不强迫 multi 回 strict |
| strict target 命中下降、Known-A 命中提高 | 系统可能选择了另一个有效路线 | 检查 canonical label join；不能把 target agreement 直接称任务正确性 |
| 总体改善、NC 不改善 | 改善可能来自更容易或不同构成的 parent 条件 | 不能宣称解决 semantic confusion |
| NC 已审近邻错误下降、未审比例上升 | 终点变了，但真实适配是否改善仍不清楚 | bounds 和 coverage；不能自动补审只给赢家加分 |
| BM25 与 dense 的表示排序不同 | 信息表达与匹配机制存在受测 interaction | “词汇重合/语义冗余”是候选解释，需诊断佐证 |
| TS/GS 胜过 generic model | 该 skill-tuned checkpoint/pipeline 更好 | 训练数据、规模、token政策可能不同，不能纯归因于架构 |
| N1 > N0，但仍输 GQ/GS 或贵很多 | 显式约束方案相对 generic LLM 有机制价值，但部署优势未建立 | 不称 state of the art，不隐去强 baseline |
| N1 输 N0，N2 恢复 | conflict-first 聚合可能过于保守 | 对同 N1 judgements 的 rule ablation 提供局部定位；不证明所有 constraint reasoning 错 |
| N1 输、quote 都 exact | Literal grounding 没有保证正确理解否定/条件/操作对象 | 做 semantic anchor/rationale 审查，不能声称 extraction 已完美 |
| N3≈N1 | 该显式核对方法未显示必须依赖七字段标题 | 可能从原始 span 自行理解，结果不损害 RQ1 的信息价值 |
| 所有方法都接近 ceiling | 此测试对方法差异辨别力不足 | 描述剩余失误与外推限制，不事后重挑更难题替换主集合 |
| 所有方法都很低 | 库/请求/表示/召回可能难，也可能实现错误 | 先做 valid-run QA，再进行有分母的分阶段诊断；不能只说 benchmark 很好很难 |
| 工程流程没有产生可靠有效输出 | 该实现未达到评价条件 | 不是算法无效的实证结论；保留失败记录与退出原因 |

## 13. Failure analysis 的完整 SOP

### 13.1 先机械、再语义

先检查 source/prompt/representation/input hashes、identity、schema、coverage、score/candidate correspondence、窗口覆盖、cache key、fallback/exception，再解释模型。工程错误与未审标签不混入“semantic confusion”饼图。

### 13.2 冻结分类

| 类别 | 证据条件 |
| --- | --- |
| TECHNICAL_INVALID | hash、schema、join、缺 candidate、未授权截断等使输出不可解释 |
| KNOWN_ACCEPTABLE_NOT_RETRIEVED | C(20) 中无 A_q；仅说明已知 acceptable miss |
| KNOWN_ACCEPTABLE_MISRANKED | C(20) 含 A_q，但 top-1 是已审非 fully acceptable |
| UNJUDGED_SELECTION | top-1 不在 J_q，缺少 adequacy 结论 |
| SOURCE_INFORMATION_GAP | 完整允许源文档本身未明确提供必要路由信息 |
| EXTRACTION_OMISSION | 信息在 I2 中但未保留在 I3，且与判断有关 |
| REPRESENTATION_DISTORTION | 否定/前提/对象/顺序被错误切分或字段误归类 |
| QUERY_INTERPRETATION | 忽略/添加要求，丢失 polarity 或 scope |
| MATCHING_OR_AGGREGATION | 证据可见但匹配/打分/冲突优先规则产生错误 |
| CONTEXT_OR_POSITION | 有对应窗口、截断、顺序或稀释诊断支持 |
| BENCHMARK_LIMITATION | 题目覆盖、池化标签、源关系或 exclusion 选择性造成解释限制 |

前四项是机械可定位的路由状态；后面是可能共存的解释标签，不强行互斥。没有证据的理由记 `UNRESOLVED`。

### 13.3 抽样与防挑例

1. 所有 rows 先做自动阶段/已审覆盖统计。
2. 对 P1/P3/P4/P5，取 comparison discordant dependency groups 的合并集合；按 pair-hash 固定排序，每个比较最多 12 个组，正反方向各最多 6 个，缺一方向就完整保留而不制造反例；最多 48 个 group selections，重复组只审一次。
3. 另取 NC scope 按 hash 排序的 12 个完整 groups，不按表现选取，查看成功/失败共有的源质量问题。
4. 核心语义分析最多 60 个独特 groups；组内相关 prompts 一起审，不只取最好讲的一句。
5. 若启用 N，再从 N1–N0 discordant groups 选最多 20 个，双方向各最多 10 个；合计上限 80 个独特 groups。样本不足则全取并报告实际分母。
6. 隐去 method 名称与输赢方向，提供 source、query、匿名预测/必要 trace。先做 source-based taxonomy，再揭示方法用于分析。若研究者已知标签/预测，明确称 unblinded researcher analysis，不冒称独立盲审。
7. 建议对 20% 的语义样本做第二次独立核验，报告实际 reviewer 身份/AI-assisted 性质和分歧；没完成就披露，不能伪造一致率。
8. 按输赢筛选的病例样本只能说明机制案例；不能将其中比例直接外推成全库错误类型 prevalence。全库频率来自自动状态统计或额外具有已知抽样概率的样本。

固定 selection seeds/hash salt `rq2-failure-v1-20260908`；输出 selection ledger，所有反方向例子保留。审计发现新的实质 label defect 时保留原冻结，开 limitation/method docket；不悄悄修到某方法变好。

## 14. 成本、稳定性与推荐规则

### 14.1 必须分开的账

- Offline：source extraction、semantic QA、SSL/graph compilation（若有）、embedding、index build、storage。
- Online：query embedding、retrieval、reranking、LLM input/output tokens、calls、模型/CPU/GPU 时间、实测端到端 latency。
- Engineering overhead：失败、transport retries、人工 QA 与开发工时单列；benchmark label construction 不伪装成部署单次 query 成本。
- Cold/warm 分开；从磁盘读 cache 的重放时间不叫真实在线 inference latency。
- 同硬件/并发/批量条件下报告 p50、p95；跨 provider/硬件只作实际 deployment pipeline 比较，不宣称纯模型计算速度。

`C_total(n) = C_offline + n × C_online`，报告 n=1/10/100/1,000/10,000/100,000 的摊销情景；break-even 仅在计价基准和线上成本差异有意义时计算。价格是注明日期的补充，tokens/calls/time/bytes 为可重放主要成本量。

### 14.2 推荐标准

- 高质量且低成本：检查 uncertainty 和 coverage 后可推荐该受测范围的 Pareto 优势。
- 更高质量、更高成本：报告每提升 1pp 的额外开销及适用预算，不自行宣布值得。
- 质量 practical-similar 或通过预设 non-inferiority，在线实测开销至少降低 20%：可称候选 efficiency improvement；20% 是本计划采用的 practical bar，不是客观常数。token 减少而 latency 未降，只能称 token reduction。
- 同时更差更贵：不推荐该实现；保留失效分析。
- 相同点估计但区间宽：不选择赢家；描述证据不足。

核心矩阵优先级不根据中间科学结果改变。若预算不足以完成 required model row，标记 incomplete matrix，预先商定减少 scope；不从已见排名中选择留下的模型。

## 15. 开跑顺序、gate 与 stopping rules

| 阶段 | 产物/通过标准 | 停止条件 |
| --- | --- | --- |
| D0，正式研究计划 | PASS：用户要求本版正式定稿；B36+C6、P1–P5、统计/实用阈值与解释规则固定 | 后续科学改动需 versioned amendment；正式计划不替代具体 runtime/预算 seal |
| D1，V7 closure / source portability | 已 PASS：1,077 frozen prompts、149 exclusions、3,798 exact primary sources；详见准备包 | 后续 drift 才阻断；不重审、不切换 528 |
| D2，Phase 7/8 | 四表示 1:1 source binding、exact spans、matching multisets、至少 120 blinded QA；root readiness PASS | critical error 任一；major error >5% 总体或 reviewed field stratum，按 master SOP 处理 |
| D3，analysis/exposure freeze | dependency groups、strata、历史暴露、五个主要比较、unknown-label bounds、failure sampling 冻结 | metadata不完整影响主分母/依赖结构；不能靠硬编码数量通过 |
| D4，implementation preflight | 模型/tokenizer/script/instruction hashes、lossless length policy、label-free dry-run、dedup/cost estimate | 当前模型变更、源外传或费用未授权、无法可靠实现 |
| D5，核心 B1 | 12 条件完整 scopes，Top-100、exact C20、索引与cache回放 | hash/identity drift；不能静默重试改参数 |
| D6，核心 B2+C | 24+6 新 rerank conditions；same-list检查；无新增候选 | mismatch、漏行或无法说明的推理缺失 |
| D7，可选扩展 | 核心完成后评估 wiki/graph/tree/SSL/field-aware，再设计小系统；受 V7 结果启发的新增比较标 exploratory | 独立 feasibility/budget gate；按模块退出，不挟持核心交付 |
| D8，analysis | 阶段恒等关系、paired stats、bounds、cost、failure ledger全部可复现 | 发现技术问题先隔离，科学问题保留记录 |
| D9，写作与口头准备 | 明确回答 AQ1–4；成功/失败同一套解释标准；强baseline/限制/复现说明 | 未决缺陷不能写成最终结论 |

当前 master SOP 的终点仍是 READY_FOR_FORMAL_EXPERIMENT，随后按具体 manifest 与预算单独取得运行授权。本稿不产生任何真实 run command 或“预计明天跑完”的承诺。

预计耗时必须在 D4 根据实际 M/N、去重 pair 数、window 数、设备、并发、provider quota 和 development pilot 吞吐计算。不要按 42×N 简单换算成 calls 或 GPU 小时。

## 16. 和 honours 评分标准的对应

### 16.1 原文核验与适用范围

仓库文件：`thesis_reference/usyd_honours/hons_thesis_assessment_criteria_2014.pdf`，共 8 页。本次抽取全文并渲染查看第 3–5 页。它列出 Contribution 40、Critical analysis 30、Knowledge of area 20、Communication 10，并说明分量随 thesis 性质可变化。这是本地保存的历史 rubric，不自动代表 2026 最终适用权重。

2026 S2 官方 INFO4913 与 COMP4106 outline 均列出 thesis 80%、presentation Q&A 20%、presentation 本身 0% hurdle；AI use 规则因任务不同，thesis 标 AI allowed、Q&A 标 AI prohibited，并要求核对 Canvas 细则与声明 AI 使用。用户实际 programme/unit 尚未在本稿确定，所以这些是当前公开参照，不替用户确认最终课程要求。[INFO4913 2026 S2](https://www.sydney.edu.au/units/INFO4913/2026-S2C-SU-CC)；[COMP4106 2026 S2](https://www.sydney.edu.au/units/COMP4106/2026-S2C-SU-CC)

注意：40/30/20/10 是 thesis 内部质量维度；80/20 是所列 unit 的 assessment components；不是同一层级，不相互替换。历史 First Class/Medal 分段也不等同于现行 unit HD=85+ 分段，不据此保证 mark 或 medal。

### 16.2 新设计为什么可能更好

| Rubric 维度 | 本稿新增的可核查价值 | 即使新系统不做/不胜，如何成立 | 剩余风险 |
| --- | --- | --- | --- |
| Contribution，历史40 | 一套 source-grounded benchmark 上的机制/完整库分离评价；同候选 bridge；可复用失败定位与成本框架 | 比较研究产生非显然结论，限制 representation universalism，提供可重放证据 | 单纯堆矩阵、复述已知排名，不自动算原创贡献 |
| Critical analysis，历史30 | 预先定义正负/无差异解释、unknown-label bounds、召回/排序拆分、消融、反向病例 | 这是负结果也能有价值的关键 | 稀疏或偏差样本不能强因果归因；需要完成而非只计划 |
| Knowledge，历史20 | 正确区分 SSL信息层、tree search、progressive disclosure；最近相关 baseline 或诚实适配分析 | 不需实现所有文章，但要说清最近工作做了什么、缺口何在 | 只列论文名或错误称“优化已有系统”会削弱该维度 |
| Communication，历史10 | RQ1→RQ2a→RQ2b 一条主线；核心/可选/历史边界清楚 | 能明确解释为什么失败不推翻全部研究 | 50配置全塞正文会模糊结论，主文应只保留关键对照 |

我的判断是：**比“必须做个更强系统”或“把所有架构都跑一遍”更稳健，也更接近高质量 honours 的方法与分析要求。** 但不能仅凭这份 spec 预测分数；评分取决于实际研究执行、研究者独立理解、结果意义、写作和答辩。

### 16.3 必须能独立回答的答辩问题

1. 为什么 RQ1 信息有用，RQ2a fielded 却能更差？
2. 同事实比较与整系统比较的区别是什么？
3. 你为什么选择这三种 first stages、两种 rerankers？哪些差异不是纯架构因素？
4. 1,077 是什么单位，为什么不等于 1,077 个独立统计样本？
5. K=6 audit 与 Top-20 retrieval 有什么关系？为什么不把未审候选当错？
6. 为什么 fixed-candidate bridge 能帮助定位，但不保证真实部署召回？
7. 新系统输了，哪条假设被削弱，哪条没有被检验？
8. 为什么没有全面比较 graph/wiki？加跨技能关系会改变什么？
9. 你能指出一个对自己方法不利、但必须保留的反例吗？
10. AI-assisted authoring/review/implementation 的角色与研究者责任如何披露？

## 17. 最终论文/仓库交付清单

核心无需新系统也应完成：

- 一张 literature–method–information mapping 表。
- 一个本版本 source/prompt/label/representation root manifest 及 exact replay。
- 完整 B+C matrix、未执行配置与原因表，不能仅发布赢家。
- 五个主要对照及全部 required replications；NC 与 parent/origin 分层。
- 召回→排序阶段分解，Known-A / Unjudged / bounds 同页呈现。
- source/extraction/representation/retrieval/ordering failure taxonomy 与 selection ledger。
- offline/online、cold/warm、质量–成本图和摊销情景。
- threats to validity：历史暴露、AI review依赖、bounded pool coverage、排除选择性、受测模型有限、合成背景/自然源混合、训练数据未知、无执行结果。
- 如果选择做 L/F/N：方法版本、偏离文献处、失败/退出记录和全部消融。
- 一页结论：什么信息/表示/方法在什么条件下有帮助，什么没有帮助，下一步证据需求是什么。

建议主文只放 5–7 个核心图表：RQ链与边界、方法/信息表、关键对照、阶段错误分解、NC诊断、质量–成本、精选双向反例。完整 42–50 配置放 appendix/repository，不让 examiner 重建版本历史。

## 18. 已批准计划与剩余执行输入

用户本轮明确要求这版正式定稿，并把大规模背景扩展列为未来事项。主计划现在固定如下；不再逐项重新请求研究方向批准：

1. 保留现有 RQ2a，RQ2b 以 semantic-confusability 下的 operationally suitable routing 为核心。
2. B36+C6 是完整核心；架构扩展待核心后做 feasibility，ECR 是可退出候选，不提前阻塞主矩阵。
3. 未审候选显式 unknown；主 endpoint 用 Known-A 并同步报告 coverage/bounds。
4. 五个主要比较、3pp practical margin、分组统计、反向病例和退出规则在新结果前固定。
5. graph/wiki 不加入第一矩阵，后续另立适配协议；完整 skill 执行系统不在当前评价范围。不把新系统胜出设为 thesis 成立条件。

benchmark freeze 与 N/M 已验证；仍须填齐 execution representation QA/root、dependency/split/exposure ledger、各 provider/model revision 与 window policy、L*（仅启用 N 时）、预算/设备/调用授权、用户实际 honours unit 的当前 rubric。未齐时继续本地准备，不把标签 freeze 等同于正式实验已启动。

## 19. 依据与核对记录

### 19.1 当前仓库依据

- [RQ2 Comprehensive Methodology Specification](</Users/jackyzhang/Work/Honour Thesis/thesis_notes/current/RQ2 Comprehensive Methodology Specification - 2026-07-26.md>)：表示、已完成/历史边界与具体实现约束。
- [RQ2 Current Status and Implementation Tracker](</Users/jackyzhang/Work/Honour Thesis/thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md>)：M6-v1/v2 与合规 field-aware adapter 的区别。
- [RQ2a Confirmatory Results and Analysis](</Users/jackyzhang/Work/Honour Thesis/thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md>)：实际 22-condition 结果与统计，不用早期规划取代实际冻结。
- [RQ2b Full-Library Execution Protocol](</Users/jackyzhang/Work/Honour Thesis/thesis_notes/current/RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md>)：既有四表示/三检索/两重排、参数、窗口、账本。内部 chronology 有历史状态，应按较新状态与绑定结果读。
- [RQ2b-NC master SOP](</Users/jackyzhang/Work/Honour Thesis/skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md>)：K=6、未审不为负、Phase 7/8、授权边界。
- [RQ2b Naturalistic Extension Protocol](</Users/jackyzhang/Work/Honour Thesis/thesis_notes/current/RQ2b Naturalistic Semantic-Confusability Extension Protocol - 2026-08-31.md>)：自然源/历史 parent/背景来源分层与外推限制。
- [Information Layer Framework](</Users/jackyzhang/Work/Honour Thesis/thesis_notes/current/Information Layer Framework.md>) 与 [Literature review source](</Users/jackyzhang/Work/Honour Thesis/thesis_latex/chapters/02_literature_review.tex>)：同信息与新增关系的区别。
- [历史 honours rubric PDF](</Users/jackyzhang/Work/Honour Thesis/thesis_reference/usyd_honours/hons_thesis_assessment_criteria_2014.pdf>)：第3–7页四维评分说明。

本次读取文件的 SHA-256（这些是被读文件身份，不是新实验 freeze SHA）：

| 文件 | SHA-256 |
| --- | --- |
| 2014 honours rubric | `7f33eeb93bba7f89f2b1043cd19a63db179464068b5ed5205b7b61cb780ce16e` |
| RQ2a final analysis | `5f7a6335f86773de2496e8b0f897702eca527bad1405737eb98b987420794552` |
| 2026-09-05 master SOP | `68f7a8e4e802317208d72155b6b3490d0f3587324aaebb67cfac0341241b8835` |

### 19.2 本次核对的外部 primary sources

- [SSL paper](https://arxiv.org/html/2604.24026v1)：表示适配，非逐层 runtime retrieval；预印本。
- [AgentSkillOS paper](https://arxiv.org/abs/2603.02176)：capability-tree 管理/检索与多技能编排的边界；预印本。
- [SkillRouter embedding model card](https://huggingface.co/pipizhao/SkillRouter-Embedding-0.6B) 与 [reranker model card](https://huggingface.co/pipizhao/SkillRouter-Reranker-0.6B)：不同 checkpoint 角色；实际运行仍绑定旧协议 revision而非浮动main。
- [INFO4913 2026 S2 outline](https://www.sydney.edu.au/units/INFO4913/2026-S2C-SU-CC)、[COMP4106 2026 S2 outline](https://www.sydney.edu.au/units/COMP4106/2026-S2C-SU-CC)：现行公开 assessment components；详细 rubric/AI instructions 以实际 Canvas 为准。
- [INFO4990 2026](https://www.sydney.edu.au/units/INFO4990)：研究计划、批判评价、文献与清楚沟通的学习要求，不是 thesis 内部评分权重证明。

本研究计划与本地准备未运行 selector、未计算新 benchmark metric、未变更 target/acceptable labels。前一轮已按用户授权将冻结研究源材料与准备文档合入 GitHub main；Git 保存不等同于授权 provider 推理。主矩阵与统计阈值是本计划的研究选择，不是 literature 或 rubric 强制要求；ECR 仍是可退出设计。

## 20. 两篇用户提供的 thesis：只借鉴组织与分析，不推定成绩

用户在本稿编写期间提供了两份本地 PDF。按要求只做 targeted skim：目录、摘要、若干方法/结果/讨论页，并渲染部分页面检查版式；没有完整复核算法、证明、实验或成绩。以下正文页码以论文印刷页码为准，同时给出 PDF 页序，方便定位。

### 20.1 Shunqi Mao，AV-GeN（2022）

源文件：[SHUNQI MAO.pdf](</Users/jackyzhang/Downloads/SHUNQI MAO.pdf>)，80 个 PDF 页面。

- **正文 p.27 / PDF p.37**：Methods 章先讲整体流程，再说明哪些模块继承已有框架、哪些是本研究新增。这很适合我们：先承认 BM25/embedding/reranker 是既有组件，随后准确界定 ECR 或评价设计的新部分。
- **正文 p.54 / PDF p.64，Table 4.2**：一张分组消融表同时展示完整系统、移除模块及模块内部选择。借鉴“一个改变对应一个比较”的组织方式；我们的 N0/N1/N2/N3 不需要散成四段重复说明。
- **正文 pp.57–60 / PDF pp.67–70 的讨论结构**：按设计选择讨论，并连接最近方法。我们可按 extraction、representation、candidate generation、ordering 分节，而不是按每个 run 的时间顺序写。
- **正文 pp.61–62 / PDF pp.71–72**：明确写到 split distribution、run variance 和算力不足以充分重复的限制。我们应同样说明 model stochasticity、历史数据暴露、bounded labels 和排除选择性，而不是用一个漂亮点估计掩盖这些问题。

版式可借鉴：清楚的层级、适度留白、黑白也能读的表格、指标方向箭头、caption 对缩写作解释。不能从这些页判断所有结果的统计推断都可靠；我们不照搬“显著”“证明”等强措辞，保留预先定义的 CI、效应大小和 scope。

### 20.2 Mitchell Jones，The Maximum Facility Location Problem（2015）

源文件：[MJones_thesis.pdf](</Users/jackyzhang/Downloads/MJones_thesis.pdf>)，64 个 PDF 页面。

- **正文 p.31 / PDF p.41，Figure 4.3 / Theorem 3**：作者对自己的 dependent-rounding 算法给出一个坏实例，展示其 approximation limitation。最有价值的借鉴是主动明确“在哪些构造下会失败”，不是学习把任何失败都说成成功。我们的 ECR 可以用有源证据的 polarity、缺字段、冲突优先反例说明失效条件；经验反例不伪装成形式化定理。
- **正文 p.39 / PDF p.49**：先定义 predicted/actual 匹配与评价规则，处理一个预测可能匹配多个真值的计分问题。对我们的启发是先说清 A_q、J_q、未审项与多 acceptable 的计分，再展示性能。
- **正文 p.41 / PDF p.51**：速度讨论同时提到 solver、实现语言和工程优化差异。我们的 provider/硬件/window/缓存比较也必须说明这些混淆，不能只把耗时差归于算法。
- **正文 p.48 / PDF p.58**：作者解释虽然数据实例大，冲突结构却很稀疏，因而实例可能较容易。这与我们直接相关：候选库大、cluster 多，不等于 semantic-confusion 难度足够；必须报告近邻竞争与阶段错误。

版式可借鉴：小而聚焦的示例图、读者可独立理解的 caption、定义先于实验、讨论不重复完整结果表。其理论论文的 theorem-heavy 结构和生物学指标不适合直接迁移。

### 20.3 对本 thesis 的四项具体写作安排

1. **主方法图**：frozen source → representation → first-stage → persisted candidates → reranker → scorer；将 labels/审查资料画在 scorer 侧，明确不流入 selector。
2. **核心结果表**：只放预先声明的主要比较，并列 effect、CI、Known-A endpoint、Unjudged rate 和成本；完整矩阵留 appendix。
3. **一张消融表 + 一张双向反例图**：如果做 ECR，明确每次移除了什么；同时展示它纠正了什么、又破坏了什么。没做 ECR，就展示 representation/selector 的正反例。
4. **统一结果段落模板**：观察到什么（分母、效应与区间）→ 与哪一假设一致/冲突 → 有什么诊断支持解释 → 哪些替代解释尚未排除 → 对应用和 RQ 的边界结论。

论文的排版目标是降低 examiner 理解证据的成本，不是复制封面、字号或总页数。两份示例都不能替代现行学校模板/声明要求，也没有提供本次可核验的 Medal 或分数证明。


## 21. 未来 scale-out 扩展：额外约 20,000 个背景源

Status: **FUTURE / NOT_EXECUTED / NOT_REQUIRED_FOR_CURRENT_RQ2_COMPLETION**。

### 21.1 未来要回答什么

在固定请求、核心候选与路由方法的条件下，增加背景候选是否改变可接受候选召回、排序可靠性和单位查询成本？不同信息组织与控制策略的离线建设成本、在线成本，以及可运行边界如何随库规模变化？

这是将来独立的新 scope/analysis amendment；本次不下载、不筛选、不新增候选，不再启动 acceptable-set 审查，不改 K=6，也不使用 deferred 528 package 补库。

### 21.2 规模和背景来源的定义

“2 万 background”暂按**额外加入约 20,000 个 source-unique candidates**理解，而非总库精确 20,000；若全数合格且无重复，名义总数为 23,798，真实总数只能由未来 admission manifest 决定。31k discovery frame 只是可考察来源，不是已通过许可/身份/去重的候选库。

未来先冻结 source provenance/许可、exact-hash 与 near-duplicate/alias 处理、来源构成与抽样 seed。不按当前方法在哪些背景上表现差来挑 distractors。新增项叫 background candidates，不预设它们均不适合请求。来源混合、模板化程度、文档长度和近邻密度均需报告。

建议使用至少三个预先固定的 nested 库规模；每一级都包含原核心 sources 和同一 query set，新背景按固定顺序增量加入。具体档位、重复抽样与预算待该扩展获准时冻结；现在不把 8k/12k/20k 等设成新硬目标。

### 21.3 标签与公平性边界

1. V7 已审 A_q 的正例身份可以保留，但新增候选可能也 fully acceptable；原 strict singleton 不能继承为扩展库中的全库唯一答案。
2. 若只做 cost/engineering scale preflight，不需要借此宣布 routing correctness；Known-A 仍只能表示旧已知正例的保留情况。
3. 若要比较扩展库的实际适配质量，必须另立 outcome-blind、各方法对称的增量覆盖审查，或清楚保留 unknown-label bounds。不得自动把新增 candidates 当作负例，也不看某个赢家输出后只补它的标签。
4. 不改原 V7 rows、不把新结果混入第一矩阵；扩展有自己的 source/representation/label/root hashes、结果目录与 exposure ledger。
5. 架构编译不能看到 queries/labels/benchmark cluster edges。新关系若超出原事实集，报告额外信息的 whole-pipeline effect，并尽可能设置同信息的文本比较。

### 21.4 未来候选对照及成本账

| 对照类型 | 特别要核对什么 | 不能预设什么 |
| --- | --- | --- |
| lexical/dense + 固定 Top-k reranking | index size、build time、query/search time、候选召回；rerank 输入预算固定 | 只测重排耗时不代表全流程与库规模无关 |
| 一次全库 in-context LLM | 对每种表示测真实 tokenizer 长度、上下文余量、完整候选覆盖、顺序敏感性、输出可解析性 | 装得下不等于更好；装不下也不能无记录截断后算模型失败 |
| 全库逐项 LLM/cross-encoder scoring | 随候选数增加的 pair/window 数、调用与累计 latency/cost | 与固定 Top-k LLM reranking 混为一谈 |
| wiki/tree/graph | compilation/embedding/storage/update cost 与线上 traversal/read 成本分账；摘要保真与停止规则 | 图一定昂贵到不可用，或有索引就已证明可扩展 |
| bounded agentic retrieval | read/search 轮数、token/call cap、停机/回退、跨题状态隔离 | 用不受限的额外推理成本宣称控制策略必然更好 |

同模型、同表示/证据、同 query scope 与硬件/并发能保持的条件尽量保持；不能保持的列为 pipeline differences。对超 context、超内存、超预设预算和 timeout 分别记工程可行性状态，保留实际分母；不能把它们悄悄删掉，也不能把未运行的行填成 0% accuracy。无截断的共同可行 subset 只能作另列 sensitivity，不替代 full-scope availability。

至少报告：Known-A/Unjudged 及合适的 bounds、NC 诊断、索引/编译秒数、峰值内存/存储、在线 p50/p95、tokens/windows/calls、failure/timeout rate、更新成本（若执行）与固定查询量下的摊销。只在实测范围内讨论 scaling trend，不用几个规模点声称渐近复杂度已被证明。

### 21.5 停止与解释规则

先完成当前 B+C。未来扩展需单独通过来源、标签边界、representation fidelity 和预算 preflight；任何大规模扩展不成为本轮 thesis 完成的前置条件。超预算时按预设边界停止并报告可行性，不根据精度输赢保留方法。

若某方法质量保持但成本陡升，报告受测范围的质量–成本限制；若 graph/wiki 离线贵但线上便宜，给出实际摊销，而非一句“不 scalable”；若小系统只在当前库有效，保留限定结论；若长上下文在可行预算内更强，也如实报告。第一矩阵的科学价值不依赖未来扩展、复杂架构或自研系统一定胜出。
