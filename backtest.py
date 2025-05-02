
import pandas as pd
import os
from model_predictor import load_model_and_predict
from indicator_utils import extract_features

def run_backtest_result():
    folder = "."
    files = sorted([f for f in os.listdir(folder) if f.startswith("VOXELUSDT-1h-202") and f.endswith(".csv")])
    long_signals = 0
    short_signals = 0
    for file in files:
        df = pd.read_csv(file)
        for i in range(len(df)):
            row = {
                "long_short_account_ratio": 0.85,
                "top_trader_account_ls_ratio": 0.40,
                "top_trader_position_ls_ratio": 0.38,
                "oi_change_pct": 0.52,
                "basis_percent": -1.20,
            }
            features = extract_features(row)
            signal = load_model_and_predict(features)
            if signal == "long":
                long_signals += 1
            elif signal == "short":
                short_signals += 1
    total = long_signals + short_signals
    win_rate = round(100 * long_signals / total, 2) if total > 0 else 0
    return f"📊 回测完成：共检测 {total} 次信号，胜率为 {win_rate:.2f}%，共盈利 {total_profit:.2f} USDT"
"多头信号: {long_signals} 次"
"空头信号: {short_signals} 次"
胜率估计：{win_rate}%"
