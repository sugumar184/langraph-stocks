from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from nodes.extract_stock import extract_stock
from nodes.reason_check import reason_check
from nodes.human_feedback import ask_human_feedback
from nodes.order_placer import execute_order
from nodes.lookup_price import lookup_price
from nodes.risk_check import risk_check
from nodes.finalize import finalize
from typing import TypedDict, Optional
from langchain_core.runnables import RunnableLambda

load_dotenv("configs/.env")


# define state
class StockState(TypedDict):
    input: str
    symbol: Optional[str]
    price: Optional[str]
    order_confirmed: Optional[str]
    order_placed: Optional[str]
    feedback: Optional[str]
    tool: Optional[str]
    result: Optional[str]
    retry_count: int
    reason: Optional[str]
    prompt_strategy: Optional[str]
    stock_info: Optional[dict]


# ---- Graph definition ----
def build_graph():
    graph = StateGraph(StockState)

    # Nodes
    graph.add_node("extract_stock", RunnableLambda(extract_stock))
    graph.add_node("lookup_price", RunnableLambda(lookup_price))
    graph.add_node("reason_check", RunnableLambda(reason_check))
    graph.add_node("ask_feedback", RunnableLambda(ask_human_feedback))
    graph.add_node("place_order", RunnableLambda(execute_order))
    graph.add_node("final", RunnableLambda(finalize))

    # Flow
    graph.set_entry_point("extract_stock")
    graph.add_edge("extract_stock", "lookup_price")
    graph.add_edge("lookup_price", "reason_check")
    graph.add_conditional_edges("reason_check", risk_check, {
        "lookup_price": "lookup_price",
        "ask_feedback": "ask_feedback",
        END: "final"
    })
    graph.add_conditional_edges("ask_feedback", lambda s: "place_order" if s.get("order_confirmed") else END, {
        "place_order": "place_order",
        END: "final"
    })
    graph.add_edge("place_order", "final")

    # Compile
    app = graph.compile()
    return app


if __name__ == "__main__":
    print("🚀 Starting Stock Trading Agent")
    user_input = input("🧠 Enter your Nifty Index symbol\n> ")

    graph_app = build_graph()

    # Initial input state
    input_state = {
        "input": user_input,
        "symbol": None,
        "price": None,
        "order_confirmed": None,
        "order_placed": None,
        "feedback": None,
        "tool": None,
        "result": None,
        "retry_count": 0,
        "reason": None,
        "prompt_strategy:": None
    }

    final_state = graph_app.invoke(input_state)

    print("\n✅ Final Result:")
    print(final_state.get("result") or final_state.get("error"))
