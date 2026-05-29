## **Working thesis focus**

This thesis investigates how agent skills should be represented and retrieved so that an agent can distinguish between skills that are semantically similar in description but procedurally different in execution. The central problem is that as skill libraries grow, flat natural-language descriptions may become insufficient for accurate selection, while naive exposure of all skill metadata to the model can create context overload. Anthropic’s Agent Skills design is a useful practical reference point because it treats skills as filesystem artifacts centered on SKILL.md, with selective loading rather than unconditional full-context inclusion.

## **Core distinction: artifact vs representation vs retrieval policy**

A major conceptual clarification for this thesis is that three layers must be separated.

First, the **skill artifact** is the actual stored object in the library. In your setting, this is typically a skill directory containing SKILL.md, plus optional scripts, documents, and resources.

Second, the **selection representation** is the form in which the skill is represented for skill choice. This is not necessarily the same as the artifact itself. A skill may physically be a markdown file and some resources, but for retrieval it may be represented as a flat text description, a structured schema, a hierarchy path, or a graph node with typed edges.

Third, the **retrieval policy** is the process by which the system selects candidate skills. This could be no retrieval at all, embedding-based nearest-neighbor retrieval, hierarchical traversal, graph expansion, LLM routing, or a hybrid pipeline with reranking.

This distinction is necessary because otherwise graph, tree, embedding, and all-in-context baselines become mixed together even though they operate at different layers.

## **Research questions**

### **Previous assignment wording, now developed**

**RQ1:** How can agent skills be represented and retrieved so that agents can accurately select among semantically similar but procedurally distinct skills as skill libraries scale?

**RQ2:** To what extent do structure-aware skill representations improve retrieval accuracy, context efficiency, and downstream task performance compared with flat description-based skill retrieval?

These questions are still useful as the submitted assignment framing, but the second question now looks too close to a simple "structure-aware versus flat" comparison. The project has developed toward a more precise contribution: identifying which information a skill representation must preserve, and then testing how different retrieval strategies use or lose that information.

### **Current working research questions**

**RQ1:** What information must agent skill representations preserve to distinguish semantically similar but procedurally distinct skills at scale?

**RQ2:** How do retrieval strategies that use flat text, dense embeddings, structured procedural fields, or hybrid reranking differ in accuracy, efficiency, and failure modes when applied to scalable skill libraries?

This framing keeps retrieval strategies in scope, but makes representation quality the core research object. The thesis does not have to begin by claiming a wholly novel architecture. Instead, it can compare representation-and-retrieval families, identify which procedural properties matter, and then optionally propose a refined or hybrid method if the evidence justifies it.

## **What “structure-aware representation” means here**

In this thesis, a **flat representation** means the skill is represented for selection mainly as unstructured natural language, such as a name, short description, and perhaps an example, treated as one text unit.

A **structure-aware representation** means the selection representation explicitly preserves internal organization relevant to procedural disambiguation. This may include:

* preconditions and postconditions,  
* inputs and outputs,  
* required tools,  
* workflow steps,  
* failure cases,  
* dependencies on other skills,  
* hierarchical capability placement,  
* graph relations such as prerequisite, compositional, or sibling relations.

Under this definition, graph-based and tree-based methods are both structure-aware representations. Schema-based and step-based encodings also count as structure-aware even if they are simpler than full graphs.

## **Candidate representation families**

### **1\. Full flat exposure baseline**

All skill metadata is placed directly into the agent context, and the model selects from what it sees. This is not a trivial strawman. It is closely related to practical progressive-disclosure systems because all skill names/descriptions may be available initially even when deeper content is only loaded later. The weakness is likely context growth and confusion as the library scales.

### **2\. Flat description-based retrieval baseline**

Each skill is represented as plain text and retrieved using standard dense retrieval or similar semantic matching. This is the most natural comparison point for RQ2 because your question explicitly contrasts structure-aware skill representations against flat description-based retrieval.

### **3\. Schema-based structured representation**

Each skill is represented through explicit fields such as purpose, preconditions, required tools, inputs, outputs, and steps. This may help by surfacing procedural distinctions that are blurred in free text.

### **4\. Hierarchical or tree-based representation**

Skills are organized into capability hierarchies or coarse-to-fine routing structures. This may reduce search complexity and improve efficiency, but may suffer from brittle early routing decisions.

### **5\. Graph-based representation**

Skills are represented as nodes with edges encoding relations such as dependency, compositionality, similarity, prerequisite, or tool overlap. This may preserve richer relations than a tree, but the quality of retrieval depends heavily on graph construction quality and edge semantics.

### **6\. Hybrid pipelines**

These combine representation and routing mechanisms, for example flat retrieval followed by structured reranking, or hierarchical narrowing followed by local graph-based reranking. These may perform best empirically but can make attribution harder.

## **Likely thesis contribution**

The most defensible contribution is threefold.

First, a clear conceptual framework distinguishing skill artifact, selection representation, and retrieval policy.

Second, a controlled evaluation of representation families under a skill-selection benchmark specifically designed to stress semantic confusability and procedural distinctness.

Third, a finding about which structural properties improve retrieval accuracy, context efficiency, and downstream task performance. If existing methods prove inadequate, this can motivate a refined or hybrid representation as a later-stage contribution rather than an a priori assumption.

## **Recommended baselines and comparisons**

A clean experimental ladder would be:

**Baseline 0:** All skill metadata exposed in context, no external retrieval.  
 **Baseline 1:** Flat description-based retrieval.  
 **Structured method A:** Schema-based structured retrieval.  
 **Structured method B:** Hierarchical/tree-based retrieval.  
 **Structured method C:** Graph-based retrieval.

You do not need to implement all structured methods if time is limited. A minimum viable thesis could compare:

* all-in-context exposure,  
* flat description retrieval,  
* one strong structure-aware alternative.

A stronger thesis would compare at least two structure-aware families.

## **Benchmark design**

The benchmark should be intentionally aligned with the research problem.

The skill library should contain skills that are:

* semantically similar in name or description,  
* but procedurally distinct in steps, prerequisites, or effects.

The benchmark should vary library scale so that the effect of growth can be observed.

The benchmark should include both:

* retrieval-only evaluation, and  
* downstream agent-task evaluation after retrieved skills are supplied.

This is important because a method may retrieve plausible skills while still harming execution quality, or it may improve retrieval accuracy at unacceptable context or latency cost.

## **Evaluation dimensions**

The core evaluation dimensions already implied by RQ2 are:

**Retrieval accuracy**  
 Did the system retrieve the correct skill or include it in top-k candidates?

**Context efficiency**  
 How much context/token budget was consumed in the selection process and during skill loading?

**Downstream task performance**  
 After using retrieved skills, did the agent complete the task correctly?

Additional useful dimensions are:

* latency,  
* robustness as the number of skills increases,  
* sensitivity to semantic overlap,  
* ablations on representation content.

## **Failure modes to analyze in the literature and experiments**

For flat exposure, the key failure mode is context overload and increased competition among many visible skills.

For flat retrieval, the key failure mode is semantic collapse: skills that look similar lexically may be confused because the representation under-specifies procedure.

For schema-based methods, the risk is that the schema may be expensive to author or may fail to capture all relevant procedural distinctions.

For tree-based methods, the risk is routing brittleness: if the wrong branch is selected early, the correct skill may become unreachable.

For graph-based methods, the risk is graph construction quality. If edges reflect only semantic similarity rather than procedurally meaningful relations, the graph may reproduce the same confusion it was meant to solve.

For hybrid methods, the main issue is complexity and attribution. Gains may be real, but it can become difficult to isolate whether the improvement comes from the representation, the retriever, or the reranker.

## **High-level methodology**

Phase 1 should define the design space and implement representative baselines. The goal is not to “explore some methods” vaguely, but to instantiate a small number of clearly defined representation families.

Phase 2 should construct or refine a benchmark that isolates semantic confusability and procedural distinctness.

Phase 3 should run retrieval and downstream experiments under varying library sizes and compare the methods on the agreed metrics.

Phase 4 should analyze failure modes and, if justified, synthesize a refined or hybrid representation informed by the results.

## **Recommended framing of the research problem**

Existing skill selection approaches often rely on flat natural-language descriptions or general semantic similarity, which may not adequately distinguish semantically similar but procedurally distinct skills. As skill libraries scale, this can reduce retrieval precision, inflate context usage, and degrade downstream task performance. While prior work has explored structured, hierarchical, and graph-based approaches, it remains unclear which representational properties most effectively preserve procedural distinguishability under scale. This thesis therefore investigates how different skill representations and retrieval policies affect retrieval accuracy, context efficiency, and downstream agent performance.

## **Recommended framing of the contribution**

This thesis does not merely claim that “graphs are better” or that “a new representation will be invented.” Instead, it contributes a clearer decomposition of the skill-selection problem, a controlled benchmark for semantically confusable skill libraries, and an empirical comparison of flat and structure-aware approaches. The final outcome may be either a strong empirical conclusion about existing methods or a refined representation motivated by the observed failure modes.
