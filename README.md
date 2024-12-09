# Can Large Language Models Reduce the Cost of Extracting Data from Electronic Health Records for Research?

This code is made publically available for reviewers of the associated paper.

## Abstract

Objective:  Much medical data is only available in unstructured electronic health records (EHR). These data can be obtained through manual (human) extraction or programmatic natural language processing (NLP) methods. We estimate that NLP only becomes economically competitive with manual extraction when there are ~6500 EHRs records. We have found that there is interest from clinicians and researchers in using NLP on projects with fewer records. We examine whether a large language model (LLM) can be used to reduce the cost of NLP to make it economically competitive for such projects, and study the feasibility of such framework for accuracy.

Methods:  We developed an NLP pipeline using an off-the-shelf open LLM to extract breast cancer ER, PR, and HER2 biomarker data. Pipeline development stopped when the prompts’ performances were competitive with manual extraction. The development time and extraction performance were compared to those of an existing rule-based (RB) NLP pipeline.

Results:  The LLM pipeline produced performance competitive with manual data extraction with a hands-on development time that was $\sim$38\% that of the RB pipeline.

Discussion:  LLMs exhibit lower hands-on development costs compared to standard NLP techniques, but require significant and potentially costly computation resources.

Conclusion:  LLMs may potentially allow the economically competitive application of NLP to smaller projects if computation costs can be managed.
