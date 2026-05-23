from textual.message import Message


class StatusUpdate(Message):
    """Fired by any component to push a line into the status panel."""

    CATEGORY_COLORS: dict[str, str] = {
        "agent": "#a78bfa",
        "tool": "#22d3ee",
        "plan": "#fbbf24",
        "todo": "#60a5fa",
        "done": "#3fb950",
        "error": "#f85149",
    }

    def __init__(self, category: str, text: str) -> None:
        super().__init__()
        self.category = category
        self.text = text
