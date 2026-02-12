from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.auth import SCOPES
import yaml
import os

 

def _load_settings():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def _get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def fetch_target_emails():
    settings = _load_settings()
    allowed_senders = settings["gmail"]["allowed_senders"]
    processed_label = settings["processing"]["gmail_label_processed"]

    service = _get_gmail_service()
    message_ids = []

    for sender in allowed_senders:
        query = f"from:{sender} has:attachment -label:{processed_label}"

        page_token = None

        while True:
            response = service.users().messages().list(
                userId="me",
                q=query,
                pageToken=page_token
            ).execute()

            messages = response.get("messages", [])
            for msg in messages:
                message_ids.append(msg["id"])

            page_token = response.get("nextPageToken")
            if not page_token:
                break

    return message_ids

