
def prepare_features(data):
    return [
        data.get("oi_change_pct", 0),
        data.get("basis_percent_negative", 0),
        data.get("top_trader_account_ls_ratio", 0),
        data.get("top_trader_position_ls_ratio", 0)
    ]
