from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ModelOption(BaseModel):
    id: str
    label: str

class ProviderOptions(BaseModel):
    provider: str
    models: List[ModelOption]

class Message(BaseModel):
    role: str = Field(..., description="Role of the sender: 'user', 'ai', or 'system'")
    content: str

class ChatRequest(BaseModel):
    provider: str
    model_id: str
    messages: List[Message]
