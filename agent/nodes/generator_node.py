import difflib
import os
import re

from langchain_core.messages import SystemMessage
from loguru import logger

from agent.state import AgentState
from agent.nodes import skill_path, extract_text, safe_llm_stream
from services.llm import get_llm
from services.session import session


async def generator_node(state: AgentState) -> dict:
    """Generator Node. Generates or patches code strictly following the provided skill instructions."""
    messages = state["messages"]
    plan_todos = state.get("plan_todos", [])

    skill_text = skill_path("generator_skill.md").read_text()
    llm = get_llm(session.provider, session.model_name)

    plan_section = ""
    if plan_todos:
        steps = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(plan_todos))
        plan_section = f"\n\n## Execution Plan\n{steps}"

    prompt = [SystemMessage(content=skill_text + plan_section), *messages]

    accumulated = ""
    async for chunk in safe_llm_stream(llm, prompt):
        accumulated += extract_text(chunk)

    file_writes = _extract_files(accumulated)
    generated_code = file_writes[0].get("content", accumulated) if file_writes else accumulated
    diff_text = ""
    file_exists = False

    if file_writes:
        first_path = file_writes[0].get("path", "")
        first_content = file_writes[0].get("content", "")
        full_path = os.path.join(session.cwd, first_path)

        if os.path.exists(full_path):
            file_exists = True
            try:
                existing = open(full_path).read()
                diff_lines = difflib.unified_diff(
                    existing.splitlines(keepends=True),
                    first_content.splitlines(keepends=True),
                    fromfile=f"a/{first_path}",
                    tofile=f"b/{first_path}",
                    lineterm="",
                )
                diff_text = "".join(diff_lines)
            except Exception as exc:
                logger.warning(f"generator_node: diff failed: {exc}")

        session.pending_state = {
            "code_filename": first_path,
            "file_writes": file_writes,
            "generated_code": generated_code,
            "diff_text": diff_text,
            "file_exists": file_exists,
            "syntax_issues": [],
        }

    logger.debug(f"generator_node: {len(file_writes)} file(s), file_exists={file_exists}")

    return {
        "generated_code": generated_code,
        "file_writes": file_writes,
        "diff_text": diff_text,
        "file_exists": file_exists,
    }


def _extract_files(text: str) -> list[dict]:
    """Parse ---FILE: path--- blocks from generator output."""
    pattern = r"---FILE:\s*([^\n]+?)\s*---\s*\n```[^\n]*\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return [{"path": p.strip(), "content": c.strip()} for p, c in matches]

    code_match = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
    if code_match:
        return [{"path": "output.py", "content": code_match.group(1).strip()}]

    return []
