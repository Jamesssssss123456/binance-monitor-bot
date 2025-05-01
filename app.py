
import os
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

if __name__ == "__main__":
    message = """
🚨【轧空信號預警】(測試訊號注入)

合約：VOXELUSDT
資金費率：-0.142%
OI激增比率：2.79
時間：2025-05-01 23:15 UTC

🔍 TradingView 圖表：
https://www.tradingview.com/symbols/VOXELUSDT.P/

📈 Binance 行情頁面：
https://www.binance.com/en/futures/VOXELUSDT
"""
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    print("✅ 測試訊號已發送")
