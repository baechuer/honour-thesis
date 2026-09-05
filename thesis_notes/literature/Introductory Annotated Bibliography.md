## **1 Background: LLM Agent Architectures**

papers:

* ReAct

* Reflexion

* survey paper

keywords

LLM agents  
agent workflows  
reasoning-action loop  
---

## **2 Tool-Augmented LLMs**

papers:

* Toolformer

* Gorilla

* ToolLLM

keywords

tool use  
API invocation  
tool augmented LLM  
---

## **3 Retrieval-Based Tool Selection**

papers:

* Gorilla

* ToolLLM

* ToolBench

keywords

tool retrieval  
API retrieval  
tool routing  
---

## **4 Skill Libraries and Capability Reuse**

papers:

* Voyager

* Anthropic skills

* AutoSkill

keywords

skill library  
capability reuse  
skill composition  
---

## **5 Scalability Challenges in Tool Ecosystems**

papers:

* skill overload

* tool overload

* context explosion papers

keywords

tool scaling  
skill scaling  
context explosion  
token explosion

# Annotated Bibliography:

###  A Review of Prominent Paradigms for LLM-Based Agents: Tool Use (Including RAG), Planning, and Feedback Learning

**1299th percentileCitations 28.28FWCI**

**Summary**

This survey proposes a unified taxonomy for LLM-based agent architectures by organising existing frameworks into three paradigms: tool use, planning, and feedback learning. The authors introduce the concept of LLM-profiled roles (LMPRs), consisting of policy models, evaluators, and dynamic models, to describe the core components of agent workflows. Based on these roles, the paper categorises common agent workflows including base workflows, tool-use workflows (e.g., RAG and ReAct), search-based planning workflows (e.g., Tree-of-Thoughts and MCTS), and feedback learning frameworks such as Reflexion.

**Evaluation**

The survey provides a useful conceptual framework for understanding the design space of LLM-based agents and clarifies relationships between existing paradigms. However, the contribution is primarily taxonomical and does not introduce new algorithms or empirical evaluations. Furthermore, the proposed LMPR abstraction may oversimplify real-world agent architectures, which often include additional components such as memory systems, tool routers, and retrievers.

**Relevance**

This work is relevant to research on tool-augmented LLM agents because it situates tool-use architectures within a broader agent workflow taxonomy. However, it does not address the scalability challenges of large tool or skill libraries, which remain an open research problem.

### LLM-Based Multi-Agent Decision-Making: Challenges and Future Directions

1798th percentile  
Citations  
Set citation alert  
8.38  
FWCI

Summary

This survey examines the emerging paradigm of LLM-based multi-agent decision-making systems and analyses how multiple language-model agents collaborate to solve complex tasks. The authors review common architectural patterns including hierarchical agents, role-based agents, and collaborative agent systems where agents perform specialised roles such as planners, executors, and evaluators. The paper also discusses the decision-making pipeline of LLM agents, covering stages such as task planning, information retrieval, reasoning, execution, and evaluation. Based on a systematic analysis of recent literature, the authors identify several key challenges in multi-agent systems, including coordination overhead, reasoning consistency, communication complexity, evaluation difficulty, and scalability limitations. The survey further highlights emerging research directions such as verifiable reasoning, self-improving agents, structured communication protocols, and more scalable multi-agent architectures.

Evaluation

The paper provides a structured overview of the design space of LLM-based multi-agent systems and clearly identifies key challenges that arise when scaling collaborative agent architectures. However, the work is primarily conceptual and does not introduce new algorithms or empirical benchmarks. Additionally, the analysis focuses mainly on multi-agent coordination and decision-making, while other practical aspects of agent systems—such as tool routing, memory management, and retrieval mechanisms—are only briefly discussed.

Relevance

This survey is relevant to research on LLM-based agent architectures because it outlines how multiple agents collaborate to perform complex reasoning and decision-making tasks. However, the paper does not directly address the scalability challenges associated with large tool or skill libraries in single-agent systems, which is a central focus of this thesis.

### The Rise and Potential of Large Language Model Based Agents: A Survey

25499th percentile  
Citations  
Set citation alert  
56.39  
FWCI

Summary

This paper presents a comprehensive survey of LLM-based agents, proposing a unified framework that decomposes agents into three core components: brain, perception, and action. The authors trace the evolution of agent systems from symbolic and reactive paradigms to modern LLM-driven agents, and categorize existing work into single-agent systems, multi-agent systems, and human-agent collaboration.

The survey highlights how LLMs function as the central reasoning and decision-making module, while perception and action modules interface with external environments through tools, APIs, or sensors. Additionally, the paper discusses emerging directions such as agent societies, collective intelligence, and real-world deployment challenges.

Evaluation

The paper provides a broad and accessible overview of the LLM agent landscape, and the brain–perception–action framework offers a useful high-level abstraction for organizing existing systems. It effectively summarizes trends and identifies key challenges such as context limitations, safety risks, and the gap between simulated and real-world environments.

However, the contribution is primarily descriptive and lacks technical depth. The proposed framework is overly general and does not capture critical components such as tool or skill selection, retrieval mechanisms, or system-level scalability. Moreover, the survey does not provide formal analysis or empirical evidence for many of its claims, limiting its utility for designing or evaluating concrete agent architectures.

Relevance

This work is relevant as a high-level conceptual background for research on LLM-based agents, particularly in understanding the modular decomposition of agent systems and the role of LLMs as decision-making cores.

However, it does not address the core challenges of scalable tool or skill selection, nor does it provide mechanisms for mitigating context explosion or performance degradation in large agent systems. As such, it serves primarily as contextual background rather than a direct contribution to solving scalability issues in tool or skill retrieval.

### Meta-Agent-Workflow: Streamlining Tool Usage in LLMs through Workflow Construction, Retrieval, and Refinement

397th percentile  
Citations  
Set citation alert  
6.27  
FWCI

Summary

This paper proposes Meta-Agent-Workflow, a framework that improves tool usage in LLM-based agents by converting multi-step tool-use trajectories into reusable workflows. Instead of planning tool calls from scratch for every query, the system first constructs workflows from previously successful tool trajectories and stores them in a workflow library. When a new query arrives, the framework retrieves candidate workflows using embedding-based similarity and then applies LLM-based reranking to select the most suitable workflow for execution. If workflow execution fails due to tool errors or changing APIs, the system performs workflow refinement by analyzing execution logs and generating updated workflow steps. Experiments on ToolBench tasks and several real-world application scenarios show that workflow-based agents can improve tool selection accuracy and provide more stable execution compared to fully dynamic tool planning.

Evaluation

The main strength of the paper lies in shifting the reuse unit from individual tools to structured workflows, which can reduce planning complexity for repetitive or structured tasks. The integration of workflow construction, retrieval, and refinement also provides a practical end-to-end system for industrial deployment. However, the framework primarily targets stable and recurring tasks, and its retrieval mechanism remains relatively simple, relying on embedding recall and LLM reranking. Furthermore, the paper does not investigate how workflow retrieval behaves when the workflow library becomes very large or contains many semantically overlapping workflows.

Relevance

This work is relevant because it demonstrates that reusable workflows can serve as a higher-level abstraction for tool usage in LLM agents, effectively functioning as reusable skills composed of multiple tools. However, it does not directly address the broader scalability challenges of large skill or workflow libraries, such as retrieval degradation or context explosion, which remain open research problems in scalable agent architectures.

### Learning Agent Skills from Demonstrations and Generating Knowledge Graph

Summary

This paper proposes a demonstration-based framework for learning agent skills and generating hierarchical knowledge graphs to improve the interpretability and usability of long-horizon skills. The method first represents complex demonstrations as ordered compositions of six parameterized meta-skills, including Move, Grab, Alignment, Insert, Rotate, and Release. It then uses DeepSeek-based prompting to decompose demonstration skills and generate behavior trees, with a self-verification strategy that executes generated primitives in a simulation environment and iteratively revises the tree based on execution feedback. Finally, the resulting structured skill information is transformed into a Neo4j-based knowledge graph for visualization and hierarchical skill representation. Experiments on 3C assembly and satellite assembly tasks report 92.6% skill decomposition accuracy, 90.7% behavior tree generation accuracy, and 88.7% overall skill graph accuracy.

Evaluation

The main strength of the paper is that it moves beyond raw demonstration trajectories and converts them into structured, interpretable skill representations using hierarchical decomposition, behavior trees, and knowledge graphs. The integration of LLM-based decomposition with simulator-based verification is also more grounded than purely text-based planning approaches. However, the framework depends on a predefined meta-skill vocabulary and is heavily tailored to robotic assembly tasks. In addition, the knowledge graph mainly functions as an organizational and visualization layer rather than a scalable retrieval or reasoning mechanism.

Relevance

This work is relevant because it shows that complex skills can be decomposed into hierarchical components and organized into structured knowledge representations rather than stored as flat trajectories. It is useful for motivating skill structuring and hierarchical skill organization. However, it does not directly address scalable skill retrieval, routing, or overload problems in LLM-based agent systems with large skill libraries.

### Agent Skills from the Perspective of Procedural Memory: A Survey

Summary

This survey provides the first systematic overview of LLM-based Agent Skills, conceptualizing them as a form of procedural memory that enables agents to reuse task-solving procedures rather than repeatedly relying on ad-hoc reasoning. The paper proposes a unified framework that characterizes Agent Skills through four key stages: skill acquisition, representation, invocation, and refinement. It reviews representative implementations such as Voyager, SkillAct, CASCADE, and SkillWeaver, and categorizes skills based on how they are learned (e.g., demonstrations, exploration, or experience distillation), represented (e.g., prompts, programs, APIs, or procedural memories), and invoked during task execution. The survey also discusses real-world applications of Agent Skills across domains such as coding, robotics, web navigation, and recommendation systems.

Evaluation

While the survey offers a useful conceptual framework for understanding the emerging research landscape of Agent Skills, its contribution is largely taxonomical rather than algorithmic. The work does not introduce new models, benchmarks, or empirical evaluations to validate the proposed framework. In addition, the procedural-memory perspective is primarily conceptual and lacks a formal computational formulation. Many practical challenges—such as skill retrieval accuracy, routing mechanisms, and the scalability of large skill libraries—remain largely unexplored.

Relevance

This work is relevant to research on skill-based LLM agents, as it clarifies how reusable procedural knowledge can improve reliability and efficiency in agent workflows. However, the paper does not address the scalability issues of large skill libraries, such as context explosion or skill selection degradation, which remain important open problems for large-scale agent systems.

### AI Agents vs. Agentic AI: A Conceptual taxonomy, applications and challenges

Summary

This survey distinguishes between AI Agents and Agentic AI, proposing a conceptual taxonomy that clarifies their architectural and functional differences. The authors characterize AI Agents as single-agent systems powered by large language models that perform task-specific automation through tool use, reasoning loops, and API integration. In contrast, Agentic AI is defined as a collaborative ecosystem of multiple specialized agents that coordinate through goal decomposition, shared memory, and inter-agent communication. The paper traces the evolution from generative AI systems to tool-augmented AI agents and finally to multi-agent orchestration frameworks. It further analyzes architectural components such as perception, reasoning, action, memory, and orchestration layers, and reviews applications ranging from customer service automation to robotics coordination.

Evaluation

The paper provides a clear conceptual framework for understanding the evolution of agent-based AI systems and helps formalize the distinction between single-agent and multi-agent architectures. However, the contribution is primarily taxonomical and descriptive, rather than algorithmic. The paper does not introduce new models, benchmarks, or empirical evaluations to validate the proposed taxonomy. Additionally, the boundaries between AI Agents and Agentic AI may remain ambiguous in practice, since many modern agent frameworks combine both paradigms.

Relevance

This work is relevant to research on LLM-based agents because it clarifies the architectural design space of agent systems and highlights the transition from single-agent task automation to multi-agent orchestration. However, it does not address scalability challenges such as tool or skill retrieval, routing accuracy, or context explosion, which remain key open problems in large-scale agent systems.

### Atlas: Few-shot Learning with Retrieval Augmented Language Models

Summary

Atlas introduces a retrieval-augmented language model designed to improve few-shot learning for knowledge-intensive tasks. The model integrates a dense neural retriever with a sequence-to-sequence generator, enabling it to access external knowledge from a large document index during inference. Instead of storing factual knowledge in model parameters, Atlas retrieves relevant documents and conditions generation on these retrieved contexts using the Fusion-in-Decoder architecture. The system is jointly trained to optimize both retrieval and generation, allowing it to adapt to tasks with very limited training examples. Experiments on benchmarks such as Natural Questions, FEVER, and MMLU show that Atlas achieves competitive few-shot performance, outperforming a 540B parameter language model on Natural Questions while using roughly 50× fewer parameters.

Evaluation

The work demonstrates that retrieval-augmented architectures can effectively decouple knowledge storage from model parameters, improving efficiency and adaptability. However, Atlas focuses primarily on knowledge-intensive tasks such as question answering and fact verification. The approach does not address broader agentic capabilities such as tool selection, skill invocation, or multi-step reasoning. In addition, the paper does not investigate scaling challenges related to large retrieval indices, latency, or integration within complex agent architectures.

Relevance

This work is relevant as a foundational example of retrieval-augmented reasoning, showing how external memory can improve language model performance without increasing parameter size. However, while Atlas addresses knowledge retrieval, it does not tackle the problem of scalable skill or tool retrieval in agent systems, which remains an open challenge in large-scale LLM-based agents.

### Cognitive Architectures for Language Agents 

Summary

This paper proposes CoALA (Cognitive Architectures for Language Agents), a conceptual framework for designing and analyzing LLM-based agents. Drawing inspiration from classical cognitive architectures such as production systems and ACT-R, the authors organize language agents around three key components: memory, action space, and decision-making loops. Memory is divided into working memory and long-term memory to capture both short-term reasoning context and persistent knowledge. The action space includes both internal cognitive actions (e.g., reasoning and planning) and external actions such as tool use or environment interaction. The decision process is modeled as an iterative observe-reason-act loop. The framework is used to reinterpret existing agent systems such as ReAct and Reflexion within a unified architectural perspective.

Evaluation

The paper provides a useful conceptual framework that connects modern LLM agents with established cognitive architecture principles. However, its contribution is primarily theoretical and descriptive. The framework does not introduce new algorithms, experimental evaluations, or concrete implementation methods. Furthermore, the architecture is highly abstract, making it difficult to assess its practical advantages over existing agent frameworks.

Relevance

This work is relevant as it clarifies the architectural design space of LLM-based agents and highlights the roles of memory, reasoning, and action in agent systems. However, it does not address challenges related to scalability of tools or skills, such as retrieval efficiency, context explosion, or routing accuracy, which remain open problems for large-scale agent systems.

### Gorilla: Large Language Model Connected with Massive APIs

Summary

Gorilla introduces a language model designed to improve the reliability of API and tool usage by large language models. The authors construct APIBench, a benchmark dataset containing API documentation and corresponding instructions across several machine learning libraries. By fine-tuning a LLaMA-based model on this dataset, Gorilla learns to map natural language instructions to correct API calls. During inference, the system retrieves relevant API documentation and conditions generation on these specifications, enabling more accurate function calls. Experiments demonstrate that Gorilla significantly improves API selection and argument generation accuracy, outperforming strong baselines such as GPT-4 on the APIBench benchmark.

Evaluation

The work demonstrates that instruction tuning with API documentation can substantially improve LLM capability in generating correct tool calls. However, the approach primarily focuses on improving API usage accuracy, rather than addressing the broader challenges of tool selection or tool retrieval when many APIs are available. Additionally, the system relies heavily on high-quality documentation and assumes that relevant API descriptions can be retrieved reliably.

Relevance

This paper is relevant to research on tool-augmented language models because it demonstrates how LLMs can be trained to interact reliably with external APIs. However, it does not address the scalability challenges of large tool libraries, such as efficient tool retrieval, routing accuracy, or context explosion, which remain key open problems in agent systems.

###  LLM-guided Hierarchical Retrieval (LATTICE)

Summary

This paper proposes LATTICE, a hierarchical retrieval framework that enables large language models to retrieve relevant documents from large corpora by navigating a semantic tree structure rather than relying on flat retrieve-then-rerank pipelines. The method consists of two stages. In the offline stage, the document corpus is organized into a hierarchy using either a bottom-up clustering strategy or a top-down LLM-driven divisive strategy based on multi-level summaries. In the online stage, a search LLM traverses this semantic tree to locate relevant documents. A central challenge is that LLM relevance judgments are often noisy, context-dependent, and not directly comparable across branches or hierarchy levels. To address this, the paper introduces a calibration mechanism that converts local LLM judgments into latent relevance estimates and aggregates them into path relevance scores for global search. The method is training-free and is designed for reasoning-intensive retrieval settings where standard dense retrieval may fail to surface the right candidates.

Evaluation

The paper is strong in motivation and system design, and it presents a meaningful attempt to move beyond flat retrieval for reasoning-heavy search. Its most technically interesting contribution is not the hierarchy alone, but the calibrated path-based traversal mechanism, which addresses the instability of local LLM relevance judgments. This is more novel than simply organizing the corpus into a tree. However, the work also has notable limitations. First, the hierarchical indexing approach appears sensitive to corpus structure, and the choice between bottom-up and top-down construction is data-dependent. Second, the method incurs substantial offline construction cost and online latency, making it less attractive in low-budget or low-latency settings. Third, while the rebuttal reportedly expanded evaluation beyond BRIGHT, concerns about novelty remained because hierarchical retrieval and structure-aware refinement have already been explored in related work. Thus, the contribution is best understood as a strong systems integration and traversal design paper rather than a fundamentally new retrieval paradigm.

Relevance

This paper is highly relevant to research on scalable skill or tool retrieval because it demonstrates that hierarchical search can reduce the effective search space and improve retrieval quality when flat retrieval reaches a recall ceiling. It is particularly valuable as evidence that LLMs can be used not only for reranking retrieved candidates but also for actively navigating an index. However, its direct transfer to skill retrieval is limited. LATTICE assumes that the indexed objects are documents organized by semantic similarity, whereas skills are better viewed as procedural capability units with execution semantics, preconditions, dependencies, and possible overlap across multiple categories. Therefore, while the paper offers useful ideas for hierarchical routing and score calibration, it does not resolve the central challenge of distinguishing semantically similar but operationally different skills.

### Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale  Summary

This paper proposes AgentSkillOS, a framework for managing and orchestrating large-scale skill ecosystems for LLM-based agents. The system organizes skills into a hierarchical capability tree to enable efficient retrieval and selection when the number of available skills becomes large. During task execution, the agent retrieves relevant skills through task-driven traversal of the capability tree and constructs a directed acyclic graph (DAG) to orchestrate multiple skills for solving complex tasks. The authors also introduce a benchmark consisting of artifact-producing tasks across five domains, including data computation, document creation, visual design, motion video, and web interaction. Experiments demonstrate that hierarchical skill retrieval approximates oracle skill selection and that structured multi-skill orchestration significantly improves task performance compared to flat skill invocation.

**Evaluation**

The paper provides a comprehensive framework for managing large skill ecosystems and highlights the importance of structured skill composition. However, the capability tree assumption may oversimplify real-world skill relationships, where skills often belong to multiple categories. In addition, the system relies on predefined skill descriptions and LLM planning for orchestration, which may lead to ambiguity when skills have semantically similar descriptions.

**Relevance**

This work is highly relevant to research on scalable skill retrieval for LLM agents. It shows that hierarchical organization can reduce search complexity and improve skill routing accuracy. However, the framework assumes that skills can be cleanly organized into a tree and does not fully address the problem of distinguishing semantically similar skills with different operational workflows.

### REAC T: SYNERGIZING REASONING AND ACTING IN LANGUAGE MODELS 

Summary

This paper proposes ReAct, a prompting framework that interleaves reasoning traces and environment actions within a single LLM trajectory. Instead of using chain-of-thought reasoning or action generation in isolation, ReAct allows the model to alternate between “Thought”, “Action”, and “Observation” steps, so that reasoning can guide action selection while external observations can inform subsequent reasoning. The approach is evaluated on knowledge-intensive tasks such as HotpotQA and FEVER, as well as interactive decision-making benchmarks including ALFWorld and WebShop. Results show that ReAct improves interpretability and often improves performance over reasoning-only or action-only baselines, particularly by reducing hallucination through interaction with external information sources.

Evaluation

The main contribution of this work is architectural rather than algorithmically complex: it establishes a general and influential reasoning–action loop for LLM agents. Its strongest contribution is showing that reasoning and acting should not be treated as separate capabilities, but as interleaved components of a single control process. The experimental evaluation is broad and convincing, which explains why the paper received strong reviewer support and was highlighted as a notable top-5% paper at ICLR. However, both the paper and reviewers reveal an important limitation: ReAct assumes that the available action space can be predefined and demonstrated within the prompt. This makes the framework difficult to scale to environments with large, dynamic, or poorly structured tool libraries. In addition, some reported gains depend on combining ReAct with self-consistent chain-of-thought, suggesting that ReAct alone is not always the strongest inference strategy.

Relevance

This paper is highly relevant as a foundational agent architecture for tool-augmented LLM systems. It provides one of the clearest early formulations of the reasoning–acting loop that later agent frameworks build upon. However, it does not address the problem of scalable tool or skill retrieval. ReAct assumes a relatively small and known action space, whereas large skill libraries introduce routing, retrieval, and context-budget challenges that are outside the scope of this work. Therefore, this paper is best positioned as a foundational precursor to later research on scalable tool or skill selection, rather than a direct solution to the skill overload problem targeted in this thesis.

### Reflexion: language agents with verbal reinforcement learning

Summary

This paper proposes Reflexion, a framework for improving LLM-based agents through verbal reinforcement learning. Instead of updating model weights, Reflexion converts feedback from the environment into natural-language reflections, which are stored in an episodic memory buffer and used to guide subsequent attempts. The framework is organized around three roles: an Actor that generates actions or responses, an Evaluator that scores the resulting trajectory, and a Self-Reflection module that summarizes failures into actionable lessons. The method is evaluated across sequential decision-making, reasoning, and programming tasks, where it shows substantial gains over baseline agents and achieves particularly strong results on coding benchmarks.

Evaluation

The main contribution of Reflexion is to shift policy improvement from parameter space into language space: the agent improves not by gradient updates, but by conditioning future decisions on textual reflections of past failures. This is an important conceptual contribution and helps explain why the paper was positively received by reviewers. The framework is also modular and empirically broad, spanning multiple task domains. However, reviewer discussions reveal several limitations. First, Reflexion relies on task-specific evaluator designs and feedback heuristics, which weakens claims of universal generality. Second, its effectiveness appears to depend strongly on the capability of the underlying LLM: weaker models may fail to generate useful reflections, as shown in the authors’ additional StarChat experiments. Third, some comparisons—particularly on HotPotQA—are better interpreted as proof-of-concept iterative improvement settings than strictly fair baseline comparisons, because Reflexion receives explicit correctness feedback unavailable to standard ReAct baselines. Finally, the framework increases inference cost through repeated trials and does not provide a scalable memory retrieval mechanism beyond storing the last few reflections.

Relevance

This work is highly relevant to LLM agent research as a foundational paper on self-improvement through memory and feedback. It demonstrates that language-based reflections can function as an effective improvement signal across multiple episodes, offering an alternative to expensive reinforcement learning or fine-tuning. However, Reflexion does not directly address the problem of scalable tool or skill selection. Its memory is a small buffer of recent reflective notes rather than a large capability library, and it does not propose retrieval, indexing, or routing mechanisms for large skill sets. Therefore, Reflexion is best positioned as a paper on agent learning and adaptation, not on large-scale skill retrieval

### Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

Summary

This paper introduces Retrieval-Augmented Generation (RAG), a framework that combines a parametric sequence-to-sequence model with a non-parametric external memory for knowledge-intensive NLP tasks. The model first retrieves relevant documents from a dense Wikipedia index using a neural retriever, then conditions a generator on both the input and the retrieved passages to produce the final output. The retrieved documents are treated as latent variables and marginalized during generation. The authors propose two variants: RAG-Sequence, which conditions the entire output on the same retrieved document, and RAG-Token, which allows different output tokens to depend on different retrieved documents. Experiments on open-domain question answering, abstractive question answering, question generation, and fact verification show that RAG improves factuality, specificity, and performance relative to parametric-only baselines.

Evaluation

The key contribution of this work is to formalize a hybrid architecture that combines parametric memory (stored in model weights) with non-parametric memory (stored in an external retrievable index). This design directly addresses important limitations of purely parametric language models, including weak provenance, poor updatability, and factual hallucination. A particularly important strength is that the external memory is human-readable and can be updated by replacing or editing the document index, without retraining the underlying model. However, RAG is primarily a framework for retrieving knowledge documents to support generation, not for retrieving executable tools or skills. As a result, while it provides a strong architectural foundation for external memory access, it does not directly address problems of capability routing, tool selection, or multi-step skill execution.

Relevance

This paper is highly relevant to research on scalable skill retrieval because it establishes the fundamental principle that external retrievable memory can complement or outperform purely parametric knowledge storage. In particular, it motivates the idea that large capability libraries should not be embedded directly into model weights or prompts, but instead organized as an external memory that can be selectively retrieved at inference time. However, the retrieval target in RAG is textual evidence rather than executable skills, so the paper does not solve the full skill selection problem. Its main value for this thesis lies in providing the architectural and conceptual basis for treating skills as retrievable non-parametric memory..

### SCALEMCP: DYNAMIC AND AUTO-SYNCHRONIZING MODEL CONTEXT PROTOCOL TOOLS FOR LLM AGENTS

Summary

This paper introduces ScaleMCP, a scalable tool selection architecture for LLM agents operating within the Model Context Protocol (MCP) ecosystem. The authors argue that existing agent frameworks rely on manually maintained local tool repositories, which leads to duplication, synchronization issues, and limited scalability when the number of available tools grows.

To address this problem, the paper proposes a dynamic tool discovery framework where LLM agents retrieve tools from MCP servers during interaction. The system maintains an auto-synchronizing tool storage pipeline that continuously updates tool representations through CRUD operations with MCP servers acting as the single source of truth.

In addition, the authors introduce Tool Document Weighted Average (TDWA), an embedding strategy that assigns different weights to tool document components such as tool names, descriptions, parameter schemas, and synthetic user queries. The approach aims to improve semantic representation for tool retrieval. Experiments conducted on a dataset of 5,000 MCP servers and approximately 140,000 queries show that reranking strategies and structured embeddings improve retrieval performance and agent task completion rates.

Evaluation

The primary contribution of the paper lies in proposing a system architecture that integrates MCP-based tool discovery with retrieval-based selection. The dynamic retrieval mechanism allows agents to discover tools during multi-turn interactions rather than relying on a static tool list.

However, the technical novelty of the approach is limited. Most of the system relies on established retrieval pipelines such as dense embeddings, vector search, and cross-encoder reranking. The proposed TDWA embedding strategy offers additional weighting control over tool document fields, but experimental results suggest that simple concatenation of tool fields often performs similarly or better under certain retrieval configurations.

Relevance

This work is relevant to research on scalable tool or skill libraries in LLM agents because it highlights practical challenges associated with managing large tool repositories. In particular, the study illustrates how retrieval mechanisms can replace static tool lists and enable agents to dynamically discover tools during interaction.

However, the paper primarily addresses engineering and infrastructure aspects of tool storage and retrieval rather than the underlying reasoning or routing challenges involved in selecting the correct tool among many candidates. Therefore, while the work contributes insights into system design for tool retrieval, it does not directly address the broader problem of scalable tool or skill selection in agent architectures.

###  SciToolAgent: A Knowledge Graph-Driven Scientific Agent for Multi-Tool Integration 

384th percentile  
Citations  
Set citation alert  
1.81  
FWCI

### 

Summary

This paper proposes SciToolAgent, an LLM-based agent designed to orchestrate large collections of domain-specific scientific tools across biology, chemistry, and materials science. The system introduces a Scientific Tool Knowledge Graph (SciToolKG), which encodes tool metadata such as functionality, input/output formats, dependencies, and safety attributes. Based on this graph, the agent performs graph-based retrieval to identify relevant tools and generate a chain-of-tools workflow, which is then executed sequentially by an LLM-based Executor.

The architecture consists of three main components: a Planner (which retrieves tools and constructs workflows), an Executor (which performs tool calls and handles errors), and a Summarizer (which synthesizes results and supports iterative refinement). In addition, a safety module is integrated to detect potentially harmful outputs (e.g., toxic molecules or proteins) using similarity-based matching against curated databases.

Experiments on a newly constructed benchmark (SciToolEval, 531 tasks) show that SciToolAgent outperforms prior agent frameworks such as ReAct and Reflexion, achieving approximately 94% accuracy and improving multi-tool task performance by 10–20%. The results suggest that explicitly modeling tool dependencies and generating structured workflows can significantly improve planning and execution in complex tasks.

Evaluation

The primary contribution of this work lies in introducing a structure-aware paradigm for tool orchestration, where tools are no longer treated as independent retrieval units but as components within a dependency-aware workflow graph. By combining graph-based retrieval with LLM planning, the framework improves global reasoning compared to reactive approaches such as ReAct, which rely on step-by-step local decisions. This design is particularly effective for multi-step scientific workflows, where tool ordering and compatibility are critical.

However, several limitations reduce the broader impact of the work. First, the SciToolKG is manually constructed, requiring extensive curation of tool metadata and relationships, which limits scalability to larger or dynamic tool ecosystems. Second, the retrieval mechanism primarily relies on embedding-based similarity, without leveraging more advanced graph reasoning techniques (e.g., learned graph traversal or path optimization), suggesting limited algorithmic novelty. Third, the evaluation benchmark (SciToolEval) is synthetically constructed by the authors, raising concerns about potential bias and overfitting to the system design. Finally, the framework depends heavily on high-capacity proprietary LLMs, and performance degrades noticeably when using smaller open-source models, indicating limited accessibility in resource-constrained settings.

Relevance

This work is relevant to research on tool and skill orchestration in LLM-based agents, as it highlights the importance of modeling inter-tool dependencies and workflow structure rather than treating tools as independent entities. In particular, it provides an important conceptual shift: tool selection should be framed as a structured retrieval and planning problem over workflows, rather than a flat semantic matching problem.

However, the paper does not directly address the scalability challenges of large tool or skill libraries, such as routing accuracy degradation, context explosion, or efficient retrieval under thousands of candidates. Moreover, the proposed solution operates at the tool level with manually defined structure, whereas many modern agent systems (e.g., skill-based frameworks) encapsulate workflows within higher-level abstractions. This suggests a gap between explicit workflow modeling (as in SciToolAgent) and implicit workflow encapsulation (as in skill-based systems).

For research on skill retrieval, this work motivates the need to externalize and leverage workflow structure within skills, enabling structure-aware retrieval, decomposition, and composition across large-scale skill libraries.

### SkillAct: Using Skill Abstractions Improves LLM Agents 

Summary

This paper proposes SkillAct, a prompting-based framework that improves LLM agents by introducing skill abstractions, defined as reusable high-level behaviors extracted from trajectories. Skills are represented as natural language descriptions consisting of a name, instructions, and example executions, and are appended to the agent prompt to guide decision-making.

The authors further demonstrate that such skills can be automatically extracted from few-shot demonstrations using LLMs, eliminating the need for manual engineering. Experiments on ALFWorld show that SkillAct improves success rates over ReAct, primarily by reducing execution errors rather than improving planning.

Evaluation

The paper introduces a simple yet effective abstraction layer that enhances LLM agent performance without requiring model fine-tuning. The idea of representing skills as reusable textual primitives is elegant and aligns with human hierarchical reasoning. Additionally, the ability to automatically extract skills from trajectories is a strong contribution toward scalable agent design.

However, the framework suffers from several limitations. First, skills are incorporated as a flat list in the prompt, leading to scalability issues as the number of skills grows. Second, the approach lacks any retrieval or routing mechanism, relying entirely on the LLM to implicitly select relevant skills. Third, skills are represented purely in natural language without explicit structural relationships, limiting compositional reasoning and reuse. Finally, the evaluation is restricted to a single simulated environment, raising concerns about generalizability.

Relevance

This work is highly relevant to research on skill-based LLM agents, as it formalizes skills as reusable abstractions and demonstrates their effectiveness in improving agent performance. However, it also exposes a critical gap: skill libraries are not scalable without structured retrieval mechanisms.

For research on skill retrieval, this paper highlights that while skills can encapsulate workflows internally, their lack of explicit structure and retrieval leads to inefficiencies and performance degradation at scale. This suggests a key research direction:

augmenting skill-based systems with structure-aware retrieval and composition mechanisms, bridging the gap between implicit skill abstraction and explicit workflow modeling.

### SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks

Summary

This paper introduces SkillsBench, the first large-scale benchmark for evaluating the effectiveness of skills in LLM-based agents. The authors evaluate agent performance across three conditions—no skills, curated skills, and self-generated skills—on 84 diverse tasks and over 7,000 trajectories. Results show that curated skills improve performance by an average of 16.2 percentage points, while self-generated skills provide no benefit on average. The study also reveals that smaller, focused skill sets outperform large, comprehensive skill libraries, and that skills can partially substitute for model scale.

Evaluation

The paper provides a valuable empirical foundation for understanding the role of skills in LLM agents and highlights the importance of skill design and selection. Its large-scale evaluation across multiple domains and models offers strong evidence that skills can significantly improve performance, particularly in procedural and domain-specific tasks.

However, the work is primarily observational and does not propose new methods for improving skill-based systems. In particular, it assumes a flat skill library without retrieval mechanisms, which limits its applicability to real-world scenarios where skill libraries are large and dynamic. Additionally, the study does not model structural relationships between skills or investigate compositional reasoning, leaving key challenges in scalable skill systems unresolved.

Relevance

This work is highly relevant to research on skill scaling in LLM agents, as it provides direct empirical evidence that increasing the number of skills can degrade performance and that effective skill usage depends on careful selection and design.

For research on skill retrieval, this paper highlights a critical gap:

current skill-based systems lack mechanisms for efficient selection, structuring, and composition of skills at scale

This motivates the need for structured skill retrieval frameworks, which can address the limitations of flat skill libraries and enable scalable agent performance in environments with thousands of available skills.

###   SoK: Agentic Skills — Beyond Tool Use in LLM Agents  

Summary

This paper presents a Systematization of Knowledge (SoK) on agentic skills, positioning them as reusable, executable procedural modules that extend beyond traditional tools, plans, and memory in LLM agents. The authors formalize skills as a structured abstraction   
𝑆  
\=  
(  
𝐶  
,  
𝜋  
,  
𝑇  
,  
𝑅  
)  
S=(C,π,T,R), capturing applicability conditions, execution policies, termination criteria, and callable interfaces.

The paper introduces a comprehensive lifecycle model covering skill discovery, refinement, storage, retrieval, execution, and evaluation, and proposes seven system-level design patterns such as metadata-driven progressive disclosure, code-as-skill, and self-evolving skill libraries. Additionally, it provides a representation × scope taxonomy and highlights security risks associated with skill-based systems, including supply-chain attacks in skill marketplaces.

Evaluation

The paper offers a well-structured conceptual framework that unifies fragmented research on LLM agents under a skill-centric perspective. The lifecycle model and design pattern taxonomy are particularly useful for understanding how real-world agent systems manage reusable procedural knowledge.

However, the contribution remains primarily conceptual. The work does not introduce new retrieval, routing, or orchestration algorithms, nor does it provide empirical evaluation of the proposed abstractions. The skill abstraction, while useful, overlaps significantly with existing notions such as tool composition and hierarchical planning, raising questions about its novelty. Additionally, critical challenges such as skill retrieval accuracy, composition conflicts, and scalability are acknowledged but not addressed with concrete solutions.

Relevance

This work is directly relevant to research on scalable skill retrieval and agent architecture design. It highlights that the core bottleneck in large-scale skill systems lies in retrieval and routing rather than representation alone.

However, the paper does not provide concrete mechanisms to address performance degradation or context explosion in large skill libraries. As such, it serves more as a problem framing and design space exploration rather than a solution to the scalability challenges central to this research.

### StableToolBench: Towards Stable Large-Scale Benchmarking on

### Tool Learning of Large Language Models

1897th percentile  
Citations  
Set citation alert  
5.29  
FWCI

Summary

This paper introduces StableToolBench, a benchmark designed to address the instability and reproducibility issues in existing tool-learning evaluations for LLM agents. The authors identify that real-world APIs are inherently unstable due to changing availability, authorization requirements, and dynamic behaviors, which undermines the reliability of existing benchmarks such as ToolBench.

To address this, the paper proposes a virtual API system that replaces real APIs with LLM-based simulators conditioned on API documentation and cached examples. This is complemented by a caching system to ensure deterministic responses and a stable evaluation protocol using GPT-4 as an automatic evaluator. The framework introduces new metrics, including Solvable Pass Rate (SoPR) and Solvable Win Rate (SoWR), to filter out unsolvable tasks and improve evaluation consistency.

Evaluation

The paper makes a strong engineering contribution by addressing a critical but often overlooked issue in LLM agent research: benchmark instability. The virtual API simulation combined with caching provides a practical solution for reproducible evaluation at scale. Empirical results show that simulated APIs closely match real APIs in both output quality and diversity, and the proposed evaluation metrics improve consistency.

However, the approach has several limitations. The reliance on LLM-based simulation introduces potential fidelity issues, as simulated APIs may produce plausible but incorrect outputs. The deterministic nature of the benchmark also fails to capture real-world uncertainties such as API failures and latency. Additionally, the work does not address core challenges in tool selection, planning, or scalability, limiting its contribution to evaluation infrastructure rather than agent capability improvement.

Relevance

This work is relevant to research on scalable tool and skill systems as it provides a controlled and reproducible evaluation environment for studying agent behavior. In particular, it highlights that tool usage patterns can be partially captured and reused through caching, suggesting potential opportunities for improving retrieval efficiency.

However, the paper does not address the central challenges of skill or tool selection at scale, nor does it propose mechanisms to mitigate context explosion or routing errors. As such, it serves as a complementary infrastructure for evaluating agent systems rather than a direct solution to scalability problems in large tool or skill libraries.

### ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers openreview

Summary

This paper introduces ToolDreamer, a framework that improves tool retrieval for LLM agents by incorporating reasoning into the retrieval process. The authors identify a key limitation in existing approaches: tool retrievers rely on semantic similarity between user queries and tool descriptions, which often fails when relevant tools are not explicitly mentioned in the query.

To address this, ToolDreamer uses an LLM to generate hypothetical tools—descriptions of tools that might be useful for solving the query. These hypothetical tools are then aligned with ground-truth tools via bipartite matching and used to train a retriever using a modified contrastive learning objective. During inference, the retriever uses these generated tools as search queries and aggregates results using reciprocal rank fusion.

Evaluation

The paper presents a novel perspective on tool retrieval by reframing it as a reasoning-aligned matching problem rather than a purely semantic similarity task. The use of hypothetical tools effectively bridges the gap between user intent and tool descriptions, and empirical results show consistent improvements across both sparse and dense retrievers.

However, the approach still relies on flat retrieval mechanisms and does not address scalability challenges in large tool libraries. The quality of retrieval is heavily dependent on the quality of LLM-generated hypothetical tools, introducing instability and additional computational overhead. Furthermore, the method does not consider structured relationships between tools or multi-step composition, limiting its effectiveness in more complex agent settings.

Relevance

This work is highly relevant to research on scalable tool or skill retrieval, as it demonstrates that incorporating reasoning into the retrieval process can significantly improve alignment between queries and tools.

However, it does not address the core challenges of scaling retrieval to large tool or skill libraries, nor does it introduce structured retrieval mechanisms or routing architectures. As such, it provides a strong foundation for improving semantic alignment, but leaves open the problem of efficient and scalable tool or skill selection.

### Toolformer: Language Models Can Teach Themselves to Use Tools

64799th percentile  
Citations  
Set citation alert  
152.56  
FWCI

Summary

Toolformer proposes a self-supervised method for teaching language models to use external tools. Instead of relying on extensive human annotations, the model generates candidate API calls, filters them based on whether they improve future token prediction, and then fine-tunes on these filtered examples. The method enables the model to learn when to call a tool, which tool to call, what arguments to provide, and how to integrate returned results into generation. Reviewers consistently recognized the work as a high-impact and elegant foundation for tool-augmented language modeling.

Evaluation

The main strength of Toolformer lies in reframing tool use as a learnable behavior rather than a hand-engineered pipeline. Its self-supervised filtering strategy is technically elegant and empirically effective. However, the OpenReview discussion also makes clear that the method has notable limitations: it struggles with chained or multiple tool calls, is sample-inefficient for some tools, and lacks a thorough error analysis of failure modes. In addition, the approach does not address scalability issues such as retrieval, routing, or large tool library selection.

Relevance

Toolformer is foundational for research on tool-augmented LLM agents because it establishes that tool use can be learned directly by the model. However, it does not solve the problem of scalable tool or skill selection in large libraries. This makes it highly relevant as background and motivation, but insufficient as a solution for context explosion or large-scale routing problems.

### ToolGen: Unified Tool Retrieval and Calling via Generation

498th percentile  
Citations  
Set citation alert  
8.85  
FWCI

Summary

OpenReview discussion around ToolGen shows that the paper is valued primarily for introducing a new paradigm: transforming tool retrieval into a generative process by representing tools as virtual tokens and directly generating them during inference. Reviewers and the area chair acknowledged the significance of this shift, especially for large tool libraries, and accepted the paper as an ICLR 2025 poster. At the same time, the discussion also clarified that ToolGen is not a universally dominant solution: its strongest case lies in unified agent performance and controllable tool generation, rather than being the best system on every retrieval metric.

Evaluation

The review discussion highlights several important limitations. First, ToolGen relies on parametric storage of tool knowledge, making dynamic tool addition and API updates difficult without retraining. Second, heavy tool-specific fine-tuning substantially degrades general LLM capability unless mixed with general instruction data. Third, the technical novelty was debated, since token-based tool representations were not entirely new; the paper’s stronger contribution is the large-scale end-to-end pipeline rather than tokenization alone. These concerns make ToolGen an important but still incomplete solution for scalable tool use.

Relevance

ToolGen is highly relevant as a competing paradigm for large-scale tool selection, especially because it shows that external retrieval is not the only option. However, its formulation is most natural for static, atomic tool libraries and less well suited for dynamic, structured, or compositional skill libraries. For research on scalable skill retrieval, ToolGen is therefore best viewed as a strong parametric baseline rather than a complete answer.

### ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs

13099th percentile  
Citations  
Set citation alert  
40.01  
FWCI

Summary

This paper introduces ToolLLM, a comprehensive framework for enabling open-source LLMs to use more than 16,000 real-world APIs. Its core contribution is the construction of ToolBench, a large-scale instruction-tuning dataset built from RapidAPI, covering both single-tool and multi-tool scenarios. The framework also includes a dense API retriever, a search-based reasoning strategy called DFSDT, and an automatic evaluator called ToolEval. Using this pipeline, the authors fine-tune LLaMA into ToolLLaMA, which shows strong tool-use ability and promising generalization to unseen APIs.

Evaluation

The main strength of this work lies in its scale and systems contribution. It moves tool-use research from toy settings to a much more realistic large-scale API environment and provides a widely adopted benchmark for subsequent work. ToolBench is especially valuable because it includes real APIs, multi-tool tasks, and practical retrieval settings. However, the work has important limitations. Its evaluation pipeline depends heavily on ChatGPT-based judgments and dynamic real-world APIs, which creates reproducibility and reliability concerns. In addition, the technical novelty of the modeling approach is more limited than the benchmark contribution, and the retriever-generator split introduces potential misalignment between API retrieval and downstream tool execution.

Relevance

This work is highly relevant as foundational background for large-scale tool retrieval and tool-use pipelines. It establishes the practical importance of API retrieval when the tool space is too large to fit directly into the prompt, and it provides an influential benchmark lineage for later work such as StableToolBench and ToolGen. However, it remains fundamentally tool-centric and does not address structured skill retrieval, hierarchical skill composition, or dynamic skill routing. As such, it is best understood as a major benchmark and systems baseline rather than a direct solution to scalable skill retrieval.

### ToolReAGt: Tool Retrieval for LLM-based Complex Task Solution via Retrieval Augmented Generation (Not really useful)

Summary

This paper proposes ToolReAGt, a training-free tool retrieval framework that combines Retrieval-Augmented Generation (RAG) with ReAct-style iterative reasoning. Instead of performing one-shot retrieval based on the full task description, the system decomposes complex tasks into sub-tasks and iteratively refines retrieval queries through a Thought–Action–Observation loop. The approach improves tool retrieval accuracy on the UltraTool benchmark, achieving an 8.9% improvement in recall@5 over conventional RAG baselines. The paper also highlights the importance of task decomposition and contextual information in improving retrieval performance.

Evaluation

The main contribution lies in integrating reasoning-based iterative refinement into the retrieval process, effectively reframing tool retrieval as a sequential decision-making problem. However, the approach primarily improves query formulation rather than introducing a fundamentally new retrieval mechanism. Additionally, the system incurs significant computational overhead due to multiple LLM calls per task, limiting its scalability in real-world settings. The reliance on LLM reasoning also introduces non-determinism, which may reduce reliability in production environments.

Relevance

This work is directly relevant to research on scalable tool and skill retrieval in LLM agents, as it demonstrates that naive one-shot retrieval is insufficient for complex tasks. However, it does not address the core scalability challenges associated with large tool or skill libraries, such as retrieval efficiency, semantic ambiguity, and structured representation. Furthermore, its design is better suited to atomic tools rather than higher-level skills, which involve procedural and hierarchical semantics. This highlights a gap between existing tool retrieval methods and the requirements of skill-based agent systems.

### Toolshed: Scale Tool-Equipped Agents with Advanced RAG-Tool Fusion and Tool Knowledge Bases

Summary

This paper proposes Toolshed Knowledge Bases and Advanced RAG-Tool Fusion, a multi-stage retrieval pipeline designed to improve tool selection in large-scale tool-equipped LLM agents. The approach enhances tool representations through structured metadata (e.g., argument schemas and synthetic queries), applies query decomposition and multi-query expansion during retrieval, and refines results via reranking and self-reflection. The study also investigates the relationship between the total number of tools (tool-M) and the retrieval threshold (top-k), highlighting their strong coupling in large-scale settings.

Evaluation

The paper provides a comprehensive engineering solution that integrates multiple advanced RAG techniques into a unified pipeline. While effective in improving retrieval accuracy, the contribution is primarily architectural and heuristic rather than algorithmically novel. The approach introduces significant computational overhead due to query decomposition, multi-query expansion, and LLM-based reranking, raising concerns about scalability and latency in real-world deployments. Additionally, the reliance on embedding-based retrieval limits its ability to resolve semantic ambiguity between similar tools.

Relevance

This work is relevant to the study of scalable tool retrieval in LLM agents, particularly in demonstrating how retrieval quality can be improved through pipeline design. However, it does not address the fundamental challenges of scaling to large tool or skill libraries, such as efficient routing, structured representation, or retrieval complexity. The framework assumes tools can be represented as static documents, making it less suitable for skill-based systems where procedural and hierarchical structures are required.

### EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction

599th percentile  
Citations  
Set citation alert  
12.89  
FWCI

Summary

This paper proposes EASYTOOL, a method for transforming raw tool documentation into concise, structured tool instructions that improve LLM-based tool utilization. The approach standardizes tool descriptions by focusing on core functionality and usage guidelines, enabling models to better understand when and how to use tools. EASYTOOL significantly reduces token cost while improving tool selection, execution accuracy, and retrieval performance across multiple benchmarks.

Evaluation

The paper demonstrates that improving tool representations alone can substantially enhance agent performance, even outperforming fine-tuned models in some cases. However, the contribution is limited to representation-level improvements and does not introduce new retrieval algorithms or architectural innovations. The approach can be viewed as structured prompt engineering, and its effectiveness depends on the quality of generated instructions. Additionally, it does not address scalability challenges in large tool libraries.

Relevance

This work is highly relevant to tool and skill retrieval research, as it highlights the importance of representation quality in tool selection. It suggests that retrieval failures may stem from poor tool descriptions rather than retrieval models. However, it does not address large-scale retrieval complexity or structured skill representations, which remain open challenges in scalable agent systems.

### Online-Optimized RAG for Tool Use and Function Calling (Still don’t know if this is highly relevant or not as it introduced online learning)

Summary

This paper proposes Online-Optimized RAG (ORAG), a deployment-time adaptation framework that improves retrieval for tool use and function calling by updating item embeddings online. The method formulates retrieval as a softmax-based multiclass prediction problem under bandit feedback, where only binary success/failure signals are observed. After each interaction, ORAG performs a lightweight gradient update: successful tools are moved closer to the query embedding, while unsuccessful ones are pushed away. The approach is designed to be plug-and-play, requiring no modification to the underlying LLM and introducing minimal latency overhead. The authors demonstrate applicability across single-hop and multi-hop retrieval, dynamic tool inventories, and reranker-based pipelines, and provide regret-based theoretical guarantees linking performance to embedding initialization quality.

Evaluation

The paper addresses a practically relevant issue—embedding misalignment in deployed RAG systems—and proposes a simple and computationally efficient solution. The formulation of retrieval as an online learning problem with bandit feedback is conceptually clean, and the method’s compatibility with black-box LLM systems is a strong practical advantage.

However, the contribution is largely incremental, as it builds on well-established ideas from online learning and softmax-based retrieval. The main weaknesses lie in the empirical evaluation:

Evaluation fairness is initially unclear, as the method adapts on the same query stream used for evaluation, raising concerns about implicit training on test data. Although temporal hold-out experiments are later introduced, questions about realism remain.

Baselines are insufficiently strong, lacking comparisons to online adaptive methods, hybrid retrieval systems, and fully trained retrievers, making it difficult to contextualize gains.

When combined with rerankers, performance attribution becomes ambiguous, as improvements cannot be cleanly separated between the retriever and downstream components.

Gains are primarily observed in Recall@k rather than ranking-sensitive metrics (e.g., NDCG), suggesting that the method improves candidate inclusion but not ranking quality.

Robustness to noisy, delayed, or adversarial feedback, as well as long-term embedding drift, is not thoroughly analyzed.

Overall, while the method is practical and well-motivated, the empirical evidence does not conclusively demonstrate superiority over stronger or more realistic alternatives.

Relevance

This work is highly relevant to research on tool retrieval and LLM agents, particularly in scenarios where retrieval systems must operate under deployment constraints and distribution shift. It highlights an important but underexplored dimension of RAG systems: post-deployment adaptation of retrieval geometry.

However, the approach is limited to item-level embedding updates, which assume a static representation of tools as independent items. It does not address challenges associated with:

Large-scale tool libraries (e.g., compositional or hierarchical skills)

Semantic generalization to unseen tools

Structured workflows or multi-step skill execution

As such, while ORAG provides a useful mechanism for incremental improvement of existing retrieval systems, it does not fundamentally advance the representation or scalability of tool use in LLM agents. This leaves open research directions in structured skill representations, semantic retrieval, and hybrid parametric–nonparametric approaches, which are critical for next-generation agent systems.

### Towards Efficient Agents: A Co-Design of Inference Architecture and System

Summary

This paper proposes AgentInfer, a unified framework for improving the end-to-end efficiency of LLM-based agents by jointly optimizing reasoning architecture and serving systems. Rather than treating agent latency as a per-token inference problem, the authors argue that autonomous agents must be optimized at the trajectory level, since their total cost emerges from iterative reasoning, context growth, retries, and heterogeneous tool interactions. To address this, the framework combines four modules: AgentCollab for dynamic collaboration between large and small models, AgentCompress for asynchronous context and search-result compression, AgentSched for KV-cache-aware scheduling under mixed long- and short-context workloads, and AgentSAM for speculative decoding using session and cross-session memory. Across BrowseComp-zh and DeepDiver-style tasks, the framework reportedly reduces ineffective token usage by over 50% and achieves 1.8×–2.5× end-to-end speedup while largely preserving accuracy.

Evaluation

The paper’s main strength is its system-level reframing of agent efficiency: it correctly identifies that autonomous agents are path-dependent multi-turn systems, so local inference acceleration can be misleading if it increases retries or reasoning instability. The empirical analysis on quantization, summarization, cache eviction, and multi-model collaboration is practically valuable. However, the work is broad rather than deep, combining several moderately novel components into a unified engineering framework rather than advancing a single sharply defined algorithmic contribution. Its evaluation is also tightly coupled to deep research agents and long-context web-based workloads, which may limit generalization to other agent settings. In addition, some components, such as progress-based escalation, depend on the reliability of self-evaluation signals that are not deeply theorized or stress-tested.

Relevance

This paper is relevant to thesis work on scalable agent systems because it highlights the systems consequences of context growth, repeated tool use, and inefficient reasoning loops. It is particularly useful as supporting evidence that agent degradation is not purely a model problem, but also a scheduling, memory, and orchestration problem. However, it is only indirectly related to skill retrieval. The paper does not address how to retrieve from large or dynamic skill libraries, how to disambiguate semantically similar but procedurally different skills, or how to organize skills hierarchically. Therefore, it is better positioned as an efficiency and systems co-design paper for agent execution rather than as a direct solution to skill overload or scalable skill selection.

### Voyager: An Open-Ended Embodied Agent with Large Language Models

Summary

This paper proposes Voyager, an LLM-powered embodied lifelong learning agent for open-ended exploration in Minecraft. The system is built around three components: an automatic curriculum that proposes progressively suitable tasks, an ever-growing skill library that stores successful behaviors as executable code, and an iterative prompting mechanism that refines generated programs using environment feedback, execution errors, and self-verification. Rather than updating model parameters, Voyager accumulates capabilities externally by storing and reusing code-based skills indexed by language embeddings. The resulting skills are temporally extended, interpretable, and compositional. Empirical results show that Voyager substantially outperforms prior LLM-based baselines in exploration, tech-tree progression, and zero-shot transfer to unseen tasks in a new world.

Evaluation

The paper is one of the strongest early demonstrations that LLM agents can benefit from an explicit skill library rather than relying purely on transient prompting. Its main strength lies in presenting a complete end-to-end lifelong learning loop in which skills are acquired, verified, stored, retrieved, and reused. However, the retrieval mechanism itself is relatively simple, relying on embedding-based similarity search over skill descriptions without explicit modelling of preconditions, compositional dependencies, or hierarchical skill relations. In addition, the system depends heavily on GPT-4’s prior knowledge of Minecraft and does not fully establish whether the approach would generalize to domains with weaker language priors or less well-documented task structure.

Relevance

This paper is highly relevant to thesis work on scalable skill retrieval because it provides a concrete example of an LLM agent built around an ever-growing skill library. It supports the view that skills are higher-level, reusable behavioral units rather than merely atomic tools, and it shows that explicit skill storage and retrieval can materially improve long-horizon agent performance. At the same time, it leaves major open questions that are central to a skill retrieval thesis, including how retrieval should scale as the library grows, how semantically similar but procedurally different skills should be disambiguated, and whether skill libraries should be organized using richer structures such as hierarchies or graphs.

### When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail

Summary

This paper investigates whether a single-agent system equipped with a library of skills can replace a multi-agent system while reducing communication overhead. The authors propose a compilation view in which specialized agent roles in a multi-agent pipeline are transformed into selectable skills within a single-agent architecture. Experiments on GSM8K, HumanEval, and HotpotQA show that compiled single-agent-with-skills systems achieve comparable accuracy to their multi-agent counterparts while reducing token consumption by 53.7% and latency by 49.5% on average. The paper then studies how skill selection scales as libraries grow, finding that selection accuracy remains stable up to a critical threshold and then drops sharply. It further shows that semantic confusability among similar skills, rather than library size alone, is a major driver of this degradation, and that hierarchical routing can partially recover performance.

Evaluation

The paper makes a strong conceptual contribution by reframing multi-agent modularity as internalized skill selection and by isolating skill selection as a distinct scaling problem. Its most valuable result is the empirical finding that semantic confusability plays a more important role than raw library size in selection failure, which directly informs the design of scalable skill libraries. However, the evidence remains preliminary. Most scaling experiments rely on synthetic skill libraries, and evaluation focuses on selection accuracy rather than full downstream task performance. In addition, the hierarchical routing methods are relatively simple, so the paper identifies the problem more clearly than it fully solves it.

Relevance

This paper is highly relevant to thesis work on scalable skill retrieval and skill-library design. It directly studies the failure mode that emerges when a flat skill library grows too large and semantically overlapping skills compete for selection. It also provides a useful theoretical framing for distinguishing multi-agent communication overhead from single-agent selection overhead, which is highly relevant to research on skill-based alternatives to multi-agent systems. At the same time, it leaves open several directions central to a thesis, including evaluation on real-world skill libraries, more advanced routing mechanisms, and dynamic skill library maintenance under continual growth.

### Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward

This paper is a survey and systematization work that consolidates the emerging Agent Skills paradigm for LLM agents. It defines skills as modular, filesystem-based packages of procedural knowledge (instructions, workflows, scripts, and resources) that can be dynamically loaded to extend agent capabilities.

Importantly, the paper does not introduce the core mechanisms itself. Instead, it synthesizes and formalizes concepts already introduced by industry (primarily Anthropic), including:

the SKILL.md specification

progressive disclosure (multi-level context loading)

the integration with the Model Context Protocol (MCP)

The paper organizes the field along four axes:

Architectural foundations

Skill acquisition methods

Deployment (especially computer-use agents)

Security and governance

A central observation is that as skill libraries scale, skill selection becomes the dominant failure point, with evidence of phase transition–like degradation in selection accuracy.

Evaluation

The primary strength of this paper is its role as a field-defining synthesis. It provides:

a clean abstraction of skills vs tools vs prompts

a structured taxonomy of skill acquisition and deployment

a consolidation of recent empirical findings (especially security)

Crucially, it surfaces the scaling problem in skill selection as a first-order research challenge, which is highly relevant for system design.

However, the paper has clear limitations:

No original architectural contribution  
Mechanisms such as progressive disclosure and SKILL.md are adopted from existing standards, not proposed.

No retrieval or routing solution  
Skill selection is identified as a bottleneck but remains completely unaddressed technically.

Lack of formalization  
There is no mathematical or algorithmic framing of:

skill retrieval

routing complexity

selection error

Descriptive rather than analytical  
The “phase transition” insight is observational, without modeling or controlled analysis.

Overall, the paper functions more as a taxonomy \+ problem statement than a technical contribution.

Relevance

This work is highly relevant as a problem-framing and positioning reference, but not as a solution.

It is useful for:

defining the skill abstraction layer

motivating why large-scale skill retrieval is difficult

identifying open challenges (especially selection at scale)

It does not address:

scalable retrieval architectures

ranking or routing algorithms

embedding or semantic matching issues

Therefore, its role in your thesis is:

To justify the problem space and highlight the unresolved bottleneck — not to provide a method.

### Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large Language Model Functionality

Summary

This paper presents a large-scale empirical analysis of over 40,000 agent skills collected from a public marketplace, with the goal of characterizing the emerging skill ecosystem for LLM agents. It studies skill growth, structure, redundancy, usage patterns, and safety risks.

The authors show that skill ecosystems grow rapidly and exhibit heavy-tailed distributions in length, significant intent-level redundancy, and clear mismatches between supply and user demand. They further introduce a taxonomy of skill types and perform LLM-based auditing to quantify safety risks.

Rather than proposing new architectures or algorithms, the paper provides a quantitative snapshot of skills as an infrastructure layer, highlighting systemic issues that arise at scale.

Evaluation

The primary strength of this paper lies in its data-driven grounding of the skill paradigm. Unlike conceptual or architectural works, it reveals how skills behave in practice, exposing critical properties that are often ignored in theoretical discussions.

In particular, three findings are highly impactful:

High redundancy (\~46%)  
→ Indicates that skill retrieval operates over a noisy and duplicated search space, not a clean library

Heavy-tailed skill length distribution  
→ Suggests that naive loading strategies will fail due to context and cost variability

Supply–demand mismatch  
→ Implies that frequency-based or popularity-based retrieval may be misleading

Additionally, the paper highlights non-trivial safety risks, showing that a significant portion of skills can perform state-changing or system-level actions, which introduces constraints beyond pure retrieval accuracy.

However, the paper has clear limitations:

No retrieval or routing method  
It identifies problems but does not propose solutions

Weak semantic redundancy analysis  
Embedding-based duplicate detection is acknowledged as unreliable

No formal modeling of retrieval complexity  
Observations remain empirical rather than theoretical

Marketplace bias  
Results depend on a single platform snapshot

Overall, the paper is diagnostic, not prescriptive.

Relevance

This work is highly relevant as empirical evidence for the difficulty of large-scale skill retrieval.

It directly supports your thesis by showing that:

Skill retrieval is not standard IR → it involves redundancy, imbalance, and noise

Scaling issues arise not only from context size but from ecosystem structure

Retrieval must consider:

duplication

distribution skew

safety constraints

However, it does not address:

retrieval architectures

ranking algorithms

routing strategies

Thus, its role in your work is:

To empirically justify why skill retrieval is a hard and under-solved problem in real-world systems.

### Agent Skill Framework: Perspectives on the Potential of Small Language Models in Industrial Environments

Summary

This paper investigates the applicability of the Agent Skill paradigm to small language models (SLMs) in industrial environments where API-based large models are impractical due to cost and security constraints. It introduces a formal POMDP-based formulation of skill usage, modeling skill selection, information disclosure, and execution as sequential decision-making under uncertainty.

The authors design an evaluation framework comparing three context-engineering strategies—Direct Instruction, Full-Skill Instruction, and Agent Skill Instruction—across multiple datasets, including a real-world insurance claims benchmark. Experiments span models from 270M to 80B parameters.

The results show that while Agent Skills improve performance for moderately sized models, small models fail to reliably perform skill selection, and performance degrades significantly as the number of available skills increases.

Evaluation

The main strength of this paper lies in its combination of formal modeling and empirical validation. The POMDP formulation provides a principled interpretation of skill usage as an information-constrained control problem, which is a meaningful step toward theoretical grounding of agent systems.

Empirically, the paper provides strong evidence for several critical phenomena:

Skill selection is the primary bottleneck, even in small candidate sets

Scaling failure in skill libraries, where accuracy declines with increasing number of skills

Model capacity threshold, below which skill-based frameworks are ineffective

The analysis of VRAM-time efficiency also adds practical relevance for deployment in resource-constrained environments.

However, the paper has several limitations:

No retrieval or routing algorithm is proposed  
Skill selection is measured but not improved

Simplified experimental setup  
Only 4–6 distractor skills in most experiments → underestimates real-world complexity

Limited task diversity  
Focuses primarily on classification and tagging tasks

Weak treatment of semantic retrieval  
No analysis of embedding quality or similarity metrics

Progressive disclosure failure is observed but not explained  
The underlying cause (reasoning vs representation vs retrieval) remains unclear

Overall, the paper is diagnostic and partially theoretical, but not solution-oriented.

Relevance

This paper is highly relevant as direct empirical evidence of the skill retrieval and routing problem.

It contributes to your thesis by showing that:

Skill selection is non-trivial even at small scale

Scaling introduces systematic degradation in routing accuracy

Model capability is tightly coupled with retrieval effectiveness

Progressive disclosure alone is insufficient without reliable selection

However, it does not address:

scalable retrieval architectures

ranking or routing strategies

semantic matching improvements

Thus, its role is:

To empirically validate that skill retrieval and selection is the central bottleneck in agent systems, especially under scaling constraints.

### Agent, Sub-Agent, Skill, or Tool? A Practitioner's Guide to Extending Agentic AI Systems

Summary

This paper proposes a control-centric taxonomy for agentic AI systems, distinguishing tools, skills, sub-agents, and agents based on who owns execution flow rather than perceived intelligence. It introduces skills as modular procedural knowledge units that improve context efficiency via progressive disclosure, and identifies three canonical orchestration patterns: tool-centric, hierarchical, and decentralized multi-agent systems. Through case studies and empirical synthesis, the paper argues that architectural complexity—especially multi-agent designs—often degrades performance unless strictly required by the task.

Evaluation

The primary strength of this paper is its conceptual clarity and practical relevance. The control-based taxonomy is clean, orthogonal, and resolves a major ambiguity in the agent literature where “agent” is overloaded. The introduction of skills as a distinct abstraction is useful, particularly in separating capability (tools) from procedural knowledge (skills)—a distinction often ignored in prior work.

However, the contribution is primarily descriptive rather than technical:

No new algorithms, models, or retrieval methods

No formal evaluation or benchmarking framework

Claims such as “96% context reduction” rely on illustrative comparisons rather than rigorous experiments

Additionally, while the paper critiques multi-agent systems effectively, it does not provide:

a formal model of coordination cost

or quantitative trade-off analysis across architectures

The “skill” abstraction also depends heavily on Anthropic’s existing paradigm, meaning the novelty lies more in systematization than invention.

Relevance

This paper is highly relevant as architectural grounding for research on:

LLM agents

tool/skill ecosystems

orchestration design

However, it does not directly solve core research problems such as:

scalable tool/skill retrieval

routing under large tool libraries

embedding misalignment

context explosion in selection

### SkillNet: Create, Evaluate, and Connect AI Skills

Summary

This paper introduces SkillNet, a large-scale infrastructure for creating, evaluating, and organizing agent skills as structured, reusable assets. Unlike prior work that treats skills as isolated modules, SkillNet models skills as nodes in a relational network, enabling connections such as similarity, dependency, and composition.

The framework integrates three key components:  
(1) a large-scale repository containing over 200,000 skills,  
(2) a multi-dimensional evaluation system assessing safety, executability, and efficiency, and  
(3) a skill relation graph that enables structured reasoning over skill libraries.

Empirical results on multiple agent benchmarks show that structured skill reuse significantly improves performance and efficiency, demonstrating the value of organizing skills beyond flat representations.

Evaluation

The main strength of this paper is its systems-level contribution to skill infrastructure. It moves beyond the assumption that skills are independent units and instead models them as part of a connected knowledge graph, which is a meaningful step toward scalable skill ecosystems.

The introduction of a multi-dimensional evaluation framework is also notable, as it addresses the often-overlooked issue of skill quality and reliability at scale. The combination of LLM-based scoring and sandbox execution provides a practical and scalable validation pipeline.

However, several limitations are critical:

No retrieval or routing algorithm  
While the paper enables structured skill organization, it does not define how agents should efficiently select skills at runtime

Graph construction is heuristic and static  
Relations are inferred but not optimized for retrieval performance

No scalability analysis of selection complexity  
The impact of graph size on retrieval efficiency is not studied

Weak integration with decision-making  
The system organizes skills but does not model how agents choose among them

Overall, the paper contributes to the representation and infrastructure layer, but leaves the retrieval and routing problem unresolved.

Relevance

This paper is highly relevant as a structural alternative to flat skill retrieval.

It contributes to your thesis by suggesting that:

Skill libraries should not be treated as flat sets

Structural information (graph relations) can improve:

retrieval

composition

reasoning

However, it does not address:

ranking strategies

routing policies

embedding alignment

selection under large candidate sets

Thus, its role is:

To motivate structured retrieval (graph-based or hierarchical), while leaving the actual retrieval mechanism as an open problem.

### Skills Are the New Apps – Now It’s Time for Skill OS

Summary

This paper presents an empirical study of nearly 100,000 real-world agent skills and argues that skills should be treated as first-class execution units managed by a system layer (“Skill OS”) rather than as prompt-level text. The authors identify six key properties of skills in practice, including procedural structure, semi-deterministic content, execution variability, environment dependencies, and cross-session reuse.

Based on these findings, the paper proposes a Skill OS abstraction, analogous to traditional operating systems, which provides runtime support for skill execution through caching, environment construction, global management, fault handling, and security enforcement. The goal is to address inefficiencies and unreliability caused by treating skills as prompt-time artifacts.

Evaluation

The main strength of this paper is its empirical grounding combined with systems-level insight. The large-scale analysis reveals concrete properties of skills that are often overlooked, particularly the prevalence of semi-deterministic blocks and execution drift under semantic equivalence. These findings provide a strong argument that current prompt-centric execution models are fundamentally inefficient.

The Skill OS abstraction is conceptually compelling, especially in drawing parallels with traditional operating systems to justify:

deterministic execution boundaries

caching and reuse mechanisms

system-level safety enforcement

However, the paper has several limitations:

No concrete implementation or system prototype  
The Skill OS remains largely conceptual

No evaluation of proposed system design  
There is no benchmark showing improvements from Skill OS

No treatment of retrieval or selection  
The paper assumes skills are already selected, focusing only on execution

Semantic matching is underspecified  
The idea of matching semantically equivalent executions is proposed but not formalized

Overall, the paper contributes a systems perspective, but does not provide algorithmic or empirical validation of the proposed architecture.

Relevance

This paper is highly relevant for understanding the execution layer of skill-based systems, particularly:

why prompt-based skill execution is inefficient

how system-level abstractions can improve reliability and reuse

the role of caching, environment management, and safety

### Evolution of Semantic Similarity—A Survey

\#\#\# Summary

The paper \*\*“Evolution of Semantic Similarity—A Survey”\*\* provides a comprehensive overview of methods for measuring semantic similarity in natural language processing. It traces the development of techniques from early lexical approaches such as Bag-of-Words and TF-IDF to more advanced methods including knowledge-based systems, corpus-based models, deep neural networks, and hybrid approaches. The survey organizes these methods into four main categories—knowledge-based, corpus-based, deep learning–based, and hybrid—and explains the underlying principles, representative algorithms, and typical use cases of each. It also reviews widely used benchmark datasets (e.g., STS, SICK, SimLex) and discusses how similarity is evaluated through correlation with human judgments. Overall, the paper serves as a unifying framework that synthesizes decades of research on semantic similarity and highlights the progression toward more context-aware and data-driven representations.

\* \* \*

\#\#\# Evaluation

The paper is strong in its \*\*systematic taxonomy and breadth of coverage\*\*, clearly distinguishing between fundamentally different paradigms (symbolic vs statistical vs neural). It provides useful conceptual clarity by linking methods to their underlying assumptions (e.g., ontology structure vs distributional hypothesis). However, as a survey, it lacks \*\*experimental novelty or unified empirical comparison\*\*, instead summarizing results across disparate works. More importantly, the discussion remains focused on \*\*pairwise similarity computation\*\*, without addressing system-level concerns such as retrieval scalability, ambiguity resolution in large candidate sets, or decision-making under competing similar options. Additionally, while modern neural methods are included, the analysis does not deeply engage with emerging issues like context efficiency or retrieval-augmented architectures.

\* \* \*

\#\#\# Relevance

This paper is relevant as a \*\*foundational reference for semantic similarity\*\*, which underpins many retrieval-based systems, including tool and skill selection in LLM agents. It provides the conceptual basis for approaches such as embedding-based retrieval and similarity scoring. However, it does not address key challenges central to scalable agent systems, such as \*\*structured retrieval, hierarchical routing, or handling large and semantically overlapping tool libraries\*\*. As such, it is best positioned as a baseline reference that motivates the limitations of flat similarity-based retrieval, rather than a direct solution to skill or tool selection problems in large-scale agent architectures.

### MCP-Zero: Active Tool Discovery for Autonomous LLM Agents

Summary

MCP-Zero introduces an active tool discovery framework that transforms tool selection in LLM agents from a passive retrieval process into an iterative, model-driven capability acquisition workflow. Instead of injecting all tool schemas into context or performing one-shot retrieval based on user queries, MCP-Zero enables the agent to generate structured tool requests, which are used to retrieve relevant tools through a hierarchical routing mechanism. The system combines three components: active tool request generation for semantic alignment, hierarchical semantic routing for efficient coarse-to-fine retrieval, and iterative capability extension for multi-step toolchain construction. The authors also introduce MCP-tools, a dataset containing 308 servers and 2,797 tools. Experiments demonstrate that MCP-Zero significantly improves scalability, maintaining high retrieval accuracy while reducing token usage by up to 98% in large-scale and multi-turn scenarios.

Evaluation

The paper’s primary strength lies in its architectural reframing of tool selection as an active information acquisition process, rather than a static retrieval problem. The introduction of intermediate structured requests significantly improves semantic alignment and reduces search complexity. The hierarchical routing mechanism is also a practical and scalable design, effectively addressing context explosion and attention dilution. However, the method still relies heavily on semantic similarity for ranking, limiting its ability to distinguish between tools that are semantically similar but procedurally different. Additionally, the framework assumes that the LLM can reliably generate accurate tool requests; errors at this stage propagate downstream and may degrade performance. While iterative invocation enables multi-step workflows, the system lacks a principled global planning mechanism, instead relying on local, step-wise refinement.

Relevance

This paper is highly relevant to research on scalable tool and skill retrieval in LLM agents, as it directly addresses key challenges such as large tool library scaling, context efficiency, and multi-step tool selection. It demonstrates that structure-aware and hierarchical retrieval combined with agent-driven request generation can significantly outperform flat similarity-based approaches. However, it does not fully solve the problem of selecting among semantically similar but procedurally distinct skills, nor does it introduce a structured representation of skills beyond textual descriptions. As such, it serves as a strong intermediate step toward more advanced retrieval architectures, particularly those involving hierarchical or graph-based representations, but leaves open the problem of robust skill disambiguation at scale.

###  Uni-Skill: Building Self-Evolving Skill Repository for Generalizable Robotic Manipulation

Summary

Uni-Skill proposes a unified framework for skill-centric robotic learning that enables dynamic skill expansion and automatic skill acquisition. Unlike traditional approaches that rely on fixed skill libraries, Uni-Skill introduces a skill-aware planning mechanism that detects missing capabilities and generates new skill descriptions at runtime. These newly defined skills are grounded through an automatic skill evolution process, which organizes large-scale unstructured robotic videos into a hierarchical repository called SkillFolder. This repository structures skills across multiple levels of abstraction, from high-level verb categories to fine-grained execution examples. At deployment, relevant skill demonstrations are retrieved from this hierarchy to support few-shot skill implementation without manual supervision. Experimental results show that Uni-Skill significantly improves zero-shot generalization and achieves strong performance on both simulation and real-world robotic tasks.

Evaluation

The paper makes a significant contribution by introducing dynamic skill evolution and hierarchical skill representation, addressing a fundamental limitation of fixed skill libraries. The use of SkillFolder provides a structured approach to organizing skills and enables efficient retrieval of relevant demonstrations, improving generalization and reducing reliance on manual annotation. The integration of skill-aware planning with automatic skill grounding is also a strong design, allowing the system to handle unseen tasks. However, the approach depends heavily on the quality of automatically annotated video data, which may introduce noise and affect retrieval accuracy. Additionally, while the hierarchical structure improves organization, retrieval still relies on semantic matching and may struggle with fine-grained disambiguation between similar skills. Finally, the system is domain-specific (robotics), and its applicability to general LLM-based tool or skill systems remains uncertain.

Relevance

This paper is highly relevant to research on scalable skill retrieval and representation, as it directly addresses key challenges such as skill library scalability, dynamic skill generation, and structured skill organization. In particular, the introduction of a hierarchical skill taxonomy (SkillFolder) aligns closely with approaches that move beyond flat skill representations, providing a concrete example of how structure can improve retrieval and generalization. Unlike many prior works that focus solely on retrieval mechanisms, Uni-Skill emphasizes skill representation and evolution, making it directly applicable to problems involving large, growing skill libraries. However, its focus on robotic manipulation means that its methods may require adaptation for general-purpose LLM agents, particularly in handling abstract or non-physical skills.

### Struc-EMB: The Potential of Structure-Aware Encoding in Language Embeddings  Summary

Struc-Emb introduces a structure-aware embedding paradigm that integrates relational information directly into the encoding process of large language models. Unlike traditional approaches that encode text independently and combine structural context post hoc, Struc-Emb incorporates related segments during encoding via two mechanisms: sequential concatenation and parallel key-value caching. These methods allow embeddings to capture interactions between a target text and its structurally related context, such as hyperlinks or graph connections. The framework also introduces context distillation to mitigate noise and semantic balancing to preserve target semantics. Extensive experiments across retrieval, clustering, classification, and recommendation tasks demonstrate that structure-aware encoding consistently outperforms text-only and post-hoc baselines, particularly in tasks requiring multi-hop reasoning or contextual disambiguation.

Evaluation

The paper makes a strong contribution by demonstrating that embedding quality can be significantly improved through in-process integration of structural information, rather than relying on post-hoc aggregation. The proposed methods are practical and scalable, and the analysis of trade-offs between sequential and parallel encoding provides valuable design insights. However, the approach remains fundamentally embedding-based and relies on similarity for downstream retrieval, limiting its ability to distinguish between semantically similar but functionally distinct entities. Additionally, the structural information is treated as contextual neighbors rather than explicit procedural or hierarchical representations, which constrains its applicability to domains where deeper structural reasoning is required.

Relevance

This paper is highly relevant to research on scalable skill retrieval, as it provides strong empirical evidence that incorporating structural information into representations significantly improves retrieval performance. Its structure-aware encoding paradigm aligns closely with the need for richer skill representations beyond flat textual descriptions. However, it does not address procedural distinctions between skills or provide mechanisms for reasoning over structured representations, leaving open the problem of disambiguating semantically similar but procedurally distinct skills. As such, it serves as a critical foundation for representation-aware retrieval, but not a complete solution for skill selection in large-scale agent systems.

###  Equipping Retrieval-Augmented Large Language Models with Document

### Structure Awareness 

Summary

This paper introduces RDR², a structure-aware retrieval-augmented generation framework that extends the standard Retrieve-and-Read paradigm by incorporating document hierarchy into the retrieval process. Documents are represented as tree structures (Document Structure Trees), and an LLM-based router iteratively navigates these structures through actions such as selecting relevant content, expanding promising sections, or terminating exploration. Unlike traditional RAG systems that treat passages as independent chunks, RDR² preserves structural relationships and dynamically assembles evidence through multi-step routing. Experimental results across multiple QA benchmarks demonstrate consistent improvements, highlighting the importance of structural awareness in complex knowledge synthesis tasks.

Evaluation

The paper provides a strong empirical demonstration that incorporating document structure and iterative routing significantly improves retrieval-augmented generation performance. The LLM-based routing mechanism is intuitive and effective, particularly for multi-hop reasoning tasks. However, reviewer feedback highlights that the approach remains largely heuristic, relying on LLM decision-making without a principled optimization objective. Additionally, the structural representation is limited to document hierarchies and does not generalize to more complex relational or procedural structures. The dependence on initial embedding-based retrieval also constrains recall under semantic ambiguity. As such, while the framework is a meaningful step toward structure-aware retrieval, it does not fundamentally resolve challenges in scalable and precise selection.

Relevance

This work is highly relevant as it provides strong empirical evidence that structure-aware retrieval significantly outperforms flat retrieval approaches. It directly supports the hypothesis that incorporating structural information improves selection accuracy and downstream task performance. However, it does not address the challenge of selecting among semantically similar but procedurally distinct skills, as it focuses on document navigation rather than skill representation or execution logic. It therefore serves as a strong baseline for structured retrieval, but highlights the need for more expressive representations and routing mechanisms in scalable agent systems.

###   SkillRouter: Retrieve-and-Rerank Skill Selection for LLM Agents at Scale

Summary

SkillRouter presents a large-scale empirical study of skill routing in LLM agent systems, focusing on the challenge of selecting relevant skills from highly homogeneous skill repositories containing tens of thousands of entries. The authors demonstrate that commonly used skill metadata (name and description) is insufficient for accurate retrieval, and that the full skill implementation (body) is the dominant signal for selection. Based on this finding, they propose a two-stage retrieve-and-rerank pipeline that incorporates full skill text in both embedding-based retrieval and cross-encoder reranking. Experiments on a benchmark of approximately 80K skills show that their approach achieves strong performance, significantly outperforming metadata-based baselines.

Evaluation

The paper makes a highly significant contribution by empirically demonstrating that semantic descriptions alone are insufficient for skill selection, and that detailed implementation information is essential in large-scale, overlapping skill environments. The experimental design is rigorous, with large-scale datasets and controlled ablations that clearly isolate the impact of different skill components. However, the approach remains fundamentally similarity-based, relying on embedding and reranking over flat text representations of skill bodies. It does not model the internal structure or procedural dependencies of skills, nor does it introduce reasoning-based selection mechanisms. As a result, while it substantially improves retrieval accuracy, it does not fully resolve ambiguity among semantically similar but procedurally distinct skills.

Relevance

This paper is extremely relevant to research on scalable skill retrieval, as it directly addresses the core challenge of selecting among large numbers of semantically similar skills. It provides strong empirical evidence that richer representations—specifically full implementation text—are necessary for accurate selection, challenging the common assumption that metadata suffices. However, it stops short of modeling skills as structured procedural entities or incorporating structure-aware retrieval mechanisms. Therefore, it serves as a critical empirical foundation for the thesis, motivating the need for structured skill representations and more principled retrieval approaches beyond similarity-based ranking.

###   CUA-Skill: Develop Skills for Computer Using Agent

Summary

CUA-Skill proposes a structured skill abstraction framework for computer-using agents, modeling skills as parameterized procedural units composed of execution graphs and composition graphs. Unlike traditional approaches that represent interaction as flat sequences of actions, CUA-Skill captures reusable workflows with branching execution paths and contextual parameters, enabling scalable skill reuse across applications. The framework integrates these structured skills into a retrieval-augmented agent pipeline, where relevant skills are selected and instantiated based on user queries. Empirical results demonstrate improved robustness and success rates in multi-step desktop tasks, highlighting the benefits of structured skill representation for complex environments.

Evaluation

The paper makes a strong contribution in formalizing skills as structured procedural entities, introducing execution graphs and compositional workflows that better reflect real-world task execution. This representation improves modularity, reusability, and robustness, and aligns well with human procedural reasoning. However, the retrieval mechanism remains largely conventional, relying on embedding-based and lexical matching over skill descriptions without incorporating the underlying structural information. As a result, the system does not fully address ambiguity among semantically similar skills, particularly in large-scale settings where procedural differences are critical.

Relevance

This paper is highly relevant to research on skill representation, providing a concrete and scalable model of skills as structured procedural graphs. It supports the argument that skills should not be treated as flat textual descriptions, but as structured entities with execution semantics. However, it does not address how such structured representations can be leveraged for retrieval and selection. Therefore, it serves as a foundational representation framework that motivates the need for structure-aware retrieval mechanisms, directly aligning with the thesis objective of improving skill selection in large-scale skill libraries.