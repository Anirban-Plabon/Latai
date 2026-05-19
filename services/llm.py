from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel
from utils.config import get_api_key
from services.providers import gemini, openai, anthropic, openrouter, mock

def get_llm(provider: str, model_name: str) -> Optional[BaseChatModel]:
    """Factory to return the appropriate LangChain ChatModel instance."""
    # 1. Handle mock provider immediately
    if provider == "mock":
        return mock.get_model(model_name, "")
        
    # 2. Fetch the API key using the original provider string
    api_key = get_api_key(provider)
    
    # Fallback: If "gemini" was passed but your config looks for "google" (or vice versa)
    if not api_key and provider in ["google", "gemini"]:
        fallback_provider = "gemini" if provider == "google" else "google"
        api_key = get_api_key(fallback_provider)

    if not api_key:
        raise ValueError(
            f"API key for {provider} not found. "
            f"Ensure load_dotenv() is called at your app's entry point and your .env is set up."
        )

    # 3. Match the provider (supporting both "google" and "gemini" naming conventions)
    match provider:
        case "gemini" | "google":
            return gemini.get_model(model_name, api_key)
        case "openai":
            return openai.get_model(model_name, api_key)
        case "anthropic":
            return anthropic.get_model(model_name, api_key)
        case "openrouter":
            return openrouter.get_model(model_name, api_key)
        case _:
            raise ValueError(f"Unsupported provider: {provider}")