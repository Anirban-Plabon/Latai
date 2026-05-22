import os
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static
from services.session import session


class CustomFooter(Horizontal):
    """The application's custom footer bar showing workspace info, selected model, and token usage."""

    def compose(self) -> ComposeResult:
        yield Static(f"Workspace: {os.getcwd()}", id="footer-workspace")
        yield Static(f"/model {session.provider}/{session.model_name}", id="footer-model")
        yield Static(f"Tokens: {self.format_tokens(session.total_tokens)}", id="footer-tokens")

    def on_mount(self) -> None:
        self.set_interval(1.0, self.update_footer)

    def update_footer(self) -> None:
        self.query_one("#footer-model", Static).update(f"/model {session.provider}/{session.model_name}")
        self.query_one("#footer-tokens", Static).update(f"Tokens: {self.format_tokens(session.total_tokens)}")

    def format_tokens(self, count: int) -> str:
        if count >= 1_000_000_000:
            return f"{count / 1_000_000_000:.1f}b"
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}m"
        if count >= 1_000:
            return f"{count / 1_000:.1f}k"
        return str(count)
