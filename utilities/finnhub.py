import finnhub
from decouple import config
FINNHUB_KEY = config("FINNHUB_KEY")

def get_latest_ipo(from_date, to_date):
    finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)
    ipo_list = finnhub_client.ipo_calendar(_from=from_date, to=to_date)["ipoCalendar"]
    return ipo_list

def get_latest_insider_transactions(symbol, from_date, to_date):
    import finnhub
    finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)

    insider_transactions = finnhub_client.stock_insider_transactions(symbol, from_date, to_date)["data"]
    return insider_transactions


# content = get_latest_insider_transactions("AAPL", "2025-01-01","2025-02-15")

# content[1]

# -4528 * 19.6