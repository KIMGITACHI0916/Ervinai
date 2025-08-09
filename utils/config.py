import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_DEFAULT_MODEL = 'openai/gpt-3.5-turbo'
MAX_FILE_MB = int(os.getenv('MAX_FILE_MB', '500'))
TEMP_DIR = os.getenv('TEMP_DIR', '/tmp')
