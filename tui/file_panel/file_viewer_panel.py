"""Read-only file viewer panel."""

from textual.widgets import TextArea, Label
from textual.containers import Vertical
from services.files.file_type_styler import get_icon


class FileViewerPanel(Vertical):
    """File viewer panel container."""

    def compose(self):
        """Compose the viewer panel widgets."""
        yield Label("📄 No file open", classes="file-header")
        yield TextArea("", read_only=True, show_line_numbers=True, id="viewer-text")

    def load_file(self, path: str, content: str, language: str) -> None:
        """Load file content into read-only viewer."""
        import os
        _, ext = os.path.splitext(path)
        icon: str = get_icon(ext)
        header_text: str = f"👀 {icon} {path} (read-only)"

        header: Label = self.query_one(".file-header", Label)
        header.update(header_text)

        text_area: TextArea = self.query_one("#viewer-text", TextArea)
        text_area.load_text(content)
        # Handle plain text language safely
        text_area.language = language if language != "plain" else None

    def clear(self) -> None:
        """Clear viewer content."""
        header: Label = self.query_one(".file-header", Label)
        header.update("📄 No file open")
        text_area: TextArea = self.query_one("#viewer-text", TextArea)
        text_area.load_text("")
        text_area.language = None
