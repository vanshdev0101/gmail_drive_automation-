from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import yaml
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def _load_settings():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def _get_gmail_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("gmail", "v1", credentials=creds)

def label_as_processed(message_id):
    settings = _load_settings()
    label_name = settings["processing"]["gmail_label_processed"]

    service = _get_gmail_service()

    labels = service.users().labels().list(userId="me").execute()["labels"]
    label_map = {l["name"]: l["id"] for l in labels}

    if label_name not in label_map:
        label = service.users().labels().create(
            userId="me",
            body={
                "name": label_name,
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show"
            }
        ).execute()
        label_id = label["id"]
    else:
        label_id = label_map[label_name]

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"addLabelIds": [label_id]}
    ).execute()
