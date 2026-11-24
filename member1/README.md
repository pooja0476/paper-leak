# Member 1 – Telegram Monitoring & Evidence Collection

## Overview
This module collects messages and media from configured public Telegram channels for the Paper-Leak Sentinel project. It stores evidence metadata and supports file-integrity verification.

## Features
- Telegram API integration using Telethon.
- Monitoring of configured Telegram channels.
- Initial collection of recent messages.
- Continuous monitoring for new messages.
- Image and PDF attachment collection.
- SHA-256 hash generation for downloaded media.
- SQLite database for evidence metadata.
- Evidence integrity verification.
- CSV report generation.

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

## Technologies Used
- Python
- Telethon
- SQLite
- SHA-256
- CSV
- python-dotenv

## Setup
1. Install the project dependencies:
   `pip install telethon python-dotenv`
2. Configure Telegram API credentials in `member1/.env`:
   - `API_ID`
   - `API_HASH`
3. Add authorized public Telegram channel usernames to `channels.txt`, one per line.

## Run Telegram Monitoring
From the project root:

```bash
python member1/src/telegram_monitor.py
```

## Verify Evidence Integrity
Run:

```bash
python member1/src/verify_evidence.py
```

The utility compares the stored SHA-256 hashes with the hashes recalculated from downloaded files.

## Output
- Downloaded media files in `data/evidence/`.
- Evidence metadata in `data/evidence.db`.
- Integrity verification results in `data/evidence_integrity_report.csv`.

## Security
- Keep `.env` and Telegram session files private.
- Never upload API credentials or session files to GitHub.
- Use only public channels or channels you are authorized to monitor.
- Treat collected posts as unverified evidence until independently validated.

## Module Responsibility
Member 1 is responsible for Telegram monitoring, evidence collection, media downloading, hash generation, database storage, and evidence integrity reporting.
