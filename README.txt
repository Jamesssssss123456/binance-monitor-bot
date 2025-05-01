# Binance Altcoin Short Squeeze Monitor (Render.com 版本)

## ✅ 功能
- 每 5 分鐘監控所有 Binance USDT 永續合約（排除 BTC/ETH）
- 根據策略：極端負 funding rate + OI 激增
- 發送警報到 Telegram 群組

## 🚀 部署方式（Render.com）

1. 註冊 / 登入 https://render.com
2. 建立新的 Web Service
3. 連結 GitHub repo（或選擇 "Deploy from Zip" 並上傳此壓縮包）
4. 環境設定：
   - `Start Command`: `python app.py`
   - `Environment`: Python 3
   - 新增兩個環境變數：
     - `TELEGRAM_TOKEN`: 你的 Bot Token
     - `TELEGRAM_CHAT_ID`: 你的 Telegram Chat ID
5. 點 Deploy 即可，5 分鐘後收到 Telegram 警報 ✅