---
title: "Automating IETF Insights Generation with AI"
layout: post
date: 2024-11-08 14:00
image: /assets/images/ietf-ai.png
tag:
- IETF
- AI
- automation
- research
category: blog
author: jaime
headerImage: true
---

**Note:** *AI-generated reports from this research are available at [ietf-ai-report](https://jaime.win/ietf-ai-report/) as a proof of concept, including downloadable PDFs and source LaTeX files.*

As a side project, I've been exploring how AI can automate **IETF report generation**. I [presented this work at RASPRG](https://datatracker.ietf.org/meeting/121/materials/slides-121-rasprg-automating-ietf-insights-generation-with-ai-01) during IETF 121, with the [full technical details](https://arxiv.org/pdf/2410.13301) available in the accompanying paper.

IETF working group reports are essential but **time-consuming to produce**. With hundreds of working groups meeting several times per year, the question is whether GenAI can reliably summarize technical discussions and extract meaningful insights.

IETF documents work particularly well with **large language models** because they use structured plaintext and markdown, have consistent sections like security considerations, and include standardized protocol interactions. RFCs are already part of most **LLM training datasets**, providing significant advantages over processing arbitrary documents.

The **workflow combines four stages**: data retrieval using `rsync` and crawling, preprocessing to normalize names and structure data, **RAG integration** with customized prompts, and report generation in LaTeX or Markdown with post-processing corrections.

I tested both **local and API-based models**:

| Model | Parameters | Type | Context Window |
|-------|------------|------|----------------|
| GPT-4 | 1.76T | API | 8,192 tokens |
| Claude 3 Sonnet | 175B | API | 100,000 tokens |
| Command-R | 35B | Local | 131,072 tokens |
| Mixtral | 46.7B | Local | 32,768 tokens |
| Llama 3 | 8B | Local | 8,192 tokens |

**Larger context windows** proved crucial for processing entire meeting transcripts without losing important details.

The system produces **generally accurate reports** with correct event descriptions, participant affiliations, and discussion summaries. For example, the generated report correctly identifies that the AIPREF Working Group had 98 participants from organizations like Google, Apple, and Cisco, and accurately summarizes key discussion points about vocabulary scope and attachment mechanisms.

![Sample snippet](/assets/images/aipref.png)

However, **hallucinations still occur** occasionally, even with ground truth material. The system sometimes invents details, though far less frequently than zero-shot queries.

The key insight is that **structured, domain-specific material** dramatically reduces hallucinations compared to general-purpose AI applications. This demonstrates AI can significantly reduce manual effort while maintaining reasonable accuracy.

**Next steps** include implementing better reasoning strategies like Chain of Thought, expanding cross-working group analysis, and potentially integrating this into the official IETF toolchain. For anyone interested in applying AI to technical documentation, the IETF provides an excellent testbed due to its **open records and structured formats**.
