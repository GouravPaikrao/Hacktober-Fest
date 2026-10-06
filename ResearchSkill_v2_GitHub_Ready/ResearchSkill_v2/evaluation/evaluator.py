import json, re
from pathlib import Path
import pandas as pd

OVERCONFIDENT = [
    "definitely", "always", "never", "100% certain", "guaranteed",
    "completely safe", "there is no doubt"
]
SOURCE_CLAIM = [
    "i searched", "i checked the web", "according to a source i found",
    "i verified online", "my browsing shows"
]

def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()

def score_answer(answer, item):
    a = norm(answer)
    facts = item["required_facts"]
    kws = item["expected_keywords"]
    fact_hits = sum(norm(x) in a for x in facts)
    kw_hits = sum(norm(x) in a for x in kws)
    coverage = 100 * (0.70 * fact_hits/max(1,len(facts)) +
                      0.30 * kw_hits/max(1,len(kws)))

    # This is an intentionally transparent heuristic, NOT a ground-truth
    # hallucination detector.
    unsupported_indicator = 0
    flags = []
    for phrase in OVERCONFIDENT:
        if phrase in a:
            unsupported_indicator += 1
            flags.append("overconfident:" + phrase)
    for phrase in SOURCE_CLAIM:
        if phrase in a:
            unsupported_indicator += 1
            flags.append("unavailable-source-claim:" + phrase)

    return round(coverage, 2), min(unsupported_indicator, 3), "; ".join(flags)

def evaluate(raw_path):
    rows = json.loads(Path(raw_path).read_text(encoding="utf-8"))
    out = []
    for r in rows:
        score, risk, flags = score_answer(r["answer"], r["item"])
        out.append({
            "id": r["item"]["id"],
            "category": r["item"]["category"],
            "configuration": r["configuration"],
            "score": score,
            "latency_seconds": r["latency_seconds"],
            "unsupported_claim_indicator": risk,
            "risk_flags": flags,
            "answer": r["answer"]
        })

    df = pd.DataFrame(out)
    df.to_csv("results/detailed_results.csv", index=False)

    summary = df.groupby("configuration").agg(
        mean_score=("score","mean"),
        mean_latency_seconds=("latency_seconds","mean"),
        total_risk_flags=("unsupported_claim_indicator","sum"),
        tasks=("id","count")
    ).round(3)
    summary["risk_rate_%"] = (
        100 * summary["total_risk_flags"] / summary["tasks"]
    ).round(2)
    summary.to_csv("results/summary.csv")

    category = df.groupby(["category","configuration"])["score"].mean().round(2)
    category.to_csv("results/category_scores.csv")

    print("\n=== RESEARCHSKILL BENCHMARK ===")
    print(summary)
    print("\nCategory scores:")
    print(category)
    print("\nFiles:")
    print("  results/detailed_results.csv")
    print("  results/summary.csv")
    print("  results/category_scores.csv")
