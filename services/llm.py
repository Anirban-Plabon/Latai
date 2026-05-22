from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel
from utils.config import get_api_key, get_base_url, get_default_key_name
from services.providers import anthropic, gemini, mock, ollama, openai, openrouter


def get_llm(provider: str, model_name: str) -> Optional[BaseChatModel]:
    """Factory to return the appropriate LangChain ChatModel instance."""
    if provider == "mock":
        return mock.get_model(model_name, "")

    match provider:
        case "gemini":
            key_name = get_default_key_name(provider) or "default"
            api_key = get_api_key(provider, key_name)
            if not api_key:
                raise ValueError(f"API key for {provider} not found in config.yaml")
            return gemini.get_model(model_name, api_key)
        case "openai":
            key_name = get_default_key_name(provider) or "default"
            api_key = get_api_key(provider, key_name)
            if not api_key:
                raise ValueError(f"API key for {provider} not found in config.yaml")
            return openai.get_model(model_name, api_key)
        case "anthropic":
            key_name = get_default_key_name(provider) or "default"
            api_key = get_api_key(provider, key_name)
            if not api_key:
                raise ValueError(f"API key for {provider} not found in config.yaml")
            return anthropic.get_model(model_name, api_key)
        case "openrouter":
            key_name = get_default_key_name(provider)
            if key_name is None:
                raise ValueError(f"No API keys configured for {provider} in config.yaml")
            api_key = get_api_key(provider, key_name)
            if not api_key:
                raise ValueError(f"API key for {provider} not found in config.yaml")
            return openrouter.get_model(model_name, api_key)
        case "ollama":
            base_url = get_base_url(provider)
            if not base_url:
                raise ValueError(f"base_url for {provider} not found in config.yaml")
            return ollama.get_model(model_name, base_url)
        case _:
            raise ValueError(f"Unsupported provider: {provider}")
