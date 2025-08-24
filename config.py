import os

# Telegram API credentials
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")  # For login (if needed)

# Channels
TELEGRAM_CHANNELS = os.getenv("TELEGRAM_CHANNELS", "").split(",")  
# Example: "https://t.me/freechannel1,https://t.me/freechannel2"

# Watchdog
WATCHDOG_INTERVAL = int(os.getenv("WATCHDOG_INTERVAL", "30"))

# FX API placeholder
FX_API_KEY = os.getenv("FX_API_KEY", "demo_key")
