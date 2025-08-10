import logging
import requests
from utils.config import OPENROUTER_API_KEY, OPENROUTER_DEFAULT_MODEL

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
FREE_FALLBACK_MODEL = "mistralai/mistral-7b-instruct"  # example free model

class OpenRouterError(Exception):
    pass

def call_openrouter(prompt, model=None, max_tokens=2000, timeout=120):
    """Call OpenRouter chat completion endpoint and return assistant content.

    Raises OpenRouterError on missing API key, and lets requests exceptions propagate
    after logging useful debugging info.
    """
    if not OPENROUTER_API_KEY:
        raise OpenRouterError('OPENROUTER_API_KEY not set. Please configure your environment variables.')

    if model is None:
        model = OPENROUTER_DEFAULT_MODEL

    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    }

    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
    }

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
        if r.status_code == 402:
            logger.warning("Insufficient credits. Falling back to free model: %s", FREE_FALLBACK_MODEL)
            payload['model'] = FREE_FALLBACK_MODEL
            r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)

        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        logger.exception('Network error when calling OpenRouter: %s', e)
        raise

    try:
        return data['choices'][0]['message']['content']
    except Exception:
        logger.debug('Unexpected response shape from OpenRouter: %s', data)
        return data
        
