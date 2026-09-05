## **Context and Summaries:**

## 

## 

	Recent advances in AI agents have enabled language models to interact with external tools, services, and predefined skills in order to perform complex tasks. Systems such as agent frameworks allow users to extend the capabilities of an agent by adding new tools or skills. However, most existing agent systems assume that users have the expertise to design efficient agent workflows and select appropriate tools. In practice, many potential users of personal AI agents may not have a technical background in prompt engineering, programming, or agent system design.

As a result, non-technical users may simply add a large number of tools or skills to their agents without understanding the trade-offs between them. This behaviour can lead to several problems. First, the descriptions of all available tools are often included in the prompt context, which can cause context explosion as the number of tools grows. Second, large tool libraries may degrade the agent’s ability to select the correct tool, resulting in reduced task performance. Third, longer prompts significantly increase token usage and computational cost, making even simple tasks unnecessarily expensive.

These challenges highlight the need for mechanisms that allow AI agents to scale efficiently when interacting with large tool libraries.

**Research Question 1**

How can performance degradation in AI agents be minimized when the number of available tools or skills becomes large (e.g., due to context explosion)?

### **Research Question 2**

What architectural mechanisms can improve scalable tool/skills retrieval and selection in AI agents with large tool libraries?

### 

**Question to clarify:** 

**Although tools and skills are conceptually related, they operate at different levels of abstraction. Tools typically represent lower-level capabilities such as APIs or functions, while skills encapsulate higher-level workflows that may combine instructions, multiple tools, and task-specific procedures. My research intends to focus on skill retrieval rather than tool retrieval. However, many existing approaches for capability selection and retrieval have primarily been developed in the context of tool retrieval. This raises several questions for my research direction. First, if a method originally designed for tool retrieval is adapted to skill retrieval, would this still constitute a meaningful research contribution, given that skills may introduce different challenges (e.g., semantically similar descriptions but significantly different underlying workflows)? Second, if some researchers consider tool retrieval and skill retrieval to be essentially similar problems, how should the novelty of such work be framed? Finally, given that this is a rapidly evolving area, how should the research question be positioned to remain meaningful if similar ideas are published during the course of this project?**

### 

### 

# Introductory Literature Review:

# **1\. Background**

Artificial intelligence (AI) agents are systems that perceive their environment, reason about tasks, and perform actions in order to achieve specific goals. In classical artificial intelligence, agents are typically defined as autonomous decision-making entities that interact with their environments through sensing, reasoning, and action execution. Recent advances in large language models (LLMs) have extended this concept to **LLM-based agents**, in which language models serve as the central reasoning component while interacting with external systems. Recent surveys describe modern AI agents as modular systems that combine large models with reasoning loops, memory mechanisms, and interfaces for interacting with external environments and tools (Sapkota et al., 2026).

With the emergence of large language models, researchers have increasingly explored ways to extend model capabilities through **access to external knowledge sources**. One important direction is retrieval-augmented language models. Retrieval-Augmented Generation (RAG) demonstrates that language models can improve performance on knowledge-intensive tasks by retrieving relevant documents from external corpora during inference rather than relying solely on parametric knowledge stored in model weights (Lewis et al., 2021). Instead of generating responses purely from internal model knowledge, the generation process is conditioned on retrieved evidence. Subsequent work such as Atlas further demonstrates that retrieval-augmented architectures can achieve strong few-shot performance by jointly training a neural retriever and a language model (Izacard et al., 2022). These results highlight the importance of external information access mechanisms for extending the capabilities of language models.

Beyond accessing external knowledge, recent research has explored how language models can interact with **external tools and services** in order to perform actions rather than only retrieve information. While retrieval-augmented language models focus on retrieving documents or textual evidence to improve knowledge-intensive tasks, many real-world applications require agents to **execute functions, query databases, run programs, or interact with external systems**. In these scenarios, retrieving information alone is insufficient; the agent must invoke external capabilities that perform computations or actions.

Several studies have investigated mechanisms that enable language models to interact with such tools. One influential approach is Toolformer, which demonstrates that language models can learn to invoke external APIs through self-supervised training (Schick et al., 2023). In this framework, the model learns when to insert API calls during generation and how to incorporate the returned results into subsequent reasoning steps. Subsequent systems explored tool interaction at much larger scales. For example, Gorilla connects language models to thousands of APIs by retrieving relevant API documentation and generating structured tool invocations (Patil et al., 2023). Similarly, ToolLLM studies tool selection in environments where agents must choose from more than 16,000 available APIs, highlighting the challenges of operating in large tool ecosystems (Qin et al., 2023). These studies demonstrate that language model agents can operate in environments with **very large tool spaces**, raising new challenges for scalable capability selection and orchestration.

Recent industry systems have also introduced standardized protocols and abstractions for managing such capabilities. The Model Context Protocol (MCP) provides a standardized interface for connecting language models with external tools and services, enabling agents to dynamically discover and invoke functions provided by external systems (Anthropic, 2024).

More recently, the concept of **agent skills** has emerged as a higher-level abstraction for organizing agent capabilities. Rather than invoking individual tools directly, skills encapsulate reusable workflows composed of instructions, tools, and task-specific resources. Recent research suggests that skills can serve as modular capability units that structure how agents interact with tools and environments (Jiang et al., 2026). Other studies further explore how such skills can be organized and orchestrated within larger agent ecosystems (Li et al., 2026). In practice, industry systems have begun to formalize this abstraction. For example, Anthropic’s Agent Skills framework packages instructions, scripts, and tool integrations into reusable capability modules that can be dynamically loaded by agents (Anthropic, 2025).

Together, these developments illustrate a broader evolution in AI agent systems. Early work focused on enabling language models to access external knowledge through retrieval mechanisms. Subsequent systems introduced methods for interacting with large tool ecosystems. More recent approaches further abstract these capabilities into reusable skills that can be composed and orchestrated within agent systems. However, as the number of available tools and skills grows, selecting the appropriate capability becomes increasingly challenging. This motivates research on scalable mechanisms for organizing and retrieving capabilities within large agent systems.

	

# **2\. Problem Motivation**

**While recent research has significantly expanded the capabilities of AI agents through external knowledge retrieval, tool interaction, and skill abstractions, these developments also introduce new scalability challenges. In many agent systems, the set of available tools or skills must be described within the model’s prompt context so that the language model can reason about which capability to invoke. For example, recent agent frameworks expose tools or skills to the model through structured descriptions or prompt-based skill definitions that are loaded into the model context during execution (Anthropic, 2025). Similarly, prior work on tool-augmented language models notes that tool descriptions are often included directly in the model input context, which limits scalability due to the restricted context window of large language models (ToolGen, 2024). As the number of available capabilities increases, including all tool descriptions in the prompt can substantially increase the prompt length, potentially exceeding the context window and leading to higher token consumption and reduced inference efficiency (ToolDreamer, 2025).**

**In addition to increased computational costs, large capability libraries introduce significant challenges for capability selection. As the number of available tools or skills grows, language models must choose among many candidate capabilities that often provide overlapping or semantically similar functionality. Prior work has shown that this selection problem becomes increasingly difficult in large tool ecosystems, where models may fail to invoke the most appropriate API or tool for a given task. Empirical studies further suggest that capability selection performance can degrade as the number of available options increases, particularly when tools or skills are semantically similar (Li, 2026). Benchmarking efforts such as StableToolBench also highlight the difficulty of reliable tool invocation across large tool collections, demonstrating substantial instability in tool selection performance for current language models (Guo et al., 2025).**

**In recent years, agent ecosystems have continued to expand, incorporating increasingly large collections of reusable capabilities. To improve modularity and reuse, several systems have begun to organize agent capabilities as reusable skills that can be dynamically loaded and executed (Jiang et al., 2026; Li et al., 2026). In such architectures, complex behaviors are encapsulated as modular units that may combine instructions, external tools, and execution policies, allowing agents to reuse and compose capabilities across tasks. However, as skill libraries grow, the agent must select the appropriate capability from an increasingly large and semantically overlapping set of skills, making reliable capability selection more difficult. These challenges motivate the need for scalable mechanisms that allow AI agents to efficiently organize, retrieve, and select capabilities from large tool or skill libraries.**

# **3\. Research Questions**

**Research Question 1**  
 How can performance degradation in AI agents be minimized when the number of available skills becomes large (e.g., due to context explosion/semantic confusion)?

This question focuses on understanding and mitigating the scalability challenges that arise when AI agents operate with many skills and large capability libraries. In many existing agent systems, skills descriptions are included in the prompt context so that the language model can select the appropriate capability. As the number of available tools or skills increases, this may lead to larger prompts, higher token costs, and reduced tool-selection accuracy. This research question therefore investigates potential mechanisms for reducing performance degradation caused by large capability libraries.

**Research Question 2**  
 What architectural mechanisms can improve scalable skills retrieval and selection in AI agents with large tool libraries?

This question explores architectural approaches that can enable agents to efficiently retrieve and select relevant tools or skills from large capability libraries. Possible directions include retrieval-based filtering, structured capability organization, and skill abstraction mechanisms. This research question aims to evaluate how different architectural designs affect the scalability and efficiency of tool or skill selection.

# **4\. Existing Approaches:**

4\. Existing Approaches for Capability Retrieval

As the number of available tools or skills increases, researchers have proposed several approaches to enable language models to efficiently retrieve and select relevant capabilities. Existing work can be broadly categorized into four main directions: embedding-based retrieval, graph-based retrieval, skill library architectures, and tool learning approaches.

## **4.1 Embedding-Based Retrieval**

Embedding-based retrieval is one of the most widely used strategies for capability selection in agent systems. In this approach, both user queries and capability descriptions are encoded into vector embeddings, and similarity search is used to retrieve the most relevant candidates from a capability library.

Several existing works apply this paradigm to **tool retrieval**. For example, ToolReAGt integrates retrieval-augmented generation with ReAct-style reasoning, enabling agents to iteratively retrieve relevant tools during complex task solving **(Braunschweiler et al., 2025\)**. Similarly, Toolshed proposes a scalable architecture that combines vector databases with query rewriting and post-retrieval refinement to support retrieval from large tool ecosystems **(Toolshed, 2024\)**.

While embedding-based retrieval has been widely explored in the context of tool ecosystems, relatively little work investigates its application to skill libraries. In many existing skill-based systems, capabilities are provided directly to the language model without a dedicated retrieval layer **(Li, 2026\)**.

### **Limitations**

Embedding-based retrieval treats capabilities as independent items and relies primarily on semantic/key word similarity between query and capability descriptions. As capability libraries grow, tools or skills may become semantically similar or partially overlapping, increasing the likelihood of retrieval ambiguity. Prior work has also shown that capability selection accuracy can degrade as the number of available skills increases when capabilities are organized in flat libraries **(Li, 2026\)**.

---

# **4.2 Graph-Based Retrieval**

Graph-based retrieval approaches represent capabilities and their relationships as structured graphs, enabling retrieval through graph traversal and structured reasoning rather than relying solely on vector similarity. In these approaches, capabilities such as tools, agents, or skills are modeled as nodes in a graph, while edges capture relationships including semantic similarity, functional dependencies, or execution workflows.

Several recent studies apply graph-based retrieval to **tool ecosystems**. For example, *Agent-as-a-Graph* represents agents and tools within a knowledge graph and performs capability retrieval using a hybrid approach that combines embedding similarity with graph traversal. After retrieving candidate nodes using vector search, the system explores graph relationships to identify relevant agents or tools for task execution (Nizar et al., 2025). Similarly, *SciToolAgent* constructs a scientific tool knowledge graph that connects hundreds of specialized research tools across domains such as biology, chemistry, and materials science. The system uses graph-based retrieval-augmented generation to support tool selection and orchestration for complex scientific workflows (Ding et al., 2025).

Related ideas also appear in **knowledge-graph-based retrieval-augmented generation frameworks**, where structured graphs guide the retrieval process. For instance, KG-RAG organizes information in a knowledge graph and performs retrieval through graph exploration, allowing language models to retrieve semantically related nodes through multi-hop reasoning rather than relying purely on embedding similarity (Sanmartin, 2024). Although KG-RAG is primarily designed for knowledge retrieval rather than tool or skill selection, it demonstrates how graph structures can improve retrieval by explicitly modeling relationships between entities.

Overall, existing graph-based retrieval systems have mainly been explored in the context of **tool retrieval**. However, the same principles could potentially be extended to **skill libraries**, where relationships between skills—such as compositional dependencies or semantic similarity—may also be represented using structured graphs.

### **Limitations**

Despite their potential advantages, graph-based retrieval approaches introduce additional system complexity. Constructing and maintaining capability graphs can be costly, particularly when capability libraries evolve dynamically and new tools or skills are frequently added. Furthermore, many existing graph-based retrieval systems still rely on embedding similarity as an initial retrieval step before graph traversal, meaning their performance remains partially dependent on the quality of embedding representations.

---

## **4.3 Hierarchical and Structured Retrieval**

Another line of research explores hierarchical organization as a way to scale capability retrieval beyond flat libraries. Instead of retrieving capabilities directly from an undifferentiated pool, hierarchical approaches organize capabilities into structured categories and perform selection in a coarse-to-fine manner.

Recent work has begun to apply this idea explicitly to **skill ecosystems**. For example, *AgentSkillOS* organizes large skill collections into a **capability tree** through recursive categorization, and then uses this tree to support task-driven skill retrieval and downstream multi-skill orchestration. In this framework, the agent first navigates the hierarchy to identify relevant capability regions, and then prunes, deduplicates, and ranks candidate skills before execution. The system further composes retrieved skills into **DAG-based orchestration plans**, enabling structured multi-skill execution at ecosystem scale (Li et al., 2026).

A complementary perspective is provided by *When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail*, which analyzes the limitations of **flat skill libraries**. That work shows that as the number of available skills increases, selection accuracy degrades non-linearly, especially when skills are semantically confusable. It further argues that **hierarchical routing** can mitigate this degradation by decomposing skill selection into coarse-to-fine decisions rather than forcing the model to select directly from a large flat library (Li, 2026).

Taken together, these studies suggest that hierarchical structure can help capability selection in two ways: first, by reducing the effective search space during retrieval; and second, by improving coordination among multiple retrieved skills through structured orchestration rather than flat invocation.

### **Limitations**

Despite their potential benefits, hierarchical capability organization introduces several practical challenges. First, constructing an effective hierarchy typically requires either manual design or heuristic clustering methods. Determining the optimal way to partition skills into hierarchical categories can be difficult, particularly when skill semantics are ambiguous or overlap significantly. Poor hierarchy construction may lead to inaccurate grouping and reduce retrieval effectiveness.

Second, pure hierarchical structures may introduce **routing errors during capability selection**. Because hierarchical retrieval often follows a coarse-to-fine selection process, an incorrect decision at an early stage can prevent the system from considering relevant skills located in other branches of the hierarchy.

Finally, many capabilities may naturally belong to multiple functional categories. However, strict tree-based hierarchies usually place each skill in only a single branch. When a skill is assigned to only one subtree, queries routed to a different branch may never retrieve that skill, even if it would be the most appropriate capability for the task.

These limitations suggest that while hierarchical structures can improve scalability, additional mechanisms—such as multi-parent capability representations or hybrid retrieval strategies—may be required to support robust capability selection in large skill libraries.

References

Anthropic. (2024).  
Model context protocol. [https://modelcontextprotocol.io](https://modelcontextprotocol.io/)

Anthropic. (2025).  
Agent skills documentation. [https://www.anthropic.com/engineering/agent-skills](https://www.anthropic.com/engineering/agent-skills)

Braunschweiler, N., Doddipatla, R., & Zorila, T.-C. (2025).  
ToolReAGt: Tool retrieval for LLM-based complex task solution via retrieval augmented generation.  
Proceedings of the ACL 2025 Workshop on Knowledge-Enhanced Foundation Models (KnowFM).

Ding, K., Yu, J., Huang, J., Yang, Y., Zhang, Q., & Chen, H. (2025).  
SciToolAgent: A knowledge graph-driven scientific agent for multi-tool integration.  
arXiv preprint arXiv:2507.20280. [https://doi.org/10.48550/arXiv.2507.20280](https://doi.org/10.48550/arXiv.2507.20280)

Guo, Z., Cheng, S., Wang, H., Liang, S., Qin, Y., Li, P., Liu, Z., Sun, M., & Liu, Y. (2025).  
StableToolBench: Towards stable large-scale benchmarking on tool learning of large language models.  
arXiv preprint arXiv:2403.07714. [https://doi.org/10.48550/arXiv.2403.07714](https://doi.org/10.48550/arXiv.2403.07714)

Izacard, G., Grave, E., & Riedel, S. (2022).  
Atlas: Few-shot learning with retrieval augmented language models.  
arXiv preprint arXiv:2208.03299.

Jiang, Y., Zhang, X., Li, Z., et al. (2026).  
Agent skills from the perspective of procedural memory: A survey.  
arXiv preprint.

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2021).  
Retrieval-augmented generation for knowledge-intensive NLP tasks.  
Proceedings of the 34th Conference on Neural Information Processing Systems (NeurIPS).

Li, H., Mu, C., Chen, J., Ren, S., Cui, Z., Zhang, Y., Bai, L., & Hu, S. (2026).  
Organizing, orchestrating, and benchmarking agent skills at ecosystem scale.  
arXiv preprint.

Li, X. (2026).  
When single-agent with skills replace multi-agent systems and when they fail.  
arXiv preprint arXiv:2601.04748.

Nizar, A., et al. (2025).  
Agent-as-a-Graph: Knowledge graph-based tool and agent retrieval.  
arXiv preprint.

Patil, S., Zhang, T., Wang, X., & Gonzalez, J. E. (2023).  
Gorilla: Large language model connected with massive APIs.  
arXiv preprint arXiv:2305.15334. [https://doi.org/10.48550/arXiv.2305.15334](https://doi.org/10.48550/arXiv.2305.15334)

Qin, Y., Liang, S., Ye, Y., Zhu, K., Yan, L., Lu, Y., Lin, Y., Cong, X., Tang, X., Qian, B., Zhao, S., Hong, L., Tian, R., Xie, R., Zhou, J., Gerstein, M., Li, D., Liu, Z., & Sun, M. (2023).  
ToolLLM: Facilitating large language models to master 16,000+ real-world APIs.  
arXiv preprint arXiv:2307.16789. [https://doi.org/10.48550/arXiv.2307.16789](https://doi.org/10.48550/arXiv.2307.16789)

Sanmartin, A. (2024).  
KG-RAG: Knowledge graph retrieval augmented generation.  
arXiv preprint.

Sapkota, S., et al. (2026).  
AI agents vs. agentic AI: A conceptual taxonomy, applications, and challenges.  
arXiv preprint.

Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023).  
Toolformer: Language models can teach themselves to use tools.  
Advances in Neural Information Processing Systems (NeurIPS).

Toolshed. (2024).  
Toolshed: Scale tool-equipped agents with advanced RAG-tool fusion and tool knowledge bases.  
arXiv preprint.

ToolDreamer. (2025).  
ToolDreamer: Learning to retrieve and utilize tools for language model agents.  
arXiv preprint.

ToolGen. (2024).  
ToolGen: Unified tool retrieval and calling via generation.  
arXiv preprint.

# **1️⃣ Vector / Embedding Tool Retrieval（最基础）**

这是目前 **最常见的 baseline**。

思想：

query embedding  
→ similarity search  
→ top-k tools

典型工作：

### **ToolRAG / Tool retrieval frameworks**

* **ToolReAGt: Tool Retrieval for LLM-based Complex Task Solution via RAG (2025)**  
   核心：  
   用 **RAG \+ ReAct** 逐步检索工具。

关键思想：

query  
→ retrieve candidate tools  
→ LLM reasoning  
→ refine retrieval  
---

### **Toolshed (2024)**

* **Toolshed: Scale Tool-Equipped Agents with Advanced RAG-Tool Fusion**

贡献：

vector database  
\+ query rewriting  
\+ post-retrieval refinement

专门研究：

large tool library retrieval

并且实验比较：

|tools| vs retrieval accuracy  
---

# **2️⃣ Knowledge Graph Retrieval**

这是你现在最接近的方向。

### **Agent-as-a-Graph (2025)**

论文：

Agent-as-a-Graph: Knowledge Graph-Based Tool and Agent Retrieval

核心：

vector retrieval  
→ graph traversal  
→ ranking

系统：

agents \+ tools  
→ knowledge graph

实验结果：

Recall@5 \+14.9%  
nDCG@5 \+14.6%

这是目前 **最接近你 idea 的 paper**。

---

# **3️⃣ GraphRAG / Graph Retrieval**

这类 paper 不是专门做 tools，但 retrieval 思路很类似。

### **KG-RAG**

论文：

KG-RAG: Knowledge Graph Retrieval Augmented Generation

核心：

LLM \+ knowledge graph reasoning

算法：

Chain-of-Explorations

流程：

query  
→ seed nodes  
→ graph exploration  
→ answer

这和你说的：

RAG seed  
→ graph traversal

几乎一样。

---

# **4️⃣ Skill Library Retrieval**

这个方向 **paper 很少**（你 thesis 的潜在 gap）。

### **SkillRL (2026)**

论文：

SkillRL: Recursive Skill-Augmented RL

核心：

hierarchical skill library

结构：

SkillBank

支持：

skill retrieval  
task-specific heuristics

并且：

skills evolve over time

这个是 **skills retrieval 的少数论文**。

---

# **5️⃣ Tool Learning / API Retrieval**

另一类相关研究。

### **Toolformer (2023)**

核心：

LLM self-annotates API calls

训练：

teach LLM to choose tools  
---

### **Gorilla (2023)**

核心：

retrieve APIs  
from documentation

目标：

correct API invocation  
---

# **6️⃣ Tool Benchmark / Retrieval Benchmark**

这类 paper 不提出 algorithm，而是提供 evaluation。

### **ToolRet benchmark**

论文：

A Comprehensive Benchmark for Tool-Augmented LLMs

包含：

7.6k tool retrieval tasks

用于评估：

tool retrieval accuracy  
---

# **7️⃣ Agentic RAG**

这是更 general 的 retrieval architecture。

### **Agentic RAG Survey (2025)**

提出 taxonomy：

agent planning  
tool retrieval  
external knowledge retrieval

总结：

agents rely on retrieval layer  
to select tools or knowledge  
---

# **8️⃣ 总结：主流 retrieval approaches**

目前 literature 基本分为：

| Retrieval type | Example papers |
| ----- | ----- |
| embedding retrieval | ToolReAGt |
| vector DB \+ RAG | Toolshed |
| knowledge graph retrieval | Agent-as-a-Graph |
| graph-based reasoning | KG-RAG |
| skill library retrieval | SkillRL |
| tool learning | Toolformer, Gorilla |
| benchmark | ToolRet |

