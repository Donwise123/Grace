# Forex Copier Bot

Auto-trade Telegram Forex signals with zero delay and watchdog.

## Features
- Parses signals (buy/sell now, forwarded only)
- Attaches follow-ups (TP/SL updates)
- Auto-closes trade if 3 pips loss
- Deployable on Render with Docker

## Deployment on Render
1. Push repo to GitHub
2. Create new **Web Service** on Render
3. Connect your GitHub repo
4. Set Build Command: `docker build -t forex-bot .`
5. Set Start Command: `python telegram_listener.py`
6. Add Environment Variables:
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`
   - `TELEGRAM_PHONE`
   - `TELEGRAM_CHANNELS` (comma-separated links)
   - `WATCHDOG_INTERVAL=30`
