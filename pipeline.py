import logging
from ai_client import call_openrouter

logger = logging.getLogger(__name__)

async def handle_pipeline(file_content, filename=None, user_instructions=None, mode=None):
    """
    Handles the pipeline for processing requests.
    :param file_content: optional file data
    :param filename: name of uploaded file
    :param user_instructions: instructions from the user
    :param mode: processing mode
    :return: processed output
    """
    prompt = ""

    if user_instructions:
        prompt += f"User instructions:\n{user_instructions}\n\n"

    if filename:
        prompt += f"Filename: {filename}\n\n"

    if file_content:
        prompt += f"File content:\n{file_content}\n\n"

    logger.info("Generated prompt for model")

    try:
        response = call_openrouter(prompt)
    except Exception as e:
        logger.exception("Error calling OpenRouter API")
        raise

    return response
