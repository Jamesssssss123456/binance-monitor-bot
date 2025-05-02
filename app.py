
import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from indicator_utils import fetch_binance_snapshot, extract_features
from model_predictor import load_model_and_predict
from backtest import run_backtest_result

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def signal_check(context: CallbackContext):
    snapshot = fetch_binance_snapshot()
    features = extract_features(snapshot)
    signal = load_model_and_predict(features)
    if signal == "long":
        msg = "📈 AI索罗斯信号：出現多頭爆拉預警（Long）"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
    elif signal == "short":
        msg = "📉 AI索罗斯信号：出現空頭崩盤預警（Short）"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

def backtest(update: Update, context: CallbackContext):
    result = run_backtest_result()
    update.message.reply_text(result)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("backtest", backtest))

    updater.job_queue.run_repeating(signal_check, interval=300, first=5)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
