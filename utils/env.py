# utils/env.py
from dotenv import load_dotenv
import os

load_dotenv("configs/.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
