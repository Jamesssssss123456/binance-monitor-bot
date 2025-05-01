import requests

def fetch_binance_snapshot(symbol='VOXELUSDT'):
    url = f"https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol={symbol}&period=5m&limit=1"
    return requests.get(url).json()

def extract_features(snapshot):
    # 模擬特徵擷取
    return [0.5, 0.2, 0.3, 0.1, 0.05]