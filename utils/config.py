import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_api_key(provider: str) -> Optional[str]:
    """Retrieve the API key for a given provider from environment variables."""
    key_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "gemini": "GOOGLE_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    env_var = key_map.get(provider)
    if not env_var:
        return None
    return os.getenv(env_var)
