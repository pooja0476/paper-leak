
import sqlite3
import hashlib
import json
from pathlib import Path
from datetime import datetime

# Reuse Member 2's existing OCR functions
from integrated_workflow import (
    extract_text,
    extract_questions_from_text,
    compare_questions
)

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent

MEMBER1_DIR = PROJECT_DIR / "member1"

DB_PATH = MEMBER1_DIR / "data" / "evidence.db"

REFERENCE_FILE = PROJECT_DIR / "sample.pdf"

RESULTS_FILE = PROJECT_DIR / "telegram_ocr_results.json"

ALERTS_FILE = PROJECT_DIR / "telegram_ocr_alerts.json"


# Calculate SHA-256
def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# Main integration
def run_telegram_ocr():

    print("\n===================================")
    print("PAPER-LEAK SENTINEL")
    print("TELEGRAM + OCR INTEGRATION")
    print("===================================")

    # Check reference paper
    if not REFERENCE_FILE.is_file():
        print("Reference paper not found:", REFERENCE_FILE)
        return

    # Extract reference questions
    print("\nLoading reference question paper...")

    reference_text = extract_text(str(REFERENCE_FILE))

    reference_questions = extract_questions_from_text(
        reference_text
    )

    if not reference_questions:
        print("No questions found in reference paper.")
        return

    print("Reference questions found:", len(reference_questions))

    # Connect to Telegram evidence database
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            evidence_id,
            channel_name,
            message_id,
            message_link,
            media_path,
            media_type,
            sha256_hash
        FROM evidence
        WHERE media_path IS NOT NULL
    """)

    evidence_records = cursor.fetchall()
    connection.close()

    print("Telegram evidence records found:", len(evidence_records))

    all_results = []
    all_alerts = []

    processed = 0
    skipped = 0

    # Process each Telegram attachment
    for record in evidence_records:

        evidence_id = record["evidence_id"]

        media_path = record["media_path"]

        print("\n-----------------------------------")
        print("Processing:", evidence_id)

        file_path = MEMBER1_DIR / media_path

        # Check file existence
        if not file_path.is_file():
            print("File missing. Skipping.")
            skipped += 1
            continue

        # Check supported formats
        if file_path.suffix.lower() not in [
            ".pdf", ".png", ".jpg", ".jpeg"
        ]:
            print("Unsupported format. Skipping.")
            skipped += 1
            continue

        # Verify evidence integrity
        stored_hash = record["sha256_hash"]

        if not stored_hash:
            print("No stored SHA-256 hash. Skipping.")
            skipped += 1
            continue

        current_hash = calculate_sha256(file_path)

        if current_hash != stored_hash:
            print("WARNING: Evidence integrity check failed!")
            skipped += 1
            continue

        print("SHA-256 verification successful.")

        try:
            # Extract text using Member 2's OCR
            suspicious_text = extract_text(str(file_path))

            if not suspicious_text.strip():
                print("No readable text found. Skipping.")
                skipped += 1
                continue

            # Extract individual questions
            suspicious_questions = extract_questions_from_text(
                suspicious_text
            )

            if not suspicious_questions:
                print("No questions detected. Skipping.")
                skipped += 1
                continue

            print(
                "Suspicious questions found:",
                len(suspicious_questions)
            )

            # Compare with reference paper
            results, alerts = compare_questions(
                reference_questions,
                suspicious_questions,
                str(REFERENCE_FILE.name),
                evidence_id
            )

            # Attach Telegram evidence information
            for result in results:
                result["Evidence ID"] = evidence_id
                result["Telegram Channel"] = record["channel_name"]
                result["Telegram Message ID"] = record["message_id"]
                result["Telegram Message Link"] = record["message_link"]
                result["Evidence SHA-256"] = stored_hash

            for alert in alerts:
                alert["Evidence ID"] = evidence_id
                alert["Telegram Channel"] = record["channel_name"]
                alert["Telegram Message ID"] = record["message_id"]
                alert["Telegram Message Link"] = record["message_link"]
                alert["Evidence SHA-256"] = stored_hash

            all_results.extend(results)
            all_alerts.extend(alerts)

            processed += 1

            print("Comparison completed.")
            print("Possible matches:", len(alerts))

        except Exception as error:
            print("Processing error:", error)
            skipped += 1

    # Save results
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(all_results, file, indent=4, ensure_ascii=False)

    with open(ALERTS_FILE, "w", encoding="utf-8") as file:
        json.dump(all_alerts, file, indent=4, ensure_ascii=False)

    # Final summary
    print("\n===================================")
    print("INTEGRATION SUMMARY")
    print("===================================")

    print("Reference paper:", REFERENCE_FILE.name)
    print("Total Telegram records:", len(evidence_records))
    print("Successfully processed:", processed)
    print("Skipped:", skipped)
    print("Total questions compared:", len(all_results))
    print("Possible matches:", len(all_alerts))

    print("\nResults saved:", RESULTS_FILE.name)
    print("Alerts saved:", ALERTS_FILE.name)

    print("\nManual review is required for all possible matches.")
    print("===================================")


if __name__ == "__main__":
    run_telegram_ocr()
