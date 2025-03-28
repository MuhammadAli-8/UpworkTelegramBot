### README.md

# Upwork Telegram Bot 🚀

A Python bot that scrapes the latest job postings from Upwork and sends real-time notifications via Telegram.

## Features
- Scrapes Upwork job postings based on keywords
- Sends job details (title, link, description) to a Telegram chat
- Uses Selenium for web scraping
- Stores the latest job to prevent duplicate notifications

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/MuhammadAli-8/UpworkTelegramBot.git
   cd UpworkTelegramBot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project directory:
   ```bash
   TELEGRAM_TOKEN=your_telegram_bot_token
   CHAT_ID=your_chat_id
   ```
  
## Usage

Run the script:
```bash
python main.py
```

The bot will start scraping Upwork and sending job updates to Telegram.

## Contributing
Feel free to submit pull requests or open issues for improvements!

## License
MIT License

## Disclaimer
This bot is for educational purposes only. Scraping Upwork may violate its terms of service. Use at your own risk.
