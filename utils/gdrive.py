import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Create Google Drive service from JSON in environment variable
def get_gdrive_service():
    gdrive_json = os.getenv("GDRIVE_SERVICE_ACCOUNT_JSON")
    if not gdrive_json:
        raise ValueError("GDRIVE_SERVICE_ACCOUNT_JSON environment variable is missing.")
    
    try:
        service_account_info = json.loads(gdrive_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in GDRIVE_SERVICE_ACCOUNT_JSON: {e}")

    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

# Download a file from Google Drive
def download_from_gdrive(file_id_or_url, dest_path):
    # Extract file ID from URL or use directly
    file_id = file_id_or_url
    if "drive.google.com" in file_id_or_url:
        if "/d/" in file_id_or_url:
            file_id = file_id_or_url.split("/d/")[1].split("/")[0]
        elif "id=" in file_id_or_url:
            file_id = file_id_or_url.split("id=")[1].split("&")[0]

    service = get_gdrive_service()
    request = service.files().get_media(fileId=file_id)
    
    with io.FileIO(dest_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download progress: {int(status.progress() * 100)}%")

    return dest_path
    
