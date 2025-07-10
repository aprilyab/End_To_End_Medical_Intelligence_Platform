from telethon import TelegramClient
from dotenv import load_dotenv
import os
import re
import json
import logging
from datetime import datetime

# ------------------ Load Environment ------------------
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE_NUMBER")

# ------------------ Setup Telegram Client ------------------
client = TelegramClient("medical_session", api_id, api_hash)

# ------------------ Define Base Paths ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_LAKE_DIR = os.path.join(BASE_DIR, "data", "raw", "telegram_messages")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# ------------------ Setup Logging ------------------
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "message_scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ Text Cleaner for Amharic ------------------
def clean_text(text):
    if text is None:
        return ""
    # Keep Amharic characters, punctuation, Latin letters, numbers, space
    text = re.sub(r"[^\u1200-\u137F\u1380-\u139F\u2D80-\u2DDF\u0300-\u036F\s\w.,!?]", "", text)
    return re.sub(r"\s+", " ", text).strip()

# ------------------ Populate Data Lake with Raw JSON ------------------
async def populate_data_lake(channels):
    today = datetime.now().strftime("%Y-%m-%d")

    for channel in channels:
        try:
            channel_name = channel.split("/")[-1]
            print(f"📥 Scraping: {channel_name}")
            logging.info(f"Start scraping channel: {channel}")

            raw_messages = []

            async for message in client.iter_messages(channel, limit=100):
                if message.message:
                    raw_messages.append({
                        "id": message.id,
                        "channel": channel,
                        "date": message.date.isoformat(),
                        "views": message.views,
                        "text": clean_text(message.message)
                    })

            # Define output path: data/raw/telegram_messages/YYYY-MM-DD/channel_name.json
            output_dir = os.path.join(DATA_LAKE_DIR, today)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{channel_name}.json")

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(raw_messages, f, ensure_ascii=False, indent=2)

            print(f"✅ Data saved to {output_path}")
            logging.info(f"✅ Saved {len(raw_messages)} messages from {channel} to {output_path}")

        except Exception as e:
            print(f"[!] Error scraping {channel}: {e}")
            logging.error(f"❌ Failed scraping {channel}: {e}")

# ------------------ Main Runner ------------------
async def main():
    await client.start(phone=phone)
    print("🔌 Telegram client connected.")

    # List of target channels
    channels = [
        'https://t.me/CheMed123',
        'https://t.me/lobelia4cosmetics',
        'https://t.me/tikvahpharma',
        'https://t.me/ethiopianfoodanddrugauthority'
    ]

    await populate_data_lake(channels)
    print("🏁 All scraping completed.")
    logging.info("🎯 All message scraping tasks finished successfully.")

# ------------------ Execute ------------------
with client:
    client.loop.run_until_complete(main())
