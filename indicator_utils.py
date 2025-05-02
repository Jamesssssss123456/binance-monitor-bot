def fetch_binance_snapshot():
    return {
        "long_short_account_ratio": 0.85,
        "top_trader_account_ls_ratio": 0.40,
        "top_trader_position_ls_ratio": 0.38,
        "oi_change_pct": 0.52,
        "basis_percent": -1.20
    }

def extract_features(snapshot):
    return [
        snapshot["long_short_account_ratio"],
        snapshot["top_trader_account_ls_ratio"],
        snapshot["top_trader_position_ls_ratio"],
        snapshot["oi_change_pct"],
        snapshot["basis_percent"]
    ]
