import os

class Config:
    PROVIDER = os.environ.get("PROVIDER", "gemini").lower()

    # Gemini API
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_MODEL = "models/chat-bison-001"

    # OpenAI API
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-4o-mini"

    DEFAULT_CURRENCY = "INR"
    MAX_DAYS = 14
    MIN_DAYS = 1
