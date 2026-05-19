from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel

def get_model(model_name: str, api_key: str) -> BaseChatModel:
    return ChatAnthropic(model=model_name, anthropic_api_key=api_key)
