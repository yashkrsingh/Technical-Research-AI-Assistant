class LLMConstants:
    GPT_GENERAL_MODEL = "openai/gpt-oss-120b:free"
    OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
    OPENAI_DEFAULT_HEADERS = {"Content-Type": "application/json"}
    OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"

    DEFAULT_HYPERPARAMETERS = {
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 8000,
        "stream": False,
    }


class DbConstants:
    SUPABASE_CONNECTION_STRING = "SUPABASE_CONNECTION_STRING"
    SCHEMA = "public"


class MessageConstants:
    WORKING_MEMORY_MESSAGE_LIMIT = 30