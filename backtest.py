# backtest.py

import pandas as pd
from model_predictor import predict_signal
from indicator_utils import calculate_indicators

def backtest_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    df['signal'] = None

    for i in range(10, len(df)):
        sample_data = {
            'oi': df['oi'][i-10:i].tolist(),
            'basis_percent': df['basis_percent'][i-10:i].tolist(),
            'top_trader_account_ls_ratio': df['top_trader_account_ls_ratio'][i-10:i].tolist(),
            'top_trader_position_ls_ratio': df['top_trader_position_ls_ratio'][i-10:i].tolist()
        }
        indicators = calculate_indicators(sample_data)
        signal = predict_signal(indicators)
        df.at[i, 'signal'] = signal

    return df[['timestamp', 'mark_price', 'signal']]
