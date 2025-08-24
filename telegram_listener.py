import asyncio, os, pytesseract, time
from PIL import Image
from telethon import TelegramClient, events
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_CHANNELS, WATCHDOG_INTERVAL
from parser import parse_signal, detect_short_vip
from manager import open_trade_from_signal, apply_command_to_trade, watchdog_tick, save_state
from fxapi_client import FXAPI

session_name = os.getenv("TELETHON_SESSION", "telegramfxcopier_session")
client = TelegramClient(session_name, TELEGRAM_API_ID, TELEGRAM_API_HASH)
fx = FXAPI()
_processed = set()

async def handle_message(event):
    try:
        msg = event.message
        mid = f"{msg.chat_id}:{msg.id}"
        if mid in _processed:
            return
        _processed.add(mid)

        # ✅ Only process forwarded messages
        if not msg.fwd_from:
            print("Ignored: not a forwarded VIP signal.")
            return

        text = msg.message or ""
        if msg.media:
            img_path = await msg.download_media()
            try:
                text += " " + pytesseract.image_to_string(Image.open(img_path))
            except Exception as e:
                print("OCR failure", e)

        # Parse signal
        signal = parse_signal(text)
        if signal:
            print("Parsed signal:", signal)
            await open_trade_from_signal(fx, signal)

        # Follow-up handling
        if msg.is_reply:
            reply_to = msg.reply_to_msg_id
            print("Applying follow-up command")
            await apply_command_to_trade(fx, msg.message, reply_to)

    except Exception as e:
        print("Error in handle_message:", e)

@client.on(events.NewMessage(chats=TELEGRAM_CHANNELS))
async def new_message_handler(event):
    await handle_message(event)

async def watchdog():
    while True:
        try:
            await watchdog_tick(fx)
            save_state()
        except Exception as e:
            print("Watchdog error:", e)
        await asyncio.sleep(WATCHDOG_INTERVAL)

async def main():
    await client.start(phone=TELEGRAM_PHONE)
    print("Bot started. Listening for signals...")
    asyncio.create_task(watchdog())
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
