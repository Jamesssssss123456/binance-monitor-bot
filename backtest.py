import pandas as pd
import os
from model_predictor import load_model_and_predict
from indicator_utils import extract_features

def run_backtest_result():
    folder = "data"
    files = sorted([f for f in os.listdir(folder) if f.startswith("VOXELUSDT") and f.endswith(".csv")])
    long_signals = 0
    short_signals = 0

    for file in files:
        df = pd.read_csv(os.path.join(folder, file))
        for i in range(len(df)):
            row = {
                "long_short_account_ratio": df["long_short_account_ratio"][i],
                "top_trader_account_ls_ratio": df["top_trader_account_ls_ratio"][i],
                "top_trader_position_ls_ratio": df["top_trader_position_ls_ratio"][i],
                "oi_change_pct": df["oi_change_pct"][i],
                "basis_percent": df["basis_percent"][i],
            }
            features = extract_features(row)
            signal = load_model_and_predict(features)
            if signal == "long":
                long_signals += 1
            elif signal == "short":
                short_signals += 1

    total = long_signals + short_signals
    win_rate = round(100 * long_signals / total, 2) if total > 0 else 0
    return f"📊 回测完成，共检测 {total} 次信号\n🟢Long: {long_signals} 次\n🔴Short: {short_signals} 次\n✅Win Rate: {win_rate:.2f}%"
# Backtest logic to respond to /backtest
