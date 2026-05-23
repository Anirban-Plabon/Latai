from datetime import datetime

from textual.containers import ScrollableContainer, Vertical
from textual.app import ComposeResult
from textual.widgets import Static

from tui.status_event import StatusUpdate


MAX_ENTRIES = 200


class StatusPanel(Vertical):
    """Right-column execution monitor. Auto-shows on activity, auto-hides when idle."""

    DEFAULT_CSS = """
    StatusPanel {
        width: 1fr;
        height: 100%;
        background: #0d1117;
        padding: 0;
    }

    .status-header {
        height: 1;
        background: #161b22;
        color: #a78bfa;
        text-style: bold;
        padding: 0 1;
    }

    .status-log {
        height: 1fr;
        padding: 0 1;
        overflow-y: scroll;
        scrollbar-size-vertical: 1;
        scrollbar-color: #30363d;
        scrollbar-background: transparent;
    }

    .status-entry {
        height: auto;
        padding: 0;
        margin: 0;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._entry_count: int = 0

    def compose(self) -> ComposeResult:
        yield Static(" ◈ Execution Monitor", classes="status-header")
        yield ScrollableContainer(classes="status-log", id="status-log")

    def post_status(self, category: str, text: str) -> None:
        """Append a timestamped status entry."""
        color = StatusUpdate.CATEGORY_COLORS.get(category, "#8b949e")
        timestamp = datetime.now().strftime("%H:%M:%S")
        icon = _category_icon(category)
        markup = f"[#6e7681]{timestamp}[/] [{color}]{icon} {text}[/]"

        log = self.query_one("#status-log", ScrollableContainer)

        entry = Static(markup, classes="status-entry")
        log.mount(entry)
        self._entry_count += 1

        if self._entry_count > MAX_ENTRIES:
            self._trim_oldest(log)

        log.call_after_refresh(log.scroll_end, animate=False)

    def _trim_oldest(self, log: ScrollableContainer) -> None:
        children = list(log.children)
        remove_count = self._entry_count - MAX_ENTRIES
        for child in children[:remove_count]:
            child.remove()
        self._entry_count = MAX_ENTRIES


def _category_icon(category: str) -> str:
    icons: dict[str, str] = {
        "agent": "⟳",
        "tool": "⚙",
        "plan": "◆",
        "todo": "○",
        "done": "✓",
        "error": "✗",
    }
    return icons.get(category, "·")
