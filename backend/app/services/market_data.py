import httpx
from app.config import settings

BASE_URL = "https://api.twelvedata.com"

RANGE_TO_PARAMS = {
    "1M": ("1day", 22),
    "3M": ("1day", 66),
    "6M": ("1day", 132),
    "1Y": ("1day", 252),
    "2Y": ("1day", 260),
    "5Y": ("1day", 500),
}

def get_current_price(ticker: str) -> float:
    resp = httpx.get(f"{BASE_URL}/price", params={
        "symbol": ticker, 
        "apikey": settings.MARKET_API_KEY}
        )

    resp.raise_for_status()
    data = resp.json()
    if "price" not in data:
        raise ValueError(f"Price not found for ticker {ticker}")
    return float(data["price"])

def get_historical_prices(ticker: str, interval: str = '1day', outputsize: int = 30) -> list[dict]:
    resp = httpx.get(f"{BASE_URL}/time_series", params={
        "symbol": ticker,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": settings.MARKET_API_KEY
    })

    resp.raise_for_status()
    data = resp.json()
    if "values" not in data:
        raise ValueError(f"Historical prices not found for ticker {ticker}")
    return data["values"]

def get_asset_info(ticker: str) -> dict:
    resp = httpx.get(f"{BASE_URL}/symbol_search", params={
        "symbol": ticker,
        "apikey": settings.MARKET_API_KEY
    })
    resp.raise_for_status()
    data = resp.json()
    if "data" not in data or len(data["data"]) == 0:
        raise ValueError(f"Asset info not found for ticker {ticker}")
    return data["data"][0]

def get_historical_range(ticker: str, range_key: str) -> list[dict]:
    if range_key not in RANGE_TO_PARAMS:
        raise ValueError(f"Unsupported range: {range_key}")
    interval, outputsize = RANGE_TO_PARAMS[range_key]
    return get_historical_prices(ticker, interval=interval, outputsize=outputsize)

