from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from services.llm import get_llm
from services.session import session

async def llm_node(state: AgentState):
    llm = get_llm(session.provider, session.model_name)
    async for chunk in llm.astream(state["messages"]):
        yield {"messages": [chunk]}

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("llm_node", llm_node)
    workflow.add_edge(START, "llm_node")
    workflow.add_edge("llm_node", END)
    return workflow.compile()

graph = build_graph()
