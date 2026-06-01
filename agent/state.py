from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    route: str
    confidence: str
    plan_todos: list[str]
    generated_code: str
    file_writes: list[dict]
    diff_text: str
    file_exists: bool
