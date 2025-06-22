# 🕘 Telegram Daily Market Reminder Bot

This is a simple Telegram bot built with `python-telegram-bot` and `apscheduler`. It sends **daily trading analysis reminders** directly to your **Telegram DM** at 9:00 AM (GMT+1) using your custom message guide.

## 🔧 Features

- Sends daily messages based on the trading day (Monday to Sunday)
- Targets individual Telegram ID (private DM only)
- Uses `apscheduler` for accurate daily scheduling
- Lightweight and suitable for VPS, Termux, or local deployment

## 📁 Files Included

- `main.py` – Bot logic and scheduler combined
- `config.json` – Stores your bot token and Telegram ID
- `requirements.txt` – Needed libraries

## 🧠 Message Format

Each day the bot sends a message like this:

```
🗓️ Yau Laraba ne –
🔥 Most reliable day for entries
✅ Breakout / Retest / SMC trades
🎯 Focus on continuation or reversal from Monday–Tuesday zone
⏰ Best time: 9:00 AM – 12:00 PM & 2:30 PM – 4:30 PM
#MarketReminder #BashirBot
```

## 🚀 Setup Guide

1. **Create a Bot** on Telegram via [@BotFather](https://t.me/BotFather)
2. Replace `"YOUR_BOT_TOKEN_HERE"` in `config.json` with your bot token
3. Ensure `user_id` is your Telegram numeric ID (use @userinfobot to find it)
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the bot:
    ```bash
    python main.py
    ```

## ⏰ Schedule

- Runs daily at **9:00 AM GMT+1 (Africa/Lagos)**

## 👤 Author

Developed by **Bashir Rabiu (@killerman6157)**  
Custom-built for daily market consistency and focus.
