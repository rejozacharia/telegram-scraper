import asyncio
import json
import os
import time
import pytesseract
import re
import requests
import logging
from telethon import TelegramClient, events
from PIL import Image

# Load configuration from secrets file
with open(os.path.join(os.path.dirname(__file__), "../config/secrets.json")) as f:
    secrets = json.load(f)

api_id = secrets["api_id"]
api_hash = secrets["api_hash"]
phone = secrets["phone"]
channel_name = secrets["channel_name"]
bot_token = secrets["bot_token"]
recipient_ids = secrets["recipient_ids"]

# Configure Tesseract executable path if necessary
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define a list of specific words to search for
specific_words = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa", "MM/DD/YYYY", "Time", "Availability"]

# Define a regex pattern for dates (e.g., M/D/YYYY, MM/DD/YYYY, D/M/YYYY, DD/MM/YYYY)
date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_image_for_text(image_path):
    # Open the image file and extract text using Tesseract OCR
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    
    # Find specific words and date patterns in the OCR result
    found_words = [word for word in specific_words if word in text]
    found_dates = re.findall(date_pattern, text)
    
    return text, found_words, found_dates

def send_message_via_bot(photo_path, found_words, found_dates):
    # Construct message
    message = f"Found dates: {found_dates}"
    send_text_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    send_photo_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    
    for recipient_id in recipient_ids:
        # Send text message
        requests.post(send_text_url, data={'chat_id': recipient_id, 'text': message})
        # Send the photo
        with open(photo_path, 'rb') as photo:
            requests.post(send_photo_url, data={'chat_id': recipient_id}, files={'photo': photo})

async def fetch_messages(client):
    # Get the channel entity
    channel = await client.get_entity(channel_name)
    last_message_id = None

    while True:
        try:
            messages = await client.get_messages(channel, limit=100)
            for message in messages:
                if last_message_id is None or message.id > last_message_id:
                    logger.info(f"New message from {channel_name} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

                    if message.photo:
                        photo_path = await message.download_media()
                        logger.debug(f"Downloaded photo to {photo_path}")

                        text, found_words, found_dates = parse_image_for_text(photo_path)
                        if found_words and 'No Slots Available' not in text and 'Scheduled Website Maintenance' not in text:
                            logger.info(f"Found words: {found_words}")
                            logger.info(f"Found dates: {found_dates}")
                            send_message_via_bot(photo_path, found_words, found_dates)
                        
                        os.remove(photo_path)
                        logger.debug(f"Deleted photo file {photo_path}")

                    last_message_id = message.id

            await asyncio.sleep(60)
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await asyncio.sleep(30)

async def main():
    while True:
        try:
            async with TelegramClient('session_name', api_id, api_hash) as client:
                await client.start(phone)
                await fetch_messages(client)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            if os.path.exists('session_name.session'):
                os.remove('session_name.session')
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
