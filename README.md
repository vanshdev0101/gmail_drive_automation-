Gmail Attachment Automation Framework
 A config-driven Python framework for automating the extraction, classification, and storage of Gmail attachments.
 
 This project is designed as a reusable automation foundation, not a domain-specific script.
 Users define which emails to process, how attachments are classified, and what folder structure is created through configuration files and minimal code changes.
 
 Overview
 This framework automates the following pipeline:
 
 Gmail → Filter Emails → Extract Attachments → Classify → Store → (Optional) Upload to Google Drive
 It is intended for developers and power users who want full control over their email-based document workflows.
 
 Key Features
 Gmail integration using OAuth 2.0
 
 Configurable email filtering (sender-based)
 
 Reliable extraction of all attachments (including nested MIME parts)
 
 Rule-based attachment classification using YAML
 
 Fully customizable folder structure
 
 Optional Google Drive upload
 
 Idempotent processing using Gmail labels
 
 Modular, extensible architecture
 
 Intended Audience
 This project is suitable for users who are comfortable with:
 
 Python
 
 Configuration files (YAML)
 
 OAuth-based APIs
 
 It is not intended as a no-code or GUI-based tool.
 
 Example Use Cases
 Accounting document automation (Invoices, GRNs, POs, Debit Notes)
 
 Resume or application intake
 
 Assignment or report collection
 
 Client document ingestion
 
 Legal or compliance archiving
 
 Personal Gmail organization
 
 Project Structure
 app/
  ├── main.py                # Application entry point
  ├── gmail_reader.py        # Gmail message retrieval
  ├── attachment_handler.py # Attachment extraction & processing
  ├── classifier.py          # Rule-based classification logic
  ├── folder_manager.py      # Folder structure definition
  ├── drive_uploader.py      # Optional Google Drive upload
  ├── gmail_labeler.py       # Gmail labeling logic
  ├── auth.py                # Shared OAuth scopes
  └── logger.py              # Logging configuration
 
 config/
  ├── settings.example.yaml  # Email filtering & processing settings
  ├── rules.example.yaml     # Document classification rules
  └── branches.example.yaml  # Optional grouping logic
 Authentication
 The framework uses OAuth 2.0 with a single token containing combined scopes:
 
 Gmail read/modify access
 
 Google Drive file upload access (optional)
 
 Required APIs
 Gmail API
 
 Google Drive API
 
 Required OAuth Client Type
 Desktop Application
 
 Users must provide their own credentials.json.
 OAuth tokens are generated automatically on first run.
 
 Installation
 1. Clone the repository
 git clone <repository-url>
 cd gmail-attachment-automation
 2. Install dependencies
 pip install -r requirements.txt
 3. Add OAuth credentials
 Place your OAuth client file in the project root:
 
 credentials.json
 Do not commit this file.
 
 Configuration
 This framework is configuration-first.
 Most users will not need to modify Python code.
 
 Email Selection
 Copy and edit:
 
 config/settings.example.yaml → config/settings.yaml
 Example:
 
 gmail:
   allowed_senders:
     - example@gmail.com
     - sender@domain.com
 
 processing:
   gmail_label_processed: "Processed"
 Attachment Classification
 Copy and edit:
 
 config/rules.example.yaml → config/rules.yaml
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
 Folder Structure
 Folder hierarchy is defined in:
 
 folder_manager.py
 Users may implement any structure they require, for example:
 
 By sender
 
 By document type
 
 By date (year/month)
 
 By project or client
 
 This design is intentionally flexible.
 
 Running the Application
 python -m app.main
 On first run:
 
 A browser window will open
 
 Google will request Gmail (and Drive, if enabled) permissions
 
 An OAuth token will be generated automatically
 
 Processing Logic
 For each eligible email:
 
 Retrieve email
 
 Extract all attachments
 
 Classify attachments using rules
 
 Build folder path
 
 Save files locally
 
 Upload to Google Drive (if enabled)
 
 Mark email as processed
 
 Emails are processed only once.
 
 Customization Guidelines
 To adapt this framework for a new workflow:
 
 Update email filters (settings.yaml)
 
 Define classification rules (rules.yaml)
 
 Adjust folder structure logic (folder_manager.py)
 
 Enable or disable Drive upload as needed
 
 Core Gmail and OAuth logic should remain unchanged.
 
 Security Notes
 Never commit credentials.json or token.json
 
 OAuth permissions are limited to required scopes
 
 Google Drive access is restricted to files created by the app
 
 Versioning
 Current Status: v1 (Stable)
 v1 indicates:
 
 Core pipeline is complete
 
 Authentication flow is correct
 
 Configuration model is stable
 
 No interactive CLI setup is included by design
 
 Future versions may introduce optional helpers if real usage demand exists.
 
 License
 MIT License (or as applicable)
 
 Final Notes
 This project is intentionally designed as a framework, not a finished product.
 
 If you can define your workflow in terms of:
 
 “Which emails, which attachments, which structure”
 
 This framework can automate it with minimal effort.
 
 If you want, I can also:
 
 review the final public repo before you push
 
 help you extract a clean template from your private version
 
 write a short “Quick Start” for developers
 
 Just tell me.
 
 