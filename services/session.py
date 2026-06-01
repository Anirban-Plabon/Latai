from typing import List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from utils.config import get_default_provider, get_default_model


class Session:
    def __init__(self) -> None:
        self.provider: str = get_default_provider()
        self.model_name: str = get_default_model()
        self.messages: List[BaseMessage] = []
        self.total_tokens: int = 0
        self.is_terminal_mode: bool = False
        self.is_file_panel_open: bool = False
        self.current_file_path: str | None = None
        self.is_editing: bool = False
        import os
        self.cwd: str = os.getcwd()
        # Single approval gate: set by generator_node, cleared after user responds
        self.pending_state: dict | None = None

    def set_model(self, provider: str, model_name: str) -> None:
        self.provider = provider
        self.model_name = model_name

    def add_tokens(self, count: int) -> None:
        self.total_tokens += count

    def add_user_message(self, content: str) -> None:
        self.messages.append(HumanMessage(content=content))

    def add_ai_message(self, content: str) -> None:
        self.messages.append(AIMessage(content=content))

    def get_messages(self) -> List[BaseMessage]:
        return self.messages

    def clear_messages(self) -> None:
        self.messages = []


session = Session()
