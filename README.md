Gmail Attachment Automation Framework (v1)

A config-driven Python framework to automatically fetch emails from Gmail, extract attachments, classify them, and store or upload them in any folder structure you define.

This project is intentionally built for developers / power users, not end-users.
All behavior is controlled through configuration files and small, readable code changes.

🎯 What this project does

At a high level, the system performs:

Gmail → Filter → Extract → Classify → Store → (Optional) Upload to Drive


Specifically, it:

Connects to Gmail using OAuth

Filters emails based on user-defined rules

Extracts all attachments (including nested MIME attachments)

Classifies attachments using YAML rules

Builds a custom folder structure

Saves files locally

Optionally uploads files to Google Drive

Marks processed emails as read + labeled

Ensures emails are not processed twice

🧠 Who this is for

This framework is designed for:

Developers

Automation engineers

Power users comfortable with config files

Anyone who wants full control, not a black-box tool

It is not intended for non-technical users.

🧩 Example use cases

Accounting documents (Invoices, GRNs, POs, Debit Notes)

HR resume intake

Assignment collection (college / training)

Client report ingestion

Legal or compliance archiving

Personal Gmail organization

If the workflow is email → attachment → folder, this framework fits.

🏗️ Project architecture
app/
 ├── main.py                # Entry point / orchestration
 ├── gmail_reader.py        # Fetch target emails
 ├── attachment_handler.py # Extract & process attachments
 ├── classifier.py          # Rule-based classification
 ├── folder_manager.py      # Folder structure logic
 ├── drive_uploader.py      # Google Drive upload
 ├── gmail_labeler.py       # Mark emails as processed
 ├── auth.py                # Shared OAuth scopes
 └── logger.py              # Logging setup

config/
 ├── rules.yaml             # Document classification rules
 ├── branches.yaml          # Logical grouping rules (optional)
 └── settings.yaml          # Gmail filters & labels

🔐 Authentication model

The system uses one OAuth token with combined scopes:

https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/drive.file


credentials.json is provided by the user

token.json is generated automatically on first run

Tokens are reused across runs

⚙️ Installation & setup
1️⃣ Clone the repository
git clone <repo-url>
cd gmail_drive_automation

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add Google credentials

Place your OAuth credentials file in the project root:

credentials.json


⚠️ Never commit this file.

4️⃣ Enable APIs in Google Cloud

In the same Google Cloud project:

Enable Gmail API

Enable Google Drive API

OAuth client type must be Desktop App

5️⃣ Configure email selection

Edit:

config/settings.yaml


Example:

gmail:
  allowed_senders:
    - example@company.com
    - reports@service.com

processing:
  gmail_label_processed: "Processed"


This defines which emails are considered.

6️⃣ Define classification rules

Edit:

config/rules.yaml


Example:

document_types:
  invoice:
    folder: "Invoices"
    filename_patterns:
      - "INVOICE"
      - "^INV"

  resume:
    folder: "Resumes"
    filename_patterns:
      - "CV"
      - "RESUME"


No code changes needed to add new document types.

7️⃣ Define your folder structure

Edit:

folder_manager.py


This file decides how folders are built.

Examples you can implement:

By sender

By document type

By date (year/month)

By project name

Any custom hierarchy

This is intentionally left flexible.

8️⃣ Run the automation
python -m app.main


On first run:

Browser opens

Google asks for Gmail + Drive permissions

Token is created automatically

🔄 Processing flow (v1)

For each eligible email:

Fetch email

Extract all attachments

Classify using rules

Build folder path

Save file locally

Upload to Google Drive (if enabled)

Mark email as read + labeled

Emails are processed exactly once.

🔧 Customizing for your own workflow

You typically only need to change:

config/settings.yaml → which emails

config/rules.yaml → how files are classified

folder_manager.py → folder structure

Core Gmail / Drive logic stays untouched.

🛑 What this project does NOT assume

No fixed document types

No fixed folder names

No business-specific logic

No UI / CLI wizard

No opinionated structure

Everything is user-defined.

🧪 Debugging tips

If Drive upload fails → delete token.json and re-auth

If classification fails → check YAML patterns

If emails repeat → check processed label

Logs provide full trace per run

🔒 Security notes

Never commit credentials.json or token.json

OAuth permissions are limited to required scopes

Drive access is file-level, not full Drive access