from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessageChunk, BaseMessage
from langchain_core.outputs import ChatGenerationChunk, ChatResult
from typing import Any, AsyncIterator, List, Optional
import asyncio

class MockChatModel(BaseChatModel):
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        return ChatResult(generations=[])

    async def _astream(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> AsyncIterator[ChatGenerationChunk]:
        text = "Hello! I am a mock AI. This is a streaming response to test the TUI."
        for word in text.split():
            chunk = ChatGenerationChunk(message=AIMessageChunk(content=word + " "))
            yield chunk
            await asyncio.sleep(0.05)

    @property
    def _llm_type(self) -> str:
        return "mock"

def get_model(model_name: str, api_key: str) -> BaseChatModel:
    return MockChatModel()
