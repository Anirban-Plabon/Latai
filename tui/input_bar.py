from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, TextArea
from textual.message import Message
from textual.binding import Binding

class ChatInput(TextArea):
    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    BINDINGS = [
        Binding("enter", "submit", "Submit message", show=False, priority=True),
        Binding("shift+enter", "newline", "Add newline", show=False, priority=True),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_line_numbers = False

    def action_submit(self) -> None:
        self.post_message(self.Submitted(self.text))

    def action_newline(self) -> None:
        self.insert("\n")

from textual.widgets import OptionList

class InputBar(Container):
    def compose(self) -> ComposeResult:
        with Horizontal(classes="rd-row"):
            yield Static("❯ ", classes="rd-prefix")
            yield ChatInput(
                id="chat-input",
            )
            yield OptionList(id="approval-options")
            yield Button("[⌘P]", id="cmd-menu-btn")

    def focus_input(self) -> None:
        self.query_one(ChatInput).focus()

    def show_approval(self, options: list[str]) -> None:
        chat_input = self.query_one(ChatInput)
        option_list = self.query_one("#approval-options", OptionList)
        chat_input.display = False
        option_list.clear_options()
        option_list.add_options(options)
        option_list.display = True
        option_list.focus()

    def hide_approval(self) -> None:
        chat_input = self.query_one(ChatInput)
        option_list = self.query_one("#approval-options", OptionList)
        option_list.display = False
        chat_input.display = True
        chat_input.focus()
