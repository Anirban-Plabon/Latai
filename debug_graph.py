import asyncio
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from loguru import logger

# Disable loguru output for cleaner script output
logger.remove()

load_dotenv()

async def debug():
    from agent.graph import graph
    from services.session import session
    
    # Ensure mock provider is used
    session.set_model("mock", "test")
    
    state = {"messages": [HumanMessage(content="hi")]}
    
    print("--- Testing stream_mode='updates' ---")
    async for update in graph.astream(state, stream_mode="updates"):
        print(f"Update: {update}")
        if "llm_node" in update:
            chunk = update["llm_node"]["messages"][0]
            print(f"  Content Type: {type(chunk.content)}")
            print(f"  Content: {repr(chunk.content)}")

    print("\n--- Testing stream_mode='messages' ---")
    async for msg, metadata in graph.astream(state, stream_mode="messages"):
        print(f"Message: {type(msg)}")
        print(f"  Content: {repr(msg.content)}")
        print(f"  Metadata: {metadata}")

if __name__ == "__main__":
    asyncio.run(debug())
