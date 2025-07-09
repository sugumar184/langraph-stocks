from jugaad_data.nse import NSELive
import json


def read_nifty_symbol():
    with open('nifty_index.json') as f:
        known_symbols = json.load(f)
        return known_symbols


def extract_stock(state):
    # print(state)
    text = state["input"].upper()
    known_symbols = read_nifty_symbol()
    try:
        matched = [sym for sym in known_symbols if sym in text]
        if not matched:
            state["result"] = "Could not identify any known stock symbol in your request."
            return state
        symbol = matched[0]
        n = NSELive()
        q = n.stock_quote(symbol)
        # symbol = q.get('info', {}).get('symbol')
        state["symbol"] = symbol
        state["tool"] = "lookup"

        # Store rich metadata into state
        stock_info = {
            "companyName": q.get('info', {}).get('companyName'),
            "industry": q.get('info', {}).get('industry'),
            "sector": q.get('industryInfo', {}).get('sector'),
            "pe": q.get('metadata', {}).get('pdSectorPe'),
            "issuedSize": q.get('securityInfo', {}).get('issuedSize'),
            "price": q.get('priceInfo', {}).get('lastPrice'),
            "52weekHigh": q.get('priceInfo', {}).get('weekHighLow', {}).get('max'),
            "52weekLow": q.get('priceInfo', {}).get('weekHighLow', {}).get('min'),
            "marketCap": q.get('securityInfo', {}).get('issuedSize') * q.get('priceInfo', {}).get('lastPrice'),
        }
        state["stock_info"] = stock_info
        state["price"] = float(stock_info["price"]) if stock_info["price"] else -1.0
        return state
    except Exception as e:
        print("extract_stock error:: ", e)
        state["result"] = "Error retrieving stock data."
        return state
