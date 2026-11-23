
import sqlite3
from pathlib import Path

# Database location
MEMBER1_DIR = Path(__file__).resolve().parent.parent
DB_PATH = MEMBER1_DIR / "data" / "evidence.db"


def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            evidence_id TEXT PRIMARY KEY,
            channel_name TEXT,
            channel_id TEXT,
            message_id INTEGER,
            message_link TEXT,
            message_text TEXT,
            original_date TEXT,
            collected_at TEXT,
            media_path TEXT,
            media_type TEXT,
            sha256_hash TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("Evidence database created successfully!")


def save_evidence(
    evidence_id,
    channel_name,
    channel_id,
    message_id,
    message_link,
    message_text,
    original_date,
    collected_at,
    media_path=None,
    media_type=None,
    sha256_hash=None
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO evidence (
            evidence_id,
            channel_name,
            channel_id,
            message_id,
            message_link,
            message_text,
            original_date,
            collected_at,
            media_path,
            media_type,
            sha256_hash
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(evidence_id) DO UPDATE SET
            media_path = COALESCE(excluded.media_path, evidence.media_path),
            media_type = COALESCE(excluded.media_type, evidence.media_type),
            sha256_hash = COALESCE(excluded.sha256_hash, evidence.sha256_hash)
    """, (
        evidence_id,
        channel_name,
        str(channel_id),
        message_id,
        message_link,
        message_text,
        original_date,
        collected_at,
        media_path,
        media_type,
        sha256_hash
    ))

    connection.commit()
    connection.close()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO evidence (
            evidence_id,
            channel_name,
            channel_id,
            message_id,
            message_link,
            message_text,
            original_date,
            collected_at,
            media_path,
            media_type,
            sha256_hash
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        evidence_id,
        channel_name,
        str(channel_id),
        message_id,
        message_link,
        message_text,
        original_date,
        collected_at,
        media_path,
        media_type,
        sha256_hash
    ))

    connection.commit()
    connection.close()

def view_evidence():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
         SELECT evidence_id, channel_name, message_id, message_link
         FROM evidence
    """)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    print("\nTotal saved records:", len(rows))

    connection.close()



if __name__ == "__main__":
    create_database()
