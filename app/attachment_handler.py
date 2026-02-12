import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from app.classifier import detect_branch, detect_doc_type
from app.folder_manager import get_target_folder
from app.logger import get_app_logger
from app.auth import SCOPES

 

logger = get_app_logger()


def _walk_parts(parts):
    for part in parts:
        if part.get("parts"):
            yield from _walk_parts(part["parts"])
        else:
            yield part

def _get_gmail_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("gmail", "v1", credentials=creds)


def download_attachments(message_id):
    service = _get_gmail_service()

    message = service.users().messages().get(
        userId="me",
        id=message_id
    ).execute()

    payload = message.get("payload", {})
    parts = payload.get("parts", [])
    headers = payload.get("headers", [])

    subject = ""
    for h in headers:
        if h["name"].lower() == "subject":
            subject = h["value"]
            break

    saved = []

    for part in _walk_parts(parts):
        filename = part.get("filename")
        attachment_id = part.get("body", {}).get("attachmentId")

        if not attachment_id:
            continue

        if not filename:
            filename = f"{message_id}.pdf"

        branch = detect_branch(subject + " " + filename)
        doc_type = detect_doc_type(subject + " " + filename)

        if not branch or not doc_type:
            logger.warning(f"Unclassified file skipped | {filename}")
            continue

        target_dir = get_target_folder(branch, doc_type)

        attachment = service.users().messages().attachments().get(
            userId="me",
            messageId=message_id,
            id=attachment_id
        ).execute()

        data = base64.urlsafe_b64decode(attachment["data"])

        safe_name = f"{message_id}_{filename}"
        file_path = target_dir / safe_name

        with open(file_path, "wb") as f:
            f.write(data)

        from app.drive_uploader import get_or_create_folder, upload_file

        drive_root = get_or_create_folder("Sarvana")
        branch_folder = get_or_create_folder(branch, drive_root)
        doc_folder = get_or_create_folder(doc_type.upper(), branch_folder)

        upload_file(file_path, doc_folder)

        saved.append(str(file_path))
        logger.info(f"Saved & uploaded | {file_path}")

    return saved

