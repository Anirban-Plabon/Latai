from textual.app import ComposeResult
from textual.widgets import Markdown, Button, Static
from textual.widgets._markdown import MarkdownFence

class MarkdownFenceWithCopy(MarkdownFence):
    """A code block with a 'Copy' button in the top right."""
    
    def compose(self) -> ComposeResult:
        yield from super().compose()
        yield Button("📋", variant="primary", id="copy-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "copy-btn":
            self.app.copy_to_clipboard(self.code)
            
            # Provide visual feedback
            event.button.label = "✅"
            event.button.variant = "success"
            
            # Reset button after 2 seconds
            def reset():
                event.button.label = "📋"
                event.button.variant = "primary"
            self.set_timer(2.0, reset)

class CustomMarkdown(Markdown):
    """Markdown widget that uses our custom code block class."""
    
    def get_block_class(self, token_type: str) -> type[Static] | None:
        if token_type == "fence":
            return MarkdownFenceWithCopy
        return super().get_block_class(token_type)
