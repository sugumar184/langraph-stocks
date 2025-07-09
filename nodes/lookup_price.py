from jugaad_data.nse import NSELive


def lookup_price(state):
    symbol = state.get('symbol')
    price = get_live_price(symbol)
    state['price'] = price
    return state


def get_live_price(symbol: str) -> float:
    n = NSELive()
    try:
        q = n.stock_quote(symbol.upper())
        output = q.get('priceInfo', {}).get('lastPrice', None)
        if output is not None:
            return float(output)
        return -1.0
    except Exception as e:
        print(f'Error: {e}')
        return -1.0
