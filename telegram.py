
import os
import requests

def send_telegram_alert(symbol, prob, features):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    message = f"🚨 {symbol} 觸發預測信號\n機率: {prob:.2%}\n特徵: {features}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})
