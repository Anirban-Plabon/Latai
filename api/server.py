from fastapi import FastAPI, HTTPException
from typing import List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from api.schemas import ProviderOptions, ChatRequest
from api.models_service import get_available_models
from services.llm_factory import get_chat_model

app = FastAPI(title="Latai Chat API")

@app.get("/api/models", response_model=List[ProviderOptions])
async def list_models():
    """Returns a filtered structure of all currently available model options."""
    try:
        return await get_available_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Instantiate the matching LangChain chat model and invoke it with messages."""
    try:
        llm = get_chat_model(request.provider, request.model_id)
    except ValueError as e:
        # E.g. Missing API key or unsupported provider
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to instantiate model: {str(e)}")

    # Convert Pydantic messages to LangChain message objects
    lc_messages = []
    for msg in request.messages:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role in ["ai", "assistant"]:
            lc_messages.append(AIMessage(content=msg.content))
        elif msg.role == "system":
            lc_messages.append(SystemMessage(content=msg.content))
        else:
            # Default to human message for unknown roles
            lc_messages.append(HumanMessage(content=msg.content))
            
    try:
        # We use await llm.ainvoke for async execution
        response = await llm.ainvoke(lc_messages)
        # response.content can be str or list, return string representation for simplicity
        content = response.content
        if isinstance(content, list):
             # handle complex content like blocks
             text_content = ""
             for block in content:
                 if isinstance(block, dict) and block.get("type") == "text":
                     text_content += block.get("text", "")
                 elif isinstance(block, str):
                     text_content += block
             content = text_content

        return {"response": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
