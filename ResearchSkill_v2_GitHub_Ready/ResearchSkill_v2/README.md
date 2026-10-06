# ResearchSkill v2 — Open-Source Agent Skill Evaluation

## Project question
Does a structured Agent Skill measurably improve an open-weight AI agent on
research and fact-verification tasks?

## What is included
- 30-task evaluation dataset across 10+ categories
- Open-weight model support through Ollama
- Baseline vs Skill V1 vs Skill V2
- Latency measurement
- Transparent fact-coverage score
- Heuristic unsupported-claim indicator
- Category-level analysis
- GitHub-ready README and MIT license
- Agent Skill files with YAML frontmatter

## Important metric note
The unsupported-claim/hallucination indicator is a lightweight heuristic, not
a ground-truth hallucination detector. For a competition-grade evaluation,
add human judging or a separately validated evaluator.

## Setup

1. Install Python 3.10+.
2. Install Ollama and make sure its local service is running.
3. Pull an open-weight model, for example:

    ollama pull qwen2.5:3b

4. Install Python packages:

    python -m pip install -r requirements.txt

## Interactive demo

    python chat.py

The demo compares the baseline, Skill V1, and Skill V2 on the same question.

## Full benchmark

    python run_evaluation.py --model qwen2.5:3b --mode all

Quick smoke test:

    python run_evaluation.py --model qwen2.5:3b --limit 3 --mode all

## Outputs

- results/raw_results.json — raw answers and latency
- results/detailed_results.csv — task-level scores
- results/summary.csv — overall comparison
- results/category_scores.csv — performance by task category

## How to present the experiment

Baseline:
  Open-weight model → Question → Answer

Skill V1:
  Open-weight model + basic structured skill → Question → Answer

Skill V2:
  Open-weight model + improved evidence/uncertainty skill → Question → Answer

Use the same dataset for every configuration. Compare:
- mean score
- mean latency
- unsupported-claim indicator
- category-level performance

## Research interpretation

A strong result is not necessarily "V2 wins every task." Report:
1. where the skill improves performance,
2. where it has little effect,
3. where it increases latency,
4. where it creates or reduces unsupported-claim risk.

## GitHub submission checklist

- [x] Open-weight AI is central
- [x] Original Agent Skill
- [x] Public-repository-ready structure
- [x] MIT license
- [x] Documentation
- [x] Evaluation dataset
- [x] Baseline comparison
- [x] Multiple skill versions
- [x] Measured latency
- [x] Results export
- [ ] Add your final measured results after running locally
- [ ] Push repository to GitHub
