
def ask_human_feedback(state):
    symbol = state.get("symbol")
    price = state.get("price")
    reason = state.get("reason")
    print(f"\n[GPT Reasoning] → {reason}\n")
    print(f"[HUMAN INPUT REQUIRED] Confirm order for {symbol} at ₹{price:.2f}? (yes/no)")
    feedback = input("Your input: ").strip().lower()
    state["feedback"] = feedback
    if feedback == "yes":
        state["order_confirmed"] = True
    else:
        state["order_confirmed"] = False
        state["result"] = "Order cancelled by user."
    return state
