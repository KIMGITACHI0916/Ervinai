import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from utils.config import GDRIVE_SERVICE_ACCOUNT_JSON, GDRIVE_FOLDER_ID


def get_gdrive_service():
    """Authenticate and return a Google Drive service instance."""
    creds = service_account.Credentials.from_service_account_file(
        GDRIVE_SERVICE_ACCOUNT_JSON,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)


def upload_to_gdrive(file_path, filename=None):
    """Uploads a file to Google Drive. Returns file ID."""
    if not filename:
        filename = os.path.basename(file_path)

    service = get_gdrive_service()

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


def download_from_gdrive(file_id, destination_path):
    """Downloads a file from Google Drive using its file ID."""
    service = get_gdrive_service()

    request = service.files().get_media(fileId=file_id)
    with open(destination_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download {int(status.progress() * 100)}% complete.")

    return destination_path
    
