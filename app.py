
import os
import time
from telegram.ext import CommandHandler, Updater
from indicator_utils import fetch_binance_snapshot, extract_features
from model_predictor import load_model_and_predict
from backtest import run_backtest_result

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def signal_check(context):
    snapshot = fetch_binance_snapshot()
    features = extract_features(snapshot)
    signal = load_model_and_predict(features)
    if signal == "long":
        msg = "🟢 AI索罗斯轧空信号：出現多头爆发徵兆（Long）"
    elif signal == "short":
        msg = "🔴 AI索罗斯轧空信号：出現暴跌崩盘徵兆（Short）"
    else:
        msg = None
    if msg:
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

def backtest_handler(update, context):
    result_msg = run_backtest_result()
    context.bot.send_message(chat_id=update.effective_chat.id, text=result_msg)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("backtest", backtest_handler))

    job_queue = updater.job_queue
    job_queue.run_repeating(signal_check, interval=300, first=5)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
