import os
import requests
from utils.config import OPENROUTER_API_KEY, OPENROUTER_DEFAULT_MODEL

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_openrouter(prompt, model=None, max_tokens=2000):
    if model is None:
        model = OPENROUTER_DEFAULT_MODEL

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }

    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=120)
    r.raise_for_status()

    data = r.json()
    try:
        return data['choices'][0]['message']['content']
    except (KeyError, IndexError):
        return data
        
