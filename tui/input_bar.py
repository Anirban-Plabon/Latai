from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Input, Static, Button

class InputBar(Container):
    def compose(self) -> ComposeResult:
        with Horizontal(classes="rd-row"):
            yield Static("> ", classes="rd-prefix")
            yield Input(
                placeholder="Type a message or command (e.g., /model, /ask)...",
                id="chat-input",
            )
            yield Button("[⌘P]", id="cmd-menu-btn")

    def focus_input(self) -> None:
        self.query_one(Input).focus()


