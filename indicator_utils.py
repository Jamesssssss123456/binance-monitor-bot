
def fetch_binance_snapshot():
    # Dummy Binance snapshot structure (replace with real API calls)
    return {
        'oi_change_pct': 0.15,
        'basis_percent_negative': 0.08,
        'top_trader_account_ls_ratio': 0.4,
        'top_trader_position_ls_ratio': 0.5
    }

def extract_features(snapshot):
    return [
        snapshot['oi_change_pct'],
        snapshot['basis_percent_negative'],
        snapshot['top_trader_account_ls_ratio'],
        snapshot['top_trader_position_ls_ratio']
    ]
