import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "GROQ")

    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        "llama-3.3-70b-versatile"
    )
    DB_HOST = os.getenv("DB_HOST", "localhost")

    DB_PORT = int(os.getenv("DB_PORT", "3306"))

    DB_NAME = os.getenv("DB_NAME", "aibes")

    DB_USER = os.getenv("DB_USER")

    DB_PASSWORD = os.getenv("DB_PASSWORD")
    
    
print("GROQ_API_KEY =", Config.GROQ_API_KEY)
print("LLM_PROVIDER =", Config.LLM_PROVIDER)    