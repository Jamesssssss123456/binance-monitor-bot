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
        msg = "📈 AI索罗斯信号：出现多头爆发预警 (Long)"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
    elif signal == "short":
        msg = "📉 AI索罗斯信号：出现空头崩盘预警 (Short)"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

def backtest_handler(update: Update, context: CallbackContext):
    result = run_backtest_result()
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    job = updater.job_queue
    job.run_repeating(signal_check, interval=300, first=1)
    updater.dispatcher.add_handler(CommandHandler("backtest", backtest_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
