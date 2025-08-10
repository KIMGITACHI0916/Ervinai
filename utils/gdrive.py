import os
import re
import tempfile
import logging

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

logger = logging.getLogger(__name__)

def download_from_gdrive(url_or_id: str) -> str:
    """
    Download a file from Google Drive given a share link or file ID.
    Returns the local path to the downloaded file.
    """
    # Extract file ID from various link formats
    file_id_match = re.search(r"[-\w]{25,}", url_or_id)
    if not file_id_match:
        raise ValueError("Could not parse Google Drive file ID from input.")
    file_id = file_id_match.group(0)

    logger.info(f"Downloading from Google Drive, file ID: {file_id}")

    # Authenticate with Google Drive (assumes client_secrets.json in project root)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # Download file to temp path
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    file_obj = drive.CreateFile({'id': file_id})
    file_obj.GetContentFile(temp_file.name)

    logger.info(f"Downloaded Google Drive file to {temp_file.name}")
    return temp_file.name
  
