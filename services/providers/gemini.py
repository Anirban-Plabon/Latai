from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

def get_model(model_name: str, api_key: str) -> BaseChatModel:
    return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, streaming=True)
