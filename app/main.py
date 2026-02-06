from app.gmail_reader import fetch_target_emails
from app.attachment_handler import download_attachments
from app.folder_manager import ensure_structure
from app.gmail_labeler import label_as_processed
from app.logger import get_app_logger

logger = get_app_logger()

def main():
    ensure_structure()

    emails = fetch_target_emails()
    logger.info(f"Found {len(emails)} emails to process")

    total_files = 0

    for msg_id in emails:
        saved_files = download_attachments(msg_id)

        if len(saved_files) > 0:
            label_as_processed(msg_id)
            total_files += len(saved_files)
            logger.info(f"Email processed | email={msg_id}")
        else:
            logger.warning(f"Email skipped (no valid attachments) | email={msg_id}")

    logger.info(f"TOTAL FILES DOWNLOADED: {total_files}")

if __name__ == "__main__":
    main()
