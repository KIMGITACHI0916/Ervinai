import os
from dotenv import load_dotenv

# Load .env for local dev; in production (Railway) use project env vars.
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_DEFAULT_MODEL = os.getenv('OPENROUTER_DEFAULT_MODEL', 'deepseek/deepseek-chat-v3-0324:free')
MAX_FILE_MB = int(os.getenv('MAX_FILE_MB', '500'))
TEMP_DIR = os.getenv('TEMP_DIR', '/tmp')

def validate_config(logger=None):
    missing = []
    if not BOT_TOKEN:
        missing.append('BOT_TOKEN')
    if not OPENROUTER_API_KEY:
        missing.append('OPENROUTER_API_KEY')
    if missing:
        msg = f"Missing required environment variables: {', '.join(missing)}"
        if logger:
            logger.error(msg)
        else:
            print('ERROR:', msg)
        return False
    # basic key format check
    if not (OPENROUTER_API_KEY.startswith('sk-') or OPENROUTER_API_KEY.startswith('sk-or-')):
        note = 'OPENROUTER_API_KEY does not appear to begin with expected prefix (sk- or sk-or-).'
        if logger:
            logger.warning(note)
        else:
            print('WARNING:', note)
    return True
