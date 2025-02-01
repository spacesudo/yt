import requests

def get_chart_data(api_key,chain, studies=None, interval="4h", theme="dark"):
    url = "https://api.chart-img.com/v1/tradingview/advanced-chart/storage"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    symbol= f"BINANCE:{chain}USDT"
    params = {
        "symbol": symbol,
        "studies": studies or ["MACD", "CCI:10,close"],
        "interval": interval,
        "theme": theme
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['url']
    else:
        return {"error": response.status_code, "message": response.text}

# Example usage:
api_key = "vnDrOf3wlruCCHf4b0jy8hcdqwYzjHc5MBQww6Ad"
chart_data = get_chart_data(api_key, "SOL")
print(chart_data)
