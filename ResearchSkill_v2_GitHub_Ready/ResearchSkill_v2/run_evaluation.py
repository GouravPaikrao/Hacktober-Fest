import argparse, json, time
from pathlib import Path
from agent import ask_ollama, baseline_prompt, skill_prompt, v1_prompt, v2_prompt
from evaluation.evaluator import evaluate

ROOT = Path(__file__).parent

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="qwen2.5:3b")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--mode", choices=["baseline","skill","v1","v2","all"], default="all")
    args = p.parse_args()

    data = json.loads((ROOT/"data/eval_set.json").read_text())
    if args.limit:
        data = data[:args.limit]

    skill_text = (ROOT/"skill/SKILL.md").read_text()
    v1_text = (ROOT/"skill/V1.md").read_text()
    v2_text = (ROOT/"skill/V2.md").read_text()

    prompts = {
        "baseline": lambda q: baseline_prompt(q),
        "skill": lambda q: skill_prompt(q, skill_text),
        "v1": lambda q: v1_prompt(q, v1_text),
        "v2": lambda q: v2_prompt(q, v2_text),
    }
    modes = list(prompts) if args.mode == "all" else [args.mode]
    results = []

    for config in modes:
        print(f"\n=== {config.upper()} ===")
        for item in data:
            start = time.perf_counter()
            answer = ask_ollama(args.model, prompts[config](item["question"]))
            latency = time.perf_counter() - start
            results.append({
                "configuration": config,
                "item": item,
                "answer": answer,
                "latency_seconds": round(latency, 3)
            })
            print(f"Task {item['id']:02d} | {latency:6.2f}s")

    raw = ROOT/"results/raw_results.json"
    raw.write_text(json.dumps(results, indent=2), encoding="utf-8")
    evaluate(raw)

if __name__ == "__main__":
    main()
