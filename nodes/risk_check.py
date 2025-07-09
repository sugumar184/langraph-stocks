import time
from langgraph.graph import END


def risk_check(state) -> str:
    if state["price"] <= 0:
        if state["retry_count"] < 2:
            state["retry_count"] += 1
            time.sleep(1)
            return "lookup_price"
        else:
            state["result"] = "Could not fetch price after retries."
            return END
    return "ask_feedback"
