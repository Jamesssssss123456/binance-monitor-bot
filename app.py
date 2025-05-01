
import os
import time
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from telegram import Bot

# Telegram config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

# Thresholds
FUNDING_THRESHOLD = -0.001
OI_SPIKE_RATIO = 2.0
AI_BULLISH_SCORE = 0.8
AI_BEARISH_SCORE = 0.8

# Fetch USDT perpetual pairs
def get_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return [s["symbol"] for s in data["symbols"]
                if s["contractType"] == "PERPETUAL"
                and s["quoteAsset"] == "USDT"
                and not s["symbol"].startswith(("BTC", "ETH"))]
    except Exception as e:
        print("get_symbols error:", e)
        return []

# Fetch metrics
def get_metrics(symbol):
    try:
        url = f"https://fapi.binance.com/futures/data/ticker?symbol={symbol}"
        fr_url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1"
        oi_url = f"https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period=5m&limit=10"
        acc_url = f"https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol={symbol}&period=5m&limit=2"
        top_acc_url = f"https://fapi.binance.com/futures/data/topLongShortAccountRatio?symbol={symbol}&period=5m&limit=2"
        top_pos_url = f"https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol={symbol}&period=5m&limit=2"

        fr = requests.get(fr_url).json()
        oi = requests.get(oi_url).json()
        acc = requests.get(acc_url).json()
        top_acc = requests.get(top_acc_url).json()
        top_pos = requests.get(top_pos_url).json()

        funding_rate = float(fr[-1]["fundingRate"])
        oi_values = [float(x["sumOpenInterest"]) for x in oi]
        oi_ratio = sum(oi_values[-3:]) / (sum(oi_values) / len(oi_values)) if len(oi_values) >= 10 else 0

        long_short_account_ratio = float(acc[-1]["longShortRatio"])
        top_trader_acc_ratio = float(top_acc[-1]["longShortRatio"])
        top_trader_pos_ratio = float(top_pos[-1]["longShortRatio"])

        mark_price = float(fr[-1]["markPrice"])
        index_price = float(fr[-1]["indexPrice"])
        basis_percent = (mark_price - index_price) / index_price * 100
        oi_change_pct = (oi_values[-1] - oi_values[-2]) / oi_values[-2] * 100 if len(oi_values) > 2 else 0

        return {
            "symbol": symbol,
            "funding_rate": funding_rate,
            "oi_ratio": oi_ratio,
            "long_short_account_ratio": long_short_account_ratio,
            "top_trader_acc_ratio": top_trader_acc_ratio,
            "top_trader_pos_ratio": top_trader_pos_ratio,
            "basis_percent": basis_percent,
            "oi_change_pct": oi_change_pct
        }
    except Exception as e:
        print(f"[{symbol}] metric error:", e)
        return None

# Logic-based squeeze detector
def detect_logic_squeeze(data):
    return data["funding_rate"] < FUNDING_THRESHOLD and data["oi_ratio"] > OI_SPIKE_RATIO

# AI model rules (based on your provided coefficients)
def ai_predict(data):
    bullish_score = (
        -0.758 * data["long_short_account_ratio"]
        -0.868 * data["top_trader_acc_ratio"]
        -0.545 * data["top_trader_pos_ratio"]
        + 2.163 * max(data["oi_change_pct"], 0)
        + 2.541 * abs(data["basis_percent"]) if data["basis_percent"] < 0 else 0
    )
    bearish_score = (
        -0.824 * data["long_short_account_ratio"]
        -0.934 * data["top_trader_acc_ratio"]
        -0.554 * data["top_trader_pos_ratio"]
        + 2.441 * max(data["oi_change_pct"], 0)
        + 1.761 * abs(data["basis_percent"]) if data["basis_percent"] < 0 else 0
    )
    return bullish_score, bearish_score

# Alert sender
def send_alert(symbol, logic_hit, bullish_score, bearish_score):
    msg = f"🚨【轧空策略信號】

幣種：{symbol}
"
    if logic_hit:
        msg += "🔍 傳統策略：符合 Funding + OI 激增 條件
"
    if bullish_score > AI_BULLISH_SCORE:
        msg += f"📈 AI預測：暴漲機率高（Score: {bullish_score:.2f}）
"
    if bearish_score > AI_BEARISH_SCORE:
        msg += f"📉 AI預測：暴跌機率高（Score: {bearish_score:.2f}）
"
    if bullish_score > AI_BULLISH_SCORE and bearish_score > AI_BEARISH_SCORE:
        msg += "⚠️ 暴漲暴跌信號衝突，建議觀望
"
    msg += f"
🔗 https://www.binance.com/en/futures/{symbol}
🕒 {datetime.utcnow()} UTC"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

# Main
def main():
    while True:
        print("🚀 開始輪詢...")
        for sym in get_symbols():
            data = get_metrics(sym)
            if data:
                logic_hit = detect_logic_squeeze(data)
                bull_score, bear_score = ai_predict(data)
                if logic_hit or bull_score > AI_BULLISH_SCORE or bear_score > AI_BEARISH_SCORE:
                    send_alert(sym, logic_hit, bull_score, bear_score)
        print(f"✅ 完成一輪檢查，休息 5 分鐘
")
        time.sleep(300)

if __name__ == "__main__":
    main()
