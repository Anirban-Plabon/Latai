from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Markdown, Static
from textual.reactive import reactive

class ChatMessage(Container):
    content = reactive("")

    def __init__(self, role: str, content: str, id: str | None = None) -> None:
        super().__init__(id=id)
        self.role = role
        self.content = content

    def compose(self) -> ComposeResult:
        display_role = "You" if self.role == "user" else "AI"
        
        with Horizontal(classes="message-row"):
            yield Static(f"{display_role}: ", classes="message-role")
            yield Markdown(self.content, classes="message-content")

    def watch_content(self, new_content: str) -> None:
        try:
            markdown_widget = self.query_one(Markdown)
            markdown_widget.update(new_content)
        except Exception:
            pass
