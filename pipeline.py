import os
import asyncio
from ai_client import call_openrouter
from mods.lib_patcher import mod_file
from file_tools import write_text_file
from utils.config import TEMP_DIR

async def handle_pipeline(temp_path, filename=None, user_instructions=None, mode='file'):
    """Orchestrates processing:
    - mode='file': process uploaded file via mod_file
    - mode='code': call AI to generate code text
    Returns file path or text.
    """
    if mode == 'code':
        prompt = f"Write complete working code for the following request:\n{user_instructions}\nReturn only the code."
        response = call_openrouter(prompt)
        # response is text code
        # save to temp file and return path
        out_path = os.path.join(TEMP_DIR, 'generated_code.py')
        write_text_file(out_path, response)
        return out_path

    # file mode
    # if no temp_path, nothing to do
    if not temp_path:
        return None

    # decide instruction: caption or user_instructions
    instr = user_instructions or 'Recode or optimize this file as needed.'
    # For large binary files, mod_file should implement streaming/patching
    processed = mod_file(temp_path, instr)
    return processed
