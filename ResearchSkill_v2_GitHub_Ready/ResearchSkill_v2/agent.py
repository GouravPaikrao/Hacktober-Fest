import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(model: str, prompt: str, temperature: float = 0.2):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    data = r.json()
    return data.get("response", "").strip()

def baseline_prompt(question):
    return f"""Answer the question clearly and accurately.
Do not invent facts or claim to have checked sources.

Question:
{question}
"""

def skill_prompt(question, skill_text):
    return f"""You are an open-weight AI research agent.

Use the following Agent Skill:
{skill_text}

Question:
{question}

Follow the skill workflow. Give a concise answer. Do not invent evidence,
sources, statistics, or external verification. If something cannot be verified
from the information available to you, say so explicitly.
"""

def v1_prompt(question, skill_text):
    return f"""Use this Agent Skill V1:
{skill_text}

Answer the question directly, identify its main claims, and check for unsupported
claims before responding.

Question:
{question}
"""

def v2_prompt(question, skill_text):
    return f"""Use this Agent Skill V2:
{skill_text}

Classify the task, break it into claims if needed, distinguish evidence from
inference, calibrate uncertainty, answer directly, and perform a final
hallucination-risk check. Never invent a source or claim external verification.

Question:
{question}
"""
