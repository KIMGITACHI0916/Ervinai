import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import GDRIVE_SERVICE_ACCOUNT_JSON, GDRIVE_FOLDER_ID

def upload_to_gdrive(file_path, filename=None):
    if not filename:
        filename = os.path.basename(file_path)

    creds = service_account.Credentials.from_service_account_file(
        GDRIVE_SERVICE_ACCOUNT_JSON,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": filename}
    if GDRIVE_FOLDER_ID:
        file_metadata["parents"] = [GDRIVE_FOLDER_ID]

    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    return uploaded_file.get("id")
    
