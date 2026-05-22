from textual.app import ComposeResult
from textual.widgets import Static


class CustomHeader(Static):
    """The application's custom header bar."""

    def compose(self) -> ComposeResult:
        yield Static("craftChat", id="app-title")
