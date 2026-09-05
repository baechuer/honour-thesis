## **What the assignment is actually asking you to do**

Task 1 is not asking for a pile of paper summaries. It requires a **critical literature review** that highlights gaps, is organized around research questions or claims, and demonstrates understanding of both the research contributions and the research methods in prior work. Task 2 then asks you to identify a research problem linked to that review, explain your intended contributions, and describe a convincing evaluation plan in enough detail to persuade the reader.

So your workflow should be:

1. define the problem your thesis is solving,  
2. organize the literature by the main competing ideas in that problem space,  
3. identify what each idea solves and where it fails,  
4. extract the unresolved gap,  
5. derive your research questions from that gap,  
6. then write Task 2 as the methodological answer to that gap.

## **The biggest mistake to avoid**

Do not structure Task 1 like this:

* Paper A summary  
* Paper B summary  
* Paper C summary  
* therefore my topic is important

That is the exact pattern that usually turns into narrative description rather than critical evaluation, which the rubric penalizes.

Instead, organize your review around **claims, method families, and unresolved tensions**.

## **The right overall structure for Task 1**

### **1\. Introduction**

State the broad domain and the central problem. For your topic, the introduction should say that agent skills allow reusable procedural capabilities to be packaged in libraries, but skill selection becomes difficult when the library grows and multiple skills are semantically similar yet procedurally distinct.

At the end of the introduction, state what the review will do. For example, say that the review examines how prior work represents and retrieves skills or similar capability artifacts, evaluates the limitations of flat and structured approaches, and identifies unresolved gaps that motivate the thesis research questions.

### **2\. Define the conceptual dimensions of the field**

Before reviewing method families, define the dimensions along which prior work differs. For your topic, a very useful framing is:

* selection representation,  
* retrieval policy,  
* evaluation protocol.

This keeps your review analytical.

### **3\. Review the main method families**

Use separate subsections for the major families:

* all-in-context or progressive-disclosure selection regimes,  
* flat description-based retrieval,  
* schema-based structured representations,  
* hierarchical/tree-based retrieval,  
* graph-based retrieval,  
* hybrid retrieval and reranking approaches.

Within each subsection, do not just say what the papers do. Answer the following:

* What problem is this family trying to solve?  
* What information does it encode?  
* What assumptions does it make?  
* What are its strengths?  
* Where does it fail relative to your research problem?

### **4\. Review evaluation practices and gaps**

This section is essential. Ask:

* How do prior papers evaluate retrieval?  
* Do they actually test semantically confusable skills?  
* Do they measure context efficiency?  
* Do they test downstream task success, or only retrieval relevance?  
* Are they evaluating tools, skills, workflows, or something else?

This section is where many of your strongest research gaps will come from.

### **5\. Synthesis section**

This is where you stop talking about individual method families and state the overall picture.

You want a synthesis paragraph that says something like:  
 prior work suggests that adding structure may improve retrieval and efficiency, but it remains unclear which representational properties are most useful for distinguishing semantically similar yet procedurally distinct skills, especially when the library scales and context budget matters.

This section should naturally lead into your RQs.

### **6\. Research gap and question transition**

Now explicitly state the gap and then your two research questions.

The literature review should make the RQs feel inevitable, not arbitrary.

## **How to analyze a paper properly**

For each paper, take notes under these headings:

**Problem addressed**  
 What concrete problem is the paper trying to solve?

**Object being represented**  
 Is it tools, skills, APIs, workflows, documents, or something else?

**Representation**  
 Flat text, schema, tree, graph, code artifact, embedding, etc.

**Retrieval/routing method**  
 No retrieval, dense retrieval, reranking, branch traversal, graph expansion, LLM router, etc.

**Evaluation**  
 What metrics and tasks are used?

**Strength**  
 What does the paper do well?

**Failure mode or limitation**  
 Where might it break, especially relative to semantically similar but procedurally distinct skills?

**Relevance to your thesis**  
 Does it help with problem framing, baseline construction, method design, or evaluation design?

This is the note-taking format that will stop your literature review from becoming descriptive.

## **How to identify failure modes**

Do not write generic complaints like “this method is complex” or “this approach is limited.”

Instead, tie the limitation to your research problem.

Use this pattern:

This method works by relying on X.  
 That means it assumes Y.  
 That assumption breaks when Z.  
 This matters for the present thesis because the thesis focuses on semantically similar but procedurally distinct skills.

Example:  
 A flat embedding-based retriever works by relying on semantic similarity in natural-language descriptions. This assumes that lexical or semantic proximity corresponds to skill relevance. That assumption breaks when two skills are described similarly but differ substantially in prerequisites, action sequence, or outputs. This matters here because the thesis problem is precisely procedural disambiguation under semantic overlap.

That is how you do critical evaluation.

## **How your literature review should lead to your RQs**

The logic should be:

There is a real problem in large skill libraries.  
 Existing approaches fall into several representation and retrieval families.  
 Each family addresses part of the problem but leaves important weaknesses.  
 Existing evaluation is not yet sufficient to determine which representational properties matter most.  
 Therefore, the following research questions arise.

That is the purpose of the literature review.

## **How to approach Task 2**

Task 2 should not introduce a completely new story. It should be the direct continuation of Task 1\.

A good Task 2 structure is:

### **1\. Research problem**

Write a short precise statement of the problem identified in the review.

### **2\. Intended contributions**

Say exactly what you intend to contribute. For your topic, likely contributions are:

* a conceptual decomposition of skill artifact, selection representation, and retrieval policy,  
* a controlled benchmark or evaluation setup for semantically confusable skills,  
* an empirical comparison of flat and structure-aware representations,  
* optionally a refined or hybrid method if the results support it.

### **3\. Method overview**

State which baselines and comparison methods you will implement.

### **4\. Evaluation plan**

State:

* what metrics you will report,  
* what data or benchmark you will use,  
* what comparisons you will make,  
* how you will show that results are convincing.

### **5\. Why this evaluation is convincing**

This is important for a high Task 2 mark. Explain why the chosen evaluation actually tests the research problem rather than a different easier problem.

## **Suggested wording for your Task 2 research problem**

A possible formulation is:

Current agent skill selection approaches often rely on flat natural-language descriptions or general semantic similarity, which may be insufficient for distinguishing semantically similar but procedurally distinct skills. As skill libraries scale, this can reduce retrieval precision, increase context overhead, and harm downstream agent performance. Although prior work has explored structured, hierarchical, and graph-based approaches, it remains unclear which skill representations best preserve procedural distinguishability while remaining context-efficient and effective in downstream use.

## **Suggested wording for your Task 2 contributions**

A strong but realistic contributions section would say:

This project aims to make three contributions. First, it will clarify the distinction between skill artifacts, selection representations, and retrieval policies in agent skill ecosystems. Second, it will construct or adapt an evaluation setting that stresses semantic confusability between procedurally distinct skills. Third, it will empirically compare flat and structure-aware skill representations on retrieval accuracy, context efficiency, and downstream task performance, and use these findings to identify which structural properties most improve skill selection.

## **Suggested wording for your Task 2 evaluation plan**

A solid evaluation paragraph would say:

The evaluation will compare at least two baselines and one or more structure-aware methods. The first baseline will expose all skill metadata directly in context without external retrieval. The second baseline will use flat description-based retrieval. Structure-aware methods may include schema-based, hierarchical, or graph-based representations. Methods will be evaluated on retrieval accuracy, top-k candidate quality, context or token cost, and downstream task success after retrieved skills are supplied to the agent. Experiments will vary library size and semantic similarity to determine how each method behaves under scale and confusability.

## **Practical writing process for you**

### **Step 1**

Make a paper spreadsheet with columns:

* citation  
* family  
* representation  
* retrieval policy  
* evaluation  
* strength  
* limitation  
* relevance to RQ1  
* relevance to RQ2

### **Step 2**

Group papers into your method families.

### **Step 3**

Write one synthesis paragraph per family, not one paragraph per paper.

### **Step 4**

After each family subsection, write a short concluding sentence about the unresolved issue that remains.

### **Step 5**

Write one synthesis section across all families.

### **Step 6**

Only then write the research gap and RQs.

### **Step 7**

Write Task 2 as the methodological response to that gap.

## **Recommended A3 section skeleton**

### **Task 1**

1. Introduction  
2. Skill retrieval as a scaling and disambiguation problem  
3. Flat selection and flat retrieval approaches  
4. Structure-aware approaches  
    4.1 Schema-based  
    4.2 Hierarchical/tree-based  
    4.3 Graph-based  
5. Hybrid retrieval and reranking approaches  
6. Evaluation practices and unresolved gaps  
7. Synthesis and research gap  
8. Research questions

### **Task 2**

1. Research problem  
2. Intended contributions  
3. Proposed approach  
4. Evaluation design  
5. Why the evaluation is convincing

## **Final advice**

Your literature review is successful if a reader can finish it and say:

* I understand the problem,  
* I understand the main existing solution families,  
* I see what each one contributes,  
* I see exactly what is still unresolved,  
* and I can see why these two research questions are the right next step.

That is the standard you should target for A3.

