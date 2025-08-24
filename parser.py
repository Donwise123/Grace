import re

def parse_signal(text):
    text = text.lower()

    if "buy" in text:
        return {"pair": "XAUUSD", "action": "buy", "entry": None, "sl": None, "tp": None}
    elif "sell" in text:
        return {"pair": "XAUUSD", "action": "sell", "entry": None, "sl": None, "tp": None}

    return None

def detect_short_vip(text):
    return ("buy" in text.lower() or "sell" in text.lower()) and "now" in text.lower()
