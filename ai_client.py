import os
import requests
import logging
from utils.config import OPENROUTER_API_KEY, OPENROUTER_DEFAULT_MODEL

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class OpenRouterError(Exception):
    pass

def call_openrouter(prompt, model=None, max_tokens=2000, timeout=120):
    if not OPENROUTER_API_KEY:
        raise OpenRouterError('OPENROUTER_API_KEY is not set. Please set it in environment variables.')

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

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
        # Provide more detailed info on 4xx/5xx errors
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # include response body when available for debugging (avoid leaking secrets)
            text = ''
            try:
                text = r.text
            except Exception:
                pass
            logger.error('OpenRouter HTTP error %s: %s', r.status_code, text[:1000])
            raise

        data = r.json()
    except requests.exceptions.RequestException as e:
        logger.exception('Network error when calling OpenRouter: %s', e)
        raise

    # normalize response
    try:
        return data['choices'][0]['message']['content']
    except Exception:
        # fallback: return full payload for debugging
        logger.debug('Unexpected OpenRouter response shape: %s', data)
        return data
