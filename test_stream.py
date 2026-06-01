import asyncio
from agent.graph import phase1_graph
from langchain_core.messages import HumanMessage

async def main():
    async for chunk in phase1_graph.astream(
        {"messages": [HumanMessage(content="hello")]},
        stream_mode=["messages", "updates", "debug"],
    ):
        print(chunk[0], chunk[1].keys() if isinstance(chunk[1], dict) else chunk[1])

asyncio.run(main())
