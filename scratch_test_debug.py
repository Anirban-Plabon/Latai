import asyncio
from agent.graph import graph
from langchain_core.messages import HumanMessage

async def main():
    from services.session import session
    session.provider = "gemini" 
    session.model_name = "gemini-2.5-flash"
    
    state = {"messages": [HumanMessage(content="Calculate 2+2")]}
    
    async for event_type, payload in graph.astream(state, stream_mode=["messages", "debug"]):
        if event_type == "debug":
            if isinstance(payload, dict) and payload.get("type") == "task":
                print(f"Task Started: {payload.get('payload', {}).get('name')}")
        elif event_type == "messages":
            msg, metadata = payload
            print(f"Message from {metadata.get('langgraph_node')}")

if __name__ == "__main__":
    asyncio.run(main())
