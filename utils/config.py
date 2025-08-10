import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load .env for local dev; in production (Railway) use project env vars.
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
GDRIVE_SERVICE_ACCOUNT_JSON = os.getenv('GDRIVE_SERVICE_ACCOUNT_JSON')  # This is the JSON string
GDRIVE_FOLDER_ID = os.getenv('GDRIVE_FOLDER_ID')
OPENROUTER_DEFAULT_MODEL = os.getenv('OPENROUTER_DEFAULT_MODEL', 'deepseek/deepseek-chat-v3-0324:free')
MAX_FILE_MB = int(os.getenv('MAX_FILE_MB', '500'))
TEMP_DIR = os.getenv('TEMP_DIR', '/tmp')

def validate_config(logger=None):
    missing = []
    if not BOT_TOKEN:
        missing.append('BOT_TOKEN')
    if not OPENROUTER_API_KEY:
        missing.append('OPENROUTER_API_KEY')
    if not GDRIVE_SERVICE_ACCOUNT_JSON:
        missing.append('GDRIVE_SERVICE_ACCOUNT_JSON')
    if not GDRIVE_FOLDER_ID:
        missing.append('GDRIVE_FOLDER_ID')

    if missing:
        msg = f"Missing required environment variables: {', '.join(missing)}"
        if logger:
            logger.error(msg)
        else:
            print('ERROR:', msg)
        return False

    if not (OPENROUTER_API_KEY.startswith('sk-') or OPENROUTER_API_KEY.startswith('sk-or-')):
        note = 'OPENROUTER_API_KEY does not appear to begin with expected prefix (sk- or sk-or-).'
        if logger:
            logger.warning(note)
        else:
            print('WARNING:', note)

    return True

def get_drive_service():
    """Create and return a Google Drive service object using service account JSON from env."""
    service_account_info = json.loads(GDRIVE_SERVICE_ACCOUNT_JSON)
    creds = service_account.Credentials.from_service_account_info(service_account_info)
    return build('drive', 'v3', credentials=creds)
    
