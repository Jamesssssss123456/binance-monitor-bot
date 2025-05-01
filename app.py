
import requests
import time
from datetime import datetime
from telegram import Bot
import os

# 讀取環境變數（Render 中設定）
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

FUNDING_THRESHOLD = -0.001
OI_SPIKE_RATIO = 2.0

def get_usdt_symbols():
    url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    response = requests.get(url, timeout=10)
    data = response.json()
    symbols = [s['symbol'] for s in data['symbols']
               if s['contractType'] == 'PERPETUAL'
               and s['quoteAsset'] == 'USDT'
               and not s['symbol'].startswith(('BTC', 'ETH'))]
    return symbols

def fetch_data(symbol):
    try:
        funding_url = f'https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1'
        oi_url = f'https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period=5m&limit=10'

        funding_data = requests.get(funding_url, timeout=10).json()
        oi_data = requests.get(oi_url, timeout=10).json()

        if not funding_data or not oi_data:
            return None

        funding_rate = float(funding_data[-1]['fundingRate'])
        oi_values = [float(x['sumOpenInterest']) for x in oi_data]
        if len(oi_values) < 10:
            return None

        oi_short_avg = sum(oi_values[-3:]) / 3
        oi_long_avg = sum(oi_values) / 10
        oi_ratio = oi_short_avg / oi_long_avg if oi_long_avg else 0

        return {
            'symbol': symbol,
            'funding_rate': funding_rate,
            'oi_ratio': oi_ratio,
            'time': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        }
    except Exception:
        return None

def check_and_alert(data):
    if data['funding_rate'] < FUNDING_THRESHOLD and data['oi_ratio'] > OI_SPIKE_RATIO:
        sym = data['symbol']
        tv_link = f"https://www.tradingview.com/symbols/{sym}P/"
        binance_link = f"https://www.binance.com/en/futures/{sym}"
        message = (
            f"🚨【轧空信號預警】\n\n"
            f"合約：{sym}\n"
            f"資金費率：{data['funding_rate']:.3%}\n"
            f"OI激增比率：{data['oi_ratio']:.2f}\n"
            f"時間：{data['time']}\n\n"
            f"🔍 TradingView 圖表：\n{tv_link}\n\n"
            f"📈 Binance 行情頁面：\n{binance_link}"
        )
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def main_loop():
    while True:
        symbols = get_usdt_symbols()
        for sym in symbols:
            data = fetch_data(sym)
            if data:
                check_and_alert(data)
        print(f"[{datetime.utcnow()}] ✅ 任務完成，休眠5分鐘...")
        time.sleep(300)

if __name__ == "__main__":
    main_loop()
