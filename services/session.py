from typing import List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

class Session:
    def __init__(self):
        self.provider: str = "google"
        self.model_name: str = "gemini-2.5-flash"
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

# Global singleton for the session
session = Session()
