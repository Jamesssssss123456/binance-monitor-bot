
import os
import pandas as pd
import requests
import joblib
from telegram import Bot
from datetime import datetime

def calculate_indicators(data):
    indicators = {}
    indicators['oi_change_pct'] = (data['oi'][-1] - data['oi'][-4]) / max(data['oi'][-4], 1)
    indicators['basis_percent_negative'] = abs(data['basis_percent'][-1]) if data['basis_percent'][-1] < 0 else 0
    indicators['top_trader_account_ls_ratio'] = data['top_trader_account_ls_ratio'][-1]
    indicators['top_trader_position_ls_ratio'] = data['top_trader_position_ls_ratio'][-1]
    return indicators

# ====== 設定區 ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ENABLE_AI_MODEL = True
MODEL_PATH = "ai_soros_model.pkl"
# =====================

bot = Bot(token=TELEGRAM_TOKEN)

def get_binance_data(symbol):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "mark_price": 0.23,
        "oi": [200000, 201000, 202500, 210000, 220000, 230000, 240000, 245000, 250000, 260000],
        "basis_percent": [-0.03]*10,
        "top_trader_account_ls_ratio": [0.48]*10,
        "top_trader_position_ls_ratio": [0.52]*10
    }

def load_model():
    if ENABLE_AI_MODEL:
        return joblib.load(MODEL_PATH)
    return None

def main_loop():
    symbol = "VOXELUSDT"
    data = get_binance_data(symbol)
    indicators = calculate_indicators(data)

    if ENABLE_AI_MODEL:
        model = load_model()
        X = pd.DataFrame([{
            "oi": indicators["oi_change_pct"],
            "basis_percent": indicators["basis_percent_negative"],
            "top_trader_account_ls_ratio": indicators["top_trader_account_ls_ratio"],
            "top_trader_position_ls_ratio": indicators["top_trader_position_ls_ratio"]
        }])
        pred = model.predict(X)[0]
        if pred == 1:
            msg = f"[AI模型信號] {symbol} 有潛在暴漲/暴跌風險 🚨"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
    else:
        msg = f"[原始模式] 暫無啟用 AI 模型"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

if __name__ == "__main__":
    main_loop()
