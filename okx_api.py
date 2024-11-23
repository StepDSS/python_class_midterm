import requests

def get_price(asset="BTC-USDT"):
    url = f"https://www.okx.com/api/v5/market/ticker?instId={asset}"
    try:
        response = requests.get(url)
        data = response.json()
        return float(data["data"][0]["last"])
    except:
        return None