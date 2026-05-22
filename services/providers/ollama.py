from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel


def get_model(model_name: str, base_url: str) -> BaseChatModel:
    api_base = f"{base_url}/v1"
    return ChatOpenAI(
        model=model_name,
        openai_api_key="ollama",
        openai_api_base=api_base,
    )
