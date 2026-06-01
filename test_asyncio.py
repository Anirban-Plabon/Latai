import asyncio
from agent.graph import graph
from langchain_core.messages import HumanMessage

async def test():
    state = {"messages": [HumanMessage(content="Hello")]}
    print("starting astream")
    async for msg, metadata in graph.astream(state, stream_mode="messages"):
        print("got chunk")
        break

asyncio.run(test())
