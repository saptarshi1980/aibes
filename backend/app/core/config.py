import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    # -----------------------------
    # LLM Configuration
    # -----------------------------

    #LLM_PROVIDER = os.getenv(
       # "LLM_PROVIDER",
        #"HUGGINGFACE"
    #)

    #LLM_MODEL = os.getenv(
      #  "LLM_MODEL",
       # "Qwen/Qwen3-235B-A22B-Instruct-2507"
    #)
    
    LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "OLLAMA"
)

    LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "qwen2.5:7b"    
)

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    HF_API_KEY = os.getenv(
        "HF_API_KEY"
    )

    # -----------------------------
    # Database Configuration
    # -----------------------------

    DB_HOST = os.getenv(
        "DB_HOST",
        "localhost"
    )

    DB_PORT = int(
        os.getenv(
            "DB_PORT",
            "3306"
        )
    )

    DB_NAME = os.getenv(
        "DB_NAME",
        "aibes"
    )

    DB_USER = os.getenv(
        "DB_USER"
    )

    DB_PASSWORD = os.getenv(
        "DB_PASSWORD"
    )