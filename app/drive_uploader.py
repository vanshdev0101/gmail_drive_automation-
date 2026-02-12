from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from app.auth import SCOPES



def _get_drive_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("drive", "v3", credentials=creds)

def get_or_create_folder(name, parent_id=None):
    service = _get_drive_service()

    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    if files:
        return files[0]["id"]

    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder"
    }

    if parent_id:
        metadata["parents"] = [parent_id]

    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]

def upload_file(file_path, parent_folder_id):
    service = _get_drive_service()

    media = MediaFileUpload(file_path, resumable=True)

    metadata = {
        "name": file_path.name,
        "parents": [parent_folder_id]
    }

    service.files().create(
        body=metadata,
        media_body=media,
        fields="id"
    ).execute()
