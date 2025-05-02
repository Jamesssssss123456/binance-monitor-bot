
import pandas as pd
import joblib
from sklearn.metrics import classification_report

MODEL_PATH = "model/ai_soros_model.pkl"
DATA_PATH = "data/data_ALPACAUSDT.csv"

def run_backtest():
    try:
        # 讀取模型與資料
        model = joblib.load(MODEL_PATH)
        df = pd.read_csv(DATA_PATH)
        
        # 特徵與標籤
        features = [
            "oi_change_pct",
            "basis_percent_negative",
            "top_trader_account_ls_ratio",
            "top_trader_position_ls_ratio"
        ]
        X = df[features]
        y_true = df["label"]

        # 模型預測
        y_pred = model.predict(X)

        # 將 -1、1 → 有預測，0 → 無預測
        y_pred_signal = [1 if p != 0 else 0 for p in y_pred]
        y_true_signal = [1 if t != 0 else 0 for t in y_true]

        # 輸出評估指標
        print("📊 回測結果 (暴漲/暴跌 總預測勝率):")
        print(classification_report(y_true_signal, y_pred_signal, digits=3))

    except Exception as e:
        print(f"❌ 回測失敗：{e}")

if __name__ == "__main__":
    run_backtest()
