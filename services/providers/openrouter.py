from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

def get_model(model_name: str, api_key: str) -> BaseChatModel:
    return ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1"
    )
