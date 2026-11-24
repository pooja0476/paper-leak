import sqlite3
import hashlib
import csv
from pathlib import Path
from datetime import datetime, timezone

MEMBER1_DIR = Path(__file__).resolve().parent.parent
DB_PATH = MEMBER1_DIR / "data" / "evidence.db"
REPORT_PATH = MEMBER1_DIR / "data" / "evidence_integrity_report.csv"


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_evidence():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT evidence_id, media_path, sha256_hash
        FROM evidence
        WHERE media_path IS NOT NULL
    """)

    records = cursor.fetchall()
    connection.close()

    verified = 0
    failed = 0
    report_rows = []

    print("\n===== EVIDENCE INTEGRITY REPORT =====\n")

    for evidence_id, media_path, stored_hash in records:
        file_path = MEMBER1_DIR / media_path

        if not file_path.exists():
            status = "MISSING FILE"
            actual_hash = ""
            failed += 1

        elif not stored_hash:
            status = "MISSING STORED HASH"
            actual_hash = calculate_sha256(file_path)
            failed += 1

        else:
            actual_hash = calculate_sha256(file_path)

            if actual_hash == stored_hash:
                status = "VERIFIED"
                verified += 1
            else:
                status = "HASH MISMATCH"
                failed += 1

        print(f"{status}: {evidence_id}")

        report_rows.append([
            evidence_id,
            media_path,
            stored_hash or "",
            actual_hash,
            status,
            datetime.now(timezone.utc).isoformat()
        ])

    with open(REPORT_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Evidence ID",
            "Media Path",
            "Stored SHA-256",
            "Actual SHA-256",
            "Verification Status",
            "Verification Time"
        ])

        writer.writerows(report_rows)

    print("\n========== SUMMARY ==========")
    print(f"Total records checked: {len(records)}")
    print(f"Verified files: {verified}")
    print(f"Failed files: {failed}")
    print(f"\nCSV report saved: {REPORT_PATH}")


if __name__ == "__main__":
    verify_evidence()