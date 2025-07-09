from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import json
from utils.env import OPENAI_MODEL


def reason_check(state):
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0)
    stock_info = state.get("stock_info", {})
    user_query = state["input"]
    context = f"""
        User Input: "{user_query}"

        Stock Metadata:
        - Company: {stock_info.get('companyName')}
        - Industry: {stock_info.get('industry')}
        - Sector: {stock_info.get('sector')}
        - Market Cap: {stock_info.get('marketCap')}
        - P/E Ratio: {stock_info.get('pe')}
        - Current Price: ₹{stock_info.get('price')}
        - 52 Week High: ₹{stock_info.get('52weekHigh')}
        - 52 Week Low: ₹{stock_info.get('52weekLow')}
    """
    # print(f"context::\n{context}")
    prompt = f"""
        You are a financial analyst AI.
        Given the user's request and the stock's metadata below, answer:

        1. What is the likely investment reasoning: fundamental value, price action, sentiment/news, or hype?
        2. Analyze the user's query as an LLM Prompt:
           - Is it specific and context-aware?
           - Does it include intent, timeframe, or price expectations?
           - Rate the prompt quality for AI-driven decision making.

        Return JSON with 'reasoning' and 'prompt_quality'.
        {context}
    """
    chat_messages = [
        SystemMessage(content="Answer in JSON."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(chat_messages)
    try:
        parsed = json.loads(response.content.strip())
        # print(f"parsed::\n{parsed}")
        state["reason"] = parsed.get("reasoning")
        state["prompt_strategy"] = parsed.get("prompt_quality")
    except Exception as e:
        print("reason_check parse error:", e)
        state["reason"] = response.content
        state["prompt_strategy"] = ""

    return state
