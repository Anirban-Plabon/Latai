from langchain_core.messages import SystemMessage, AIMessage
from agent.state import AgentState
from agent.nodes import skill_path, extract_text, safe_llm_stream
from services.llm import get_llm
from services.session import session


async def chat_node(state: AgentState) -> dict:
    """General chat and coding assistant node. Streams response to TUI."""
    messages = state["messages"]

    skill_text = skill_path("chat_skill.md").read_text()
    llm = get_llm(session.provider, session.model_name)

    prompt = [SystemMessage(content=skill_text), *messages]

    accumulated = ""
    async for chunk in safe_llm_stream(llm, prompt):
        accumulated += extract_text(chunk)

    return {"messages": [AIMessage(content=accumulated)]}
