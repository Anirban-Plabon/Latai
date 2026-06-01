from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Static
from textual.widget import Widget

from tui.custom_markdown import CustomMarkdown


class ChatMessage(Container):
    def __init__(self, role: str, content: str | Widget, id: str | None = None) -> None:
        super().__init__(id=id)
        self.role = role
        self._content_widget = content if isinstance(content, Widget) else None
        self._text = content if isinstance(content, str) else ""
        self._is_streaming = False

    def compose(self) -> ComposeResult:
        if self.role == "user":
            display_role = "You"
        elif self.role == "system":
            display_role = ""
        else:
            display_role = "Latai"

        prefix = f"{display_role}: " if display_role else ""

        with Horizontal(classes="message-row"):
            if prefix:
                yield Static(prefix, classes="message-role")
            if self._content_widget:
                yield self._content_widget
            else:
                yield CustomMarkdown(self._text, classes="message-content")

    def stream_update(self, text: str) -> None:
        """Fast path: update plain Static during streaming — no Markdown lock."""
        if not self._is_streaming:
            self._is_streaming = True
            try:
                md = self.query_one(CustomMarkdown)
                self._stream_static = Static(text, classes="message-content")
                md.display = False
                self.query_one(".message-row").mount(self._stream_static)
            except Exception:
                pass
            return
        try:
            self._stream_static.update(text)
        except Exception:
            pass

    def finalize(self, text: str) -> None:
        """Replace the streaming Static with a fully-rendered CustomMarkdown."""
        self._is_streaming = False
        try:
            static = getattr(self, "_stream_static", None)
            md = self.query_one(CustomMarkdown)
            if static:
                static.remove()
            md.display = True
            self.call_after_refresh(md.update, text)
        except Exception:
            pass

    def set_content(self, text: str) -> None:
        """Non-streaming update (system / user messages)."""
        try:
            md = self.query_one(CustomMarkdown)
            self.call_after_refresh(md.update, text)
        except Exception:
            pass
