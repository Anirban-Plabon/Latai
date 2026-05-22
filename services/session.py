from typing import List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from utils.config import get_default_provider, get_default_model


class Session:
    def __init__(self):
        self.provider: str = get_default_provider()
        self.model_name: str = get_default_model()
        self.messages: List[BaseMessage] = []

    def set_model(self, provider: str, model_name: str) -> None:
        self.provider = provider
        self.model_name = model_name

    def add_user_message(self, content: str) -> None:
        self.messages.append(HumanMessage(content=content))

    def add_ai_message(self, content: str) -> None:
        self.messages.append(AIMessage(content=content))

    def get_messages(self) -> List[BaseMessage]:
        return self.messages

    def clear_messages(self) -> None:
        self.messages = []


session = Session()
