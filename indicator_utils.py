
def fetch_binance_snapshot():
    # 模擬 VOXEL 指標數據
    return {
        "long_short_account_ratio": 0.85,
        "top_trader_account_ls_ratio": 0.40,
        "top_trader_position_ls_ratio": 0.38,
        "oi_change_pct": 0.52,
        "basis_percent": -1.20,
    }

def extract_features(snapshot):
    return [
        snapshot["long_short_account_ratio"],
        snapshot["top_trader_account_ls_ratio"],
        snapshot["top_trader_position_ls_ratio"],
        snapshot["oi_change_pct"],
        abs(snapshot["basis_percent"]) if snapshot["basis_percent"] < 0 else 0
    ]
