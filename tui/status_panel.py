from datetime import datetime

from textual.containers import ScrollableContainer, Vertical
from textual.app import ComposeResult
from textual.widgets import Static, OptionList
from textual import on
from textual.widgets.option_list import Option
from tui.command_menu import AVAILABLE_COMMANDS

from tui.status_event import StatusUpdate


MAX_ENTRIES = 200


class StatusPanel(Vertical):
    """Right-column execution monitor. Auto-shows on activity, auto-hides when idle."""

    DEFAULT_CSS = """
    StatusPanel {
        width: 1fr;
        height: 100%;
        background: $background;
        padding: 0;
    }

    .status-header {
        height: 1;
        background: $surface;
        color: $accent;
        text-style: bold;
        padding: 0 1;
    }

    .status-log {
        height: 1fr;
        padding: 0 1;
        overflow-y: scroll;
        scrollbar-size-vertical: 1;
        scrollbar-color: $surface-lighten-2;
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
        with Vertical(id="monitor-view"):
            yield Static(" ◈ Execution Monitor", classes="status-header")
            yield ScrollableContainer(classes="status-log", id="status-log")
        with Vertical(id="inline-commands-view"):
            yield Static(" ◈ Available Commands", classes="status-header")
            yield OptionList(id="inline-commands-list")
            yield Static("", id="inline-command-desc")

    def _populate_commands(self) -> None:
        ol = self.query_one("#inline-commands-list", OptionList)
        for cmd, desc in AVAILABLE_COMMANDS:
            ol.add_option(Option(cmd, id=f"cmd_{cmd.strip('/')}"))

    def show_inline_commands(self) -> None:
        self.query_one("#inline-commands-view").styles.display = "block"
        if not self.query_one("#inline-commands-list", OptionList).option_count:
            self._populate_commands()

    def hide_inline_commands(self) -> None:
        self.query_one("#inline-commands-view").styles.display = "none"

    def navigate_commands(self, direction: str) -> str | None:
        ol = self.query_one("#inline-commands-list", OptionList)
        if not ol.option_count:
            return None
            
        current = ol.highlighted
        if current is None:
            current = 0
        else:
            if direction == "down":
                current = (current + 1) % ol.option_count
            elif direction == "up":
                current = (current - 1) % ol.option_count
                
        ol.highlighted = current
        try:
            return str(ol.get_option_at_index(current).prompt)
        except Exception:
            return None

    @on(OptionList.OptionHighlighted, "#inline-commands-list")
    def on_command_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        try:
            cmd = str(event.option.prompt)
            desc = next((d for c, d in AVAILABLE_COMMANDS if c == cmd), "")
            self.query_one("#inline-command-desc", Static).update(desc)
        except Exception:
            pass

    def post_status(self, category: str, text: str) -> None:
        """Append a timestamped status entry."""
        color = StatusUpdate.CATEGORY_COLORS.get(category, "$text-muted")
        timestamp = datetime.now().strftime("%H:%M:%S")
        icon = _category_icon(category)
        
        if category == "todo":
            markup = f"[{color}]{icon} {text}[/]"
        else:
            markup = f"[$surface-lighten-2]{timestamp}[/] [{color}]{icon} {text}[/]"

        log = self.query_one("#status-log", ScrollableContainer)

        classes = "status-entry"
        if category == "todo":
            classes += " todo-item"

        entry = Static(markup, classes=classes)
        if category == "todo":
            entry.todo_text = text
            entry.todo_timestamp = timestamp

        log.mount(entry)
        self._entry_count += 1

        if self._entry_count > MAX_ENTRIES:
            self._trim_oldest(log)

        log.call_after_refresh(log.scroll_end, animate=False)

    def mark_todos_completed(self) -> None:
        """Strike through all todo entries in the execution monitor and tick them."""
        log = self.query_one("#status-log", ScrollableContainer)
        color = StatusUpdate.CATEGORY_COLORS.get("done", "$success")
        icon = _category_icon("done")
        for child in log.query(".todo-item"):
            if hasattr(child, "todo_text"):
                markup = f"[{color}]{icon} [s]{child.todo_text}[/s]"
                child.update(markup)

    def show_agent_loader(self, node_name: str) -> None:
        """Shows a loader for the current agent node in the status panel."""
        log = self.query_one("#status-log", ScrollableContainer)
        from res.ui.loaders import ThinkingIndicator
        
        # Stop any existing loader
        for child in log.query(ThinkingIndicator):
            if hasattr(child, "stop"):
                child.stop()
            if hasattr(child, "mark_done"):
                try:
                    child.mark_done()
                except Exception:
                    pass

        # Map nodes to loaders and user-facing labels
        node_loaders = {
            "root_node": ("loader2", "Working: Root"),
            "planner_node": ("loader2", "Working: Planner"),
            "generator_node": ("loader2", "Working: Generator"),
            "write_file_node": ("loader2", "Working: Write File"),
            "chat_node": ("loader2", "Working: Chat"),
        }
        loader_name, label = node_loaders.get(node_name, ("loader2", f"Working: {node_name}"))

        # Mount new loader
        loader = ThinkingIndicator(loader_name=loader_name, label=label)
        log.mount(loader)
        self._entry_count += 1
        
        if self._entry_count > MAX_ENTRIES:
            self._trim_oldest(log)
            
        log.call_after_refresh(log.scroll_end, animate=False)

    def mark_agent_done(self) -> None:
        log = self.query_one("#status-log", ScrollableContainer)
        from res.ui.loaders import ThinkingIndicator
        
        for child in log.query(ThinkingIndicator):
            if hasattr(child, "stop"):
                child.stop()
            if hasattr(child, "mark_done"):
                try:
                    child.mark_done()
                except Exception:
                    pass

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
