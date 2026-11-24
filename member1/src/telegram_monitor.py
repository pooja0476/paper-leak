
import os
import sys
import hashlib
import asyncio
from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv
from telethon import TelegramClient, events

# ==========================================
# MEMBER 1 PATHS
# ==========================================

MEMBER1_DIR = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = MEMBER1_DIR / "data" / "evidence"
SESSION_PATH = MEMBER1_DIR / "data" / "telegram_session"

sys.path.insert(0, str(MEMBER1_DIR))

from database.evidence_db import create_database, save_evidence

# ==========================================
# LOAD TELEGRAM CREDENTIALS
# ==========================================

load_dotenv(MEMBER1_DIR / ".env")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient(
    str(SESSION_PATH),
    API_ID,
    API_HASH
)

# ==========================================
# SHA-256 HASH CALCULATION
# ==========================================

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# ==========================================
# DOWNLOAD IMAGE / PDF EVIDENCE
# ==========================================

async def download_media_evidence(message, evidence_id):

    if not message.photo and not message.document:
        return None, None, None

    mime_type = message.file.mime_type if message.file else None

    if message.photo:
        media_type = mime_type or "image/jpeg"
        extension = message.file.ext or ".jpg"

    elif message.document and (
        mime_type == "application/pdf"
        or (mime_type and mime_type.startswith("image/"))
    ):
        media_type = mime_type

        extension = message.file.ext or (
            ".pdf" if mime_type == "application/pdf" else ".jpg"
        )

    else:
        return None, None, None

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    destination = EVIDENCE_DIR / f"{evidence_id}{extension}"

    downloaded_path = await message.download_media(
        file=str(destination)
    )

    if not downloaded_path:
        return None, None, None

    file_hash = calculate_sha256(downloaded_path)

    relative_path = str(
        Path(downloaded_path).relative_to(MEMBER1_DIR)
    )

    print("Media downloaded:", relative_path)
    print("SHA-256:", file_hash)

    return relative_path, media_type, file_hash


# ==========================================
# SAVE TELEGRAM MESSAGE
# ==========================================

async def process_message(message, entity, channel):

    if not message:
        return

    collected_at = datetime.now(timezone.utc).isoformat()

    original_date = (
        message.date.isoformat()
        if message.date
        else None
    )

    username = getattr(entity, "username", None)

    if username:
        message_link = f"https://t.me/{username}/{message.id}"
    else:
        message_link = "No public message link"

    evidence_id = f"TG_{entity.id}_{message.id}"

    media_path, media_type, sha256_hash = (
        await download_media_evidence(message, evidence_id)
    )

    save_evidence(
        evidence_id=evidence_id,
        channel_name=channel,
        channel_id=entity.id,
        message_id=message.id,
        message_link=message_link,
        message_text=message.message or "",
        original_date=original_date,
        collected_at=collected_at,
        media_path=media_path,
        media_type=media_type,
        sha256_hash=sha256_hash
    )

    print("Saved evidence:", evidence_id)
    print("Message link:", message_link)


# ==========================================
# MAIN TELEGRAM MONITOR
# ==========================================

async def main():

    print("Connecting to Telegram...")

    await client.start()

    print("Telegram connected successfully!")

    create_database()

    channels_file = MEMBER1_DIR / "channels.txt"

    with open(channels_file, "r", encoding="utf-8") as file:
        channels = [
            line.strip().lstrip("@")
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]

    monitored_entities = []

    # ======================================
    # INITIAL COLLECTION
    # ======================================

    for channel in channels:

        print(f"\nCollecting initial messages from {channel}")

    try:
        # First, try to resolve a public channel
        try:
            entity = await client.get_entity(channel)

        except Exception:
            # If it is private, search channels available in this account
            entity = None

            async for dialog in client.iter_dialogs():
                if (
                    dialog.is_channel
                    and dialog.name.strip().lower() == channel.strip().lower()
                ):
                    entity = dialog.entity
                    break

            if entity is None:
                raise ValueError(
                    f"Channel '{channel}' not found in your Telegram dialogs."
                )

        monitored_entities.append(entity)

        async for message in client.iter_messages(
            entity,
            limit=5
        ):
            await process_message(message, entity, channel)

    except Exception as error:
            print(f"Could not read @{channel}: {error}")

    # ======================================
    # CONTINUOUS MONITORING
    # ======================================

    if not monitored_entities:
        print("No channels could be accessed. Monitoring stopped.")
        return

    @client.on(events.NewMessage(chats=monitored_entities))
    async def new_message_handler(event):

        try:
            entity = await event.get_chat()

            channel = getattr(entity, "username", None)
            channel = channel or str(entity.id)

            print(f"\nNew message detected in @{channel}")

            await process_message(
                event.message,
                entity,
                channel
            )

        except Exception as error:
            print("Error processing new message:", error)

    print("\n===================================")
    print("CONTINUOUS TELEGRAM MONITORING ON")
    print("Listening for new messages...")
    print("Press Ctrl + C to stop monitoring.")
    print("===================================")

    await client.run_until_disconnected()


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    try:
        with client:
            client.loop.run_until_complete(main())

    except KeyboardInterrupt:
        print("\nTelegram monitoring stopped.")

    except Exception as error:
        print(f"\nTelegram monitor stopped due to an error: {error}")
        print("Check your internet connection and restart the script.")