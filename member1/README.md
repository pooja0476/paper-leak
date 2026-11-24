# Member 1 – Telegram Monitoring & Evidence Collection

## Overview
This module monitors configured Telegram channels and collects messages and shared files that may contain leaked examination papers or related information.

## Features
- Telegram authentication using Telethon.
- Monitors configured public channels and accessible private channels.
- Collects existing messages when monitoring starts.
- Continuously listens for newly received messages.
- Downloads image and PDF attachments.
- Stores message details and evidence metadata in an SQLite database.
- Calculates SHA-256 hashes for downloaded files.
- Verifies evidence file integrity by comparing stored and recalculated hashes.
- Generates a CSV integrity verification report.

## Technologies Used
- Python
- Telethon
- SQLite
- Python-dotenv
- SHA-256 hashing
- CSV

## Project Structure
```text
member1/
├── .env
├── channels.txt
├── README.md
├── data/
│   ├── evidence.db
│   ├── evidence/
│   └── evidence_integrity_report.csv
├── database/
│   └── evidence_db.py
└── src/
    ├── telegram_monitor.py
    └── verify_evidence.py
```

## How to Run

1. Install the required dependencies.
2. Configure Telegram API credentials in `member1/.env`.
3. Add channel usernames or accessible private channel names to `member1/channels.txt`.
4. Start the monitor from the project root:

```bash
python member1/src/telegram_monitor.py
```

5. Stop monitoring using `Ctrl + C`.

## Evidence Integrity Verification

Run:

```bash
python member1/src/verify_evidence.py
```

The script checks downloaded evidence files against their stored SHA-256 hashes and generates:

`member1/data/evidence_integrity_report.csv`

## Testing Performed
- Telegram authentication and connection: Successful.
- Configured channel access: Successful.
- Existing message collection: Successful.
- Real-time new message detection: Successful.
- PDF download: Successful.
- SHA-256 hash generation: Successful.
- Evidence integrity verification: 9 files verified, 0 failures in the recorded test.
- Continuous monitoring startup: Successful.

## Security
- Telegram API credentials are stored in `.env`.
- Session files, databases, and downloaded evidence are excluded from Git.
- Evidence files are verified using SHA-256 hashes.

## Responsibility
Member 1 is responsible for Telegram monitoring, message collection, media downloading, evidence storage, and evidence integrity verification.

**Note:** SHA-256 verification confirms that a downloaded file has not changed since its recorded hash was stored. It does not independently establish the authenticity of the original Telegram content.