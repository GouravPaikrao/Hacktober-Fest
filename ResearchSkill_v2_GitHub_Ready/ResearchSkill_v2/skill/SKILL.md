---
name: research-skill
description: A structured research and fact-verification workflow for open-weight AI agents. Use it when answering research questions, checking claims, comparing concepts, or when uncertainty and evidence quality matter.
---

# ResearchSkill

## Purpose
Improve answer reliability by making the agent explicitly structure a task before answering.

## Workflow
1. Identify the exact question and task type.
2. Break a multi-part question into atomic claims.
3. Separate known facts, assumptions, and inferences.
4. Identify what evidence would be needed to support each important claim.
5. Answer each part directly and concisely.
6. Do not invent sources, citations, statistics, or observations.
7. If evidence is unavailable, state the limitation rather than presenting an uncertain claim as verified.
8. Perform a final self-check for completeness, unsupported claims, and overconfidence.

## Output discipline
- Answer the user's actual question first.
- Keep factual claims proportional to available evidence.
- Do not claim that information was searched or verified externally unless an external source was actually available.
