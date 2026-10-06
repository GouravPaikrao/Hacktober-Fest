from pathlib import Path
from agent import ask_ollama, baseline_prompt, skill_prompt, v1_prompt, v2_prompt

MODEL = "qwen2.5:3b"
texts = {
    "skill": Path("skill/SKILL.md").read_text(),
    "v1": Path("skill/V1.md").read_text(),
    "v2": Path("skill/V2.md").read_text(),
}
print("ResearchSkill interactive demo")
print("Type exit to quit.\n")
while True:
    q = input("Question: ").strip()
    if q.lower() == "exit":
        break
    print("\n--- BASELINE ---")
    print(ask_ollama(MODEL, baseline_prompt(q)))
    print("\n--- SKILL V1 ---")
    print(ask_ollama(MODEL, v1_prompt(q, texts["v1"])))
    print("\n--- SKILL V2 ---")
    print(ask_ollama(MODEL, v2_prompt(q, texts["v2"])))
    print()
