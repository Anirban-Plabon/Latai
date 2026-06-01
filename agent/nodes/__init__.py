from pathlib import Path

from langchain_core.messages import AIMessage
from langchain_core.language_models.chat_models import BaseChatModel


def skill_path(name: str) -> Path:
    """Return absolute path to a skill file."""
    return Path(__file__).resolve().parents[1] / "skills" / name


def extract_text(msg) -> str:
    content = getattr(msg, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            p.get("text", "") if isinstance(p, dict) and p.get("type") == "text" else ""
            for p in content
        )
    return ""


async def safe_llm_call(
    llm: BaseChatModel, messages: list, tags: list[str] | None = None
) -> AIMessage:
    """Invoke LLM, return AIMessage with error info on failure."""
    try:
        config = {"tags": tags} if tags else {}
        return await llm.ainvoke(messages, config=config)
    except Exception as exc:
        return AIMessage(content=f"[LLM Error] {exc}")


async def safe_llm_stream(llm: BaseChatModel, messages: list):
    """Stream from LLM, yield error AIMessage on failure."""
    try:
        async for chunk in llm.astream(messages):
            yield chunk
    except Exception as exc:
        yield AIMessage(content=f"[LLM Error] {exc}")
