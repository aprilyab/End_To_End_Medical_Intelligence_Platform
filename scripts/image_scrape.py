from telethon import TelegramClient
from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime

# ------------------ Load Environment ------------------
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE_NUMBER")

# ------------------ Initialize Telegram Client ------------------
client = TelegramClient("image_session", api_id, api_hash)

# ------------------ Paths ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_LAKE_IMAGES = os.path.join(BASE_DIR, "data", "raw", "images")
DATA_LAKE_META = os.path.join(BASE_DIR, "data", "raw", "telegram_images")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# ------------------ Setup Logging ------------------
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "image_scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ Image Scraper ------------------
async def scrape_images(channels):
    today = datetime.now().strftime("%Y-%m-%d")

    for channel in channels:
        try:
            print(f"📸 Scraping images from: {channel}")
            logging.info(f"Scraping channel: {channel}")

            channel_name = channel.split("/")[-1]
            images = []

            async for message in client.iter_messages(channel, limit=200):
                if message.photo:
                    # Prepare image file path
                    image_dir = os.path.join(DATA_LAKE_IMAGES, today, channel_name)
                    os.makedirs(image_dir, exist_ok=True)

                    filename = f"{channel_name}_{message.id}.jpg"
                    filepath = os.path.join(image_dir, filename)

                    try:
                        await message.download_media(file=filepath)
                        print(f"🖼️ Saved image: {filename}")
                        logging.info(f"Image saved: {filepath}")

                        # Save raw metadata
                        images.append({
                            "id": message.id,
                            "channel": channel,
                            "date": message.date.isoformat(),
                            "views": message.views,
                            "image_path": filepath
                        })

                    except Exception as e:
                        print(f"[!] Failed to save image {filename}: {e}")
                        logging.error(f"❌ Failed to download image {filename}: {e}")

            # Save image metadata JSON
            if images:
                meta_dir = os.path.join(DATA_LAKE_META, today)
                os.makedirs(meta_dir, exist_ok=True)
                meta_path = os.path.join(meta_dir, f"{channel_name}.json")

                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(images, f, ensure_ascii=False, indent=2)

                print(f"✅ Metadata saved to {meta_path}")
                logging.info(f"✅ Metadata for {channel_name} saved with {len(images)} images.")

        except Exception as e:
            print(f"[!] Error scraping channel '{channel}': {e}")
            logging.error(f"❌ Skipping channel {channel}: {e}")

# ------------------ Runner ------------------
async def main():
    await client.start(phone=phone)
    print("🔌 Logged in to Telegram.")

    channels = [
        'https://t.me/tikvahpharma',
        'https://t.me/lobelia4cosmetics',
        'https://t.me/CheMed123',
        'https://t.me/ethiopianfoodanddrugauthority'
    ]

    await scrape_images(channels)
    print("🏁 Image scraping completed.")
    logging.info("🎯 All image scraping tasks completed successfully.")

# ------------------ Execute ------------------
with client:
    client.loop.run_until_complete(main())
