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
    processed_emails = 0

    for msg_id in emails:
        try:
            saved_files = download_attachments(msg_id)

            if saved_files:
                label_as_processed(msg_id)
                processed_emails += 1
                total_files += len(saved_files)
                logger.info(
                    f"Email processed | email={msg_id} | files={len(saved_files)}"
                )
            else:
                logger.warning(
                    f"Email skipped (no valid attachments) | email={msg_id}"
                )

        except Exception as e:
            logger.error(
                f"Failed processing email | email={msg_id} | error={e}"
            )

    logger.info(
        f"RUN SUMMARY | emails_processed={processed_emails} | files_uploaded={total_files}"
    )

if __name__ == "__main__":
    main()
