# **Revised Introductory Literature Review** **for Skill Retrieval in Personal AI Agents**

## *Prepared for supervisor discussion. Focus: scalable skill representation and retrieval in large agent skill libraries.*

*Current proposed research questions are included in Section 4\.*

| Working position. The literature now suggests that the central bottleneck is not merely context explosion from many skills, but the inability of current systems to accurately distinguish semantically similar yet procedurally different skills at scale. This reframes the project from generic tool scaling toward structure-aware skill representation and retrieval. |
| :---- |

# **1\. Project Context and Purpose**

The broader project context is the development of a personal AI agent that can be extended with reusable skills. In principle, skills allow the agent to reuse procedures rather than solving every task from scratch. However, most current agent systems still assume that users can curate skills carefully, write effective descriptions, and keep the capability library manageable. That assumption becomes weak in realistic personal-agent settings, where users may accumulate many overlapping skills over time without a principled way to organise or retrieve them.

This creates a practical research motivation. If a personal agent accumulates a large skill library, naïvely exposing all skills to the model can increase context length, token cost, and routing difficulty. More importantly, the agent may fail even when the correct skill exists, because multiple skills can look semantically similar while encoding different procedures, preconditions, or execution constraints. The aim of this review is therefore to refine the research problem from broad capability scaling into a narrower question about scalable skill representation and retrieval.

# **2\. Background**

Recent LLM agents have evolved from pure text generators into modular systems that combine reasoning, memory, external retrieval, and action. Retrieval-Augmented Generation (RAG) showed that models can improve performance by retrieving external documents at inference time rather than relying solely on parametric memory (Lewis et al., 2021). Later work such as Atlas further demonstrated that retrieval can be tightly integrated with generation for knowledge-intensive tasks (Izacard et al., 2022).

A second development was tool-augmented language modelling. Toolformer showed that models can learn when to call external APIs (Schick et al., 2023), while Gorilla and ToolLLM demonstrated that language models can interact with very large API ecosystems (Patil et al., 2023; Qin et al., 2023). These systems established that external capabilities can be treated as retrievable resources, but they mostly focus on atomic tools or APIs rather than higher-level procedures.

More recent work introduces agent skills as a distinct abstraction. Anthropic’s Agent Skills documentation describes skills as reusable folders of instructions, scripts, and resources that Claude can discover and use when relevant (Anthropic, 2025a). The public skills repository uses the same framing, emphasizing dynamic loading for specialised tasks (Anthropic, 2025c). Survey and SoK papers now position skills as procedural modules or reusable procedural memory, distinguishing them from lower-level callable tools (Jiang, Zhang, Li, et al., 2026; Jiang, Li, Deng, et al., 2026).

This distinction matters for the present project. Tools primarily represent capabilities such as functions or APIs. Skills, by contrast, can package triggering conditions, instructions, scripts, tool interactions, and workflow structure (Anthropic, 2025a, 2025b; Jiang, Zhang, Li, et al., 2026). As a result, simply adapting tool retrieval methods to skills may be insufficient, because skills introduce a stronger need to model procedural suitability rather than only semantic relevance (Jiang, Li, Deng, et al., 2026).

# **3\. Problem Motivation and Identified Limitation**

The initial project question was how to build a personal agent that remains usable as more tools or skills are added. The introductory review suggested two broad difficulties. First, large capability libraries can cause context explosion: if many descriptions are exposed directly in the prompt, inference cost grows and practical context limits are stressed (Anthropic, 2025a; Schick et al., 2023). Second, selection performance degrades as the number of capabilities grows, especially when several candidates are semantically similar (Qin et al., 2023; Li, 2026).

After reviewing newer skill-specific papers, the research problem can be made more precise. The core failure is not simply that there are too many skills. Rather, current systems often treat skills as flat textual items, even though skills are higher-level procedural objects (Jiang, Zhang, Li, et al., 2026; Jiang, Li, Deng, et al., 2026). This creates a mismatch between representation and retrieval. A flat description may be sufficient when skills are few and clearly separated, but it becomes unreliable when the library is large, redundant, noisy, or semantically dense (Ling et al., 2026; Li, X., Chen, Liu, et al., 2026).

Recent evidence strengthens this diagnosis. The paper *When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail* reports that skill-selection accuracy can remain stable up to a critical library size and then drop sharply, with semantic confusability playing a central role (Li, 2026). *SkillsBench* similarly shows that smaller, focused skill sets outperform larger comprehensive ones, even though curated skills are helpful overall (Li, X., Chen, Liu, et al., 2026). The new marketplace analysis of Claude skills finds heavy-tailed length distributions, strong intent-level redundancy, and supply-demand mismatches, suggesting that real skill ecosystems are noisy rather than cleanly structured (Ling et al., 2026). Together, these findings imply that scalable skill retrieval is not a standard similarity-search problem; it must cope with redundancy, overlap, and procedural distinctions.

# **4\. Revised Research Questions**

The project has therefore been reframed away from generic tool scaling and toward scalable skill retrieval. The revised questions are designed to capture both the core failure mode and the candidate intervention.

Research Question 1: How can agent skills be represented and retrieved so that agents can accurately select among semantically similar but procedurally distinct skills as skill libraries scale?

Research Question 2: To what extent do structure-aware skill representations improve retrieval accuracy, context efficiency, and downstream task performance compared with flat description-based skill retrieval?

## **4.1 How these questions were developed**

These questions were developed through iterative narrowing. The initial concern was performance degradation in large capability libraries. However, the background literature already shows that broad issues such as context growth and selection difficulty are known. The newer skill literature then suggested a sharper distinction: skills should not be treated as interchangeable with tools, because they encode reusable procedures. At that point, the central research gap became clearer. Existing work either diagnoses the scaling problem, proposes partial organisation mechanisms such as hierarchy or graphs, or studies the skill ecosystem empirically, but does not fully solve runtime disambiguation between semantically similar yet operationally different skills. This led to a final formulation in which RQ1 defines the problem and RQ2 defines the mechanism to be evaluated.

# **5\. Existing Approaches Relevant to the New Questions**

## **5.1 Flat or prompt-based skill exposure**

Early skill systems often expose skills directly in the prompt. *SkillAct* shows that reusable skill abstractions can improve LLM agents, but the approach still relies on a flat list of textual skills, with no dedicated retrieval or routing layer (Liu et al., 2024). Voyager likewise benefits from a growing skill library, yet retrieval remains relatively simple and description-driven. These systems motivate the current project because they show that skills are useful, but also expose the weakness of flat prompt-level retrieval when libraries become large (Liu et al., 2024; Jiang, Zhang, Li, et al., 2026).

**Limitation.** Flat skill exposure is not scalable as all skills’ description must be consist within the prompt and greatly restrict the context windows for LLMs to operate. Additionally, flat descriptions assume that the model can infer the right procedure from a small amount of text. This becomes unreliable when multiple skills share vocabulary or high-level intent while differing in method, preconditions, or tool usage (Li, 2026; Ling et al., 2026).

## **5.2 Embedding-based retrieval**

A common response to large capability libraries is to encode queries and capability descriptions as embeddings and retrieve the nearest candidates. This general pattern appears in tool-oriented work such as ToolReAGt, ToolDreamer, ToolGen, and related RAG-style tool retrieval pipelines. These methods are attractive because they reduce prompt size and support top-k filtering before generation (Schick et al., 2023; Patil et al., 2023; Qin et al., 2023).

**Limitation.** Embedding retrieval usually treats capabilities as independent text items. This is problematic for skills, because semantic similarity does not guarantee procedural equivalence. A retrieval model may return the wrong skill when two skills look lexically similar but differ materially in execution (Jiang, Zhang, Li, et al., 2026; Li, 2026).

## **5.3 Graph-based or relational skill organization**

Graph-based approaches try to model relationships explicitly rather than relying only on vector similarity. *SciToolAgent* uses a scientific tool knowledge graph to capture dependencies between tools in multi-step workflows. The newly released *SkillNet* extends this idea to skills: it introduces an infrastructure with more than 200,000 skills, multi-dimensional evaluation, and a skill relation graph supporting similarity, dependency, and composition links (Liang et al., 2026). These papers are useful because they challenge the assumption that skill libraries should be treated as flat sets (Liang et al., 2026).

**Limitation.** Current graph-oriented systems mainly improve organisation and infrastructure. They do not yet provide a fully developed runtime retrieval and routing algorithm that is clearly optimised for selecting the right skill under semantic confusability. Graph construction can also be heuristic, static, and expensive to maintain (Liang et al., 2026; Ling et al., 2026).

## **5.4 Hierarchical and structured retrieval**

Hierarchical retrieval reduces the search space by organising capabilities into coarse-to-fine structures. *AgentSkillOS* is the closest paper to the present topic: it builds a capability tree, retrieves relevant branches, and orchestrates multiple skills via DAG-based pipelines across libraries ranging from 200 to 200,000 skills (Li, H., Mu, Chen, et al., 2026). More generally, LATTICE demonstrates that hierarchical traversal can outperform flat retrieval in reasoning-heavy search by calibrating local relevance scores along a path.

**Limitation.** Pure trees can create routing errors. If the system makes a wrong early branch decision, relevant skills may never be seen. They also struggle when one skill belongs naturally to multiple categories. *AgentSkillOS* itself still assumes that skills can be organised into a capability tree and does not fully resolve the problem of semantically similar but procedurally distinct skills (Li, H., Mu, Chen, et al., 2026; Li, 2026).

## **5.5 Ecosystem-level and diagnostic analyses**

Several recent papers are particularly important because they do not merely propose mechanisms; they reveal what real skill ecosystems look like. The data-driven analysis of Claude skills studies 40,285 public skills and reports strong redundancy, heavy-tailed skill lengths, and safety-relevant behaviours (Ling et al., 2026). The *Agent Skill Framework* paper studies whether small language models can benefit from skills in industrial settings and finds that skill selection is the main bottleneck, with performance dropping as the number of available skills increases (Xu et al., 2026). *SkillsBench* provides benchmark evidence that curated skills help overall, but large and unfocused skill sets can still hurt outcomes (Li, X., Chen, Liu, et al., 2026).

**Limitation.** These works are primarily diagnostic. They justify the importance of the problem, but they do not give a strong solution to runtime skill retrieval and ranking (Ling et al., 2026; Xu et al., 2026).

# **6\. Representative Papers Mapped to the Revised Research Questions**

The assignment asks for about five core sources per research question. The same paper can legitimately support both questions where appropriate.

| Research question | Most relevant papers | Why they matter |
| :---- | :---- | :---- |
| RQ1 | When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail; SkillsBench; SkillAct; Voyager; Agent Skills from the Perspective of Procedural Memory | These papers define the failure mode: skill selection degrades with scale, semantic confusability matters, and skills differ from tools because they encode procedures. |
| RQ2 | AgentSkillOS; SkillNet; SciToolAgent; LATTICE; Agent Skills: A Data-Driven Analysis of Claude Skills | These papers motivate structure-aware retrieval by showing the limits of flat libraries and the potential value of hierarchy, graphs, and ecosystem-aware organisation. |

# **7\. Questions for Supervisor Discussion**

* Is the current framing sufficiently narrow if the thesis focuses specifically on skill retrieval rather than general tool retrieval?  
* Would it be considered a strong honours contribution to adapt and extend a retrieval idea from tool retrieval if the novelty is framed around procedural skill structure?  
* Would it be better to position the work as a method paper with a small benchmark/evaluation protocol, rather than as a benchmark-first project?  
* Are the current research questions appropriately scoped for the project timeline, or should one be narrowed further into a single technical mechanism?

# **References (selected)**

Anthropic. (2024). Introducing the Model Context Protocol.

Anthropic. (2025). Agent Skills \- Claude API Docs.

Anthropic. (2025). Skill authoring best practices \- Claude API Docs.

Anthropic. (2025). Public repository for Agent Skills.

Izacard, G., Grave, E., & Riedel, S. (2022). Atlas: Few-shot learning with retrieval augmented language models.

Lewis, P., Perez, E., Piktus, A., et al. (2021). Retrieval-augmented generation for knowledge-intensive NLP tasks.

Li, H., Mu, C., Chen, J., et al. (2026). Organizing, orchestrating, and benchmarking agent skills at ecosystem scale.

Li, X. (2026). When single-agent with skills replace multi-agent systems and when they fail.

Li, X., Chen, W., Liu, Y., et al. (2026). SkillsBench: Benchmarking how well agent skills work across diverse tasks.

Liang, Y., Zhong, R., Xu, H., et al. (2026). SkillNet: Create, evaluate, and connect AI skills.

Ling, G., Zhong, S., & Huang, R. (2026). Agent skills: A data-driven analysis of Claude skills for extending large language model functionality.

Liu, A. Z., Choi, J., Sohn, S., et al. (2024). SkillAct: Using skill abstractions improves LLM agents.

Patil, S., Zhang, T., Wang, X., & Gonzalez, J. E. (2023). Gorilla: Large language model connected with massive APIs.

Qin, Y., Liang, S., Ye, Y., et al. (2023). ToolLLM: Facilitating large language models to master 16,000+ real-world APIs.

Schick, T., Dwivedi-Yu, J., Dessì, R., et al. (2023). Toolformer: Language models can teach themselves to use tools.

Xu, Y., Li, L., Sleem, L., et al. (2026). Agent skill framework: Perspectives on the potential of small language models in industrial environments.

Jiang, Y., Zhang, X., Li, Z., et al. (2026). Agent skills from the perspective of procedural memory: A survey.

Jiang, Y., Li, D., Deng, H., et al. (2026). SoK: Agentic skills \- Beyond tool use in LLM agents.