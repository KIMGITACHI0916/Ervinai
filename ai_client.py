import os
import requests
from utils.config import OPENROUTER_API_KEY

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_openrouter(prompt, model="nousresearch/nous-hermes-2-mistral-7b-dpo", max_tokens=2000):
    header = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }
    r = requests.post(OPENROUTER_URL, headers=header, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    # adapt for provider schema
    # expected: data['choices'][0]['message']['content']
    try:
        return data['choices'][0]['message']['content']
    except Exception:
        return data
