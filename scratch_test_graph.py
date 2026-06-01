import asyncio
from agent.graph import graph
from services.session import session
from langchain_core.messages import HumanMessage

async def run_test(prompt):
    session.provider = "gemini" 
    session.model_name = "gemini-2.5-flash"
    
    print(f"\n--- Testing prompt: '{prompt}' ---")
    state = {"messages": [HumanMessage(content=prompt)]}
    
    try:
        async for s in graph.astream(state):
            for k, v in s.items():
                print(f"Node: {k}")
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        if kk == 'messages':
                            continue
                        print(f"  {kk}: {vv}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    await run_test("Hello, how are you today?")
    await run_test("Write a script to reverse the string 'hello world' and print it.")

if __name__ == "__main__":
    asyncio.run(main())
