from langchain_core.language_models.chat_models import BaseChatModel
from services.llm_factory import get_chat_model

def get_llm(provider: str, model_name: str) -> BaseChatModel:
    """Legacy wrapper for the new LLM factory."""
    return get_chat_model(provider, model_name)
