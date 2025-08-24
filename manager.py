import time

_open_trades = {}

async def open_trade_from_signal(fx, signal):
    trade_id = f"{signal['pair']}_{time.time()}"
    _open_trades[trade_id] = {
        "signal": signal,
        "entry_price": fx.get_price(signal["pair"]),
        "sl": None,
        "tp": None,
        "opened": time.time()
    }
    print("Opened trade:", _open_trades[trade_id])

async def apply_command_to_trade(fx, command, reply_to_id):
    for tid, t in _open_trades.items():
        if str(reply_to_id) in tid:
            if "tp" in command.lower():
                t["tp"] = fx.get_price(t["signal"]["pair"])
            if "sl" in command.lower():
                t["sl"] = fx.get_price(t["signal"]["pair"])
            print("Updated trade:", t)

async def watchdog_tick(fx):
    for tid, t in list(_open_trades.items()):
        current = fx.get_price(t["signal"]["pair"])
        entry = t["entry_price"]

        # Auto-close if 3 pips against us
        if t["signal"]["action"] == "buy" and current <= entry - 0.03:
            print("Auto-closed BUY trade (3 pips loss)")
            del _open_trades[tid]
        elif t["signal"]["action"] == "sell" and current >= entry + 0.03:
            print("Auto-closed SELL trade (3 pips loss)")
            del _open_trades[tid]

def save_state():
    pass
