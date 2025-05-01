import os
from telegram import Bot
from indicator_utils import fetch_binance_snapshot, extract_features
from model_predictor import load_model_and_predict

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

def main():
    snapshot = fetch_binance_snapshot()
    features = extract_features(snapshot)
    signal = load_model_and_predict(features)

    if signal == "long":
        msg = "📈 AI索罗斯信号：出现多头爆发预警（Long）"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
    elif signal == "short":
        msg = "📉 AI索罗斯信号：出现空头崩盘预警（Short）"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

if __name__ == "__main__":
    main()