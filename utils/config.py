import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENROUTER_API_KEY = os.getenv('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')
OPENROUTER_DEFAULT_MODEL = 'openai/gpt-3.5-turbo'
MAX_FILE_MB = int(os.getenv('MAX_FILE_MB', '500'))
TEMP_DIR = os.getenv('TEMP_DIR', '/tmp')
