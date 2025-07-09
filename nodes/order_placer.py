def place_order(symbol: str, price: float) -> str:
    return f"Order Placed for {symbol} at ₹{price:.2f}"


def execute_order(state):
    if not state.get("order_confirmed"):
        state["result"] = "Order not confirmed."
        return state
    symbol = state.get("symbol")
    price = state.get("price")
    state["result"] = place_order(symbol, price)
    state["order_placed"] = True
    return state
