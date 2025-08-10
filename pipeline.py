import os
import logging
from ai_client import call_openrouter, OpenRouterError
from utils.config import MAX_FILE_MB, TEMP_DIR, OPENROUTER_API_KEY

logger = logging.getLogger(__name__)

async def handle_pipeline(file_path=None, filename=None, user_instructions=None, mode='code'):
    """Process requests; supports 'code' mode (AI generates text) and 'file' mode (process uploaded file)."""
    # Early check for API key
    if not OPENROUTER_API_KEY:
        raise OpenRouterError('OPENROUTER_API_KEY is not set. Please configure your environment variables.')

    prompt_parts = []
    if user_instructions:
        prompt_parts.append(f"User instructions:\n{user_instructions}\n")

    if filename:
        prompt_parts.append(f"Filename: {filename}\n")

    if file_path and os.path.exists(file_path):
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > MAX_FILE_MB:
            raise ValueError(f"Uploaded file size {size_mb:.2f}MB exceeds limit of {MAX_FILE_MB}MB")
        # Optionally include small file contents in prompt
        if size_mb < 1:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
                prompt_parts.append('\nFile content:\n' + fh.read())

    prompt = "\n".join(prompt_parts).strip()
    logger.info('Generated prompt for model')

    try:
        response = call_openrouter(prompt)
    except Exception as e:
        logger.exception('Error calling OpenRouter API: %s', e)
        raise

    return response
