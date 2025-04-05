# Telegram Channel Scraper

## Overview

This project is a Telegram channel scraper built using Python. It monitors a specific Telegram channel for new messages that contain image attachments. When an image is received, it uses Tesseract OCR to extract text from the image, searches for specific keywords and date patterns, and sends notifications via a Telegram Bot to a list of recipients—if certain conditions are met.

## Purpose

The main goal of this project is to automate the monitoring of a Telegram channel for slot updates or announcements. It extracts dates and keywords from images posted in the channel and forwards important notifications (via text and image) to designated Telegram users.

## Approach

1. **Monitoring:**  
   The project uses the [Telethon](https://docs.telethon.dev/en/stable/) library to connect to Telegram, authenticate, and fetch messages from a specified channel.

2. **OCR Processing:**  
   When a message contains an image, the script downloads it and uses [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (via the [pytesseract](https://pypi.org/project/pytesseract/) library) to extract text.

3. **Keyword & Date Filtering:**  
   The extracted text is checked for specific keywords (e.g., days of the week, "Time", "Availability") and date patterns (in various formats). The script only sends notifications if the keywords are found and if the text does **not** include phrases such as "No Slots Available" or "Scheduled Website Maintenance".

4. **Notification:**  
   A Telegram Bot (using the Bot API) sends the notification message and image to predefined recipient chat IDs.

5. **Robustness:**  
   The script includes error handling and reconnection logic to manage network issues, unexpected disconnections, and session problems.

## Prerequisites

- **Python 3.7+**  
- **Tesseract OCR:**  
  - Download and install from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
  - Ensure the Tesseract executable path is set correctly in the script.
- **Python Libraries:**  
  Install the required libraries by running:
  ```bash
  pip install -r requirements.txt

 ## Configuration

This project uses a separate secrets file for sensitive API credentials and configuration. To set up your environment:

1. Navigate to the `config/` directory.
2. Copy `secrets_example.json` to `secrets.json`.
3. Edit `secrets.json` and fill in your API credentials, phone number, channel username, bot token, and recipient IDs.

These credentials will be loaded by the script at runtime, ensuring that sensitive information is not included in the public repository.


