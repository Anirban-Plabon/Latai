import json
import re

from langchain_core.messages import SystemMessage, HumanMessage
from loguru import logger

from agent.state import AgentState
from agent.nodes import skill_path, extract_text, safe_llm_call
from services.llm import get_llm
from services.session import session


async def root_node(state: AgentState) -> dict:
    """Intent Classifier Node. Analyzes the user's input and classifies their intent."""
    if state.get("route") in ("new_task", "edit_request", "skip_plan"):
        logger.debug(f"root_node: route already set to {state['route']}. Bypassing classification.")
        return {"route": state["route"], "confidence": state.get("confidence", "high")}

    messages = state["messages"]
    last_human = next(
        (m for m in reversed(messages) if isinstance(m, HumanMessage)), None
    )
    user_text = extract_text(last_human) if last_human else ""

    skill_text = skill_path("root_skill.md").read_text()
    llm = get_llm(session.provider, session.model_name)

    prompt = [
        SystemMessage(content=skill_text),
        HumanMessage(content=user_text),
    ]

    response = await safe_llm_call(llm, prompt, tags=["nostream"])
    raw = extract_text(response)

    route = "skip_plan"
    confidence = "low"

    try:
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        parsed = json.loads(clean)
        route = parsed.get("route", "skip_plan")
        confidence = parsed.get("confidence", "low")
    except Exception:
        logger.warning(f"root_node: failed to parse JSON: {raw!r}")

    logger.debug(f"root_node: route={route} confidence={confidence}")
    return {"route": route, "confidence": confidence}
