import re

from langchain_core.messages import SystemMessage
from loguru import logger

from agent.state import AgentState
from agent.nodes import skill_path, extract_text, safe_llm_stream
from services.llm import get_llm
from services.session import session


async def planner_node(state: AgentState) -> dict:
    """Decompose & plan node. Streams plan into chat, emits plan_todos."""
    messages = state["messages"]

    skill_text = skill_path("planner_skill.md").read_text()
    llm = get_llm(session.provider, session.model_name)

    prompt = [SystemMessage(content=skill_text), *messages]

    accumulated = ""
    async for chunk in safe_llm_stream(llm, prompt):
        accumulated += extract_text(chunk)

    plan_todos = _extract_steps(accumulated)
    logger.debug(f"planner_node: {len(plan_todos)} todos")

    return {"plan_todos": plan_todos}


def _extract_steps(text: str) -> list[str]:
    steps_block = re.search(
        r"##\s*Steps?\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    block = steps_block.group(1) if steps_block else text

    steps = re.findall(r"^\s*\d+\.\s+(.+)", block, re.MULTILINE)
    if not steps:
        steps = re.findall(r"^\s*[-*]\s+(.+)", block, re.MULTILINE)

    return [s.strip() for s in steps if s.strip()]
