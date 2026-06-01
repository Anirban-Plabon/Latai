from textual.message import Message


class StatusUpdate(Message):
    """Fired by any component to push a line into the status panel."""

    CATEGORY_COLORS: dict[str, str] = {
        "agent": "$accent",
        "tool": "$secondary",
        "plan": "$warning",
        "todo": "$primary",
        "done": "$success",
        "error": "$error",
    }

    def __init__(self, category: str, text: str) -> None:
        super().__init__()
        self.category = category
        self.text = text
