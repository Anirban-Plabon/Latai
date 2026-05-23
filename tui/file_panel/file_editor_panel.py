"""Editable file buffer panel."""

import os
from textual import on
from textual.widgets import TextArea, Label
from textual.containers import Vertical
from services.files.file_type_styler import get_icon


class FileEditorPanel(Vertical):
    """File editor panel container."""

    def __init__(self, **kwargs) -> None:
        """Initialize editor panel."""
        self.file_path: str | None = None
        self._original_content: str = ""
        super().__init__(**kwargs)

    def compose(self):
        """Compose the editor panel widgets."""
        yield Label("📄 No file open", classes="file-header")
        yield TextArea.code_editor("", show_line_numbers=True, id="editor-text")

    def load_file(self, path: str, content: str, language: str) -> None:
        """Load file content into editable TextArea."""
        self.file_path = path
        self._original_content = content

        text_area: TextArea = self.query_one("#editor-text", TextArea)
        text_area.load_text(content)
        text_area.language = language if language != "plain" else None

        self.update_header()

    def get_content(self) -> str:
        """Return the current buffer text."""
        text_area: TextArea = self.query_one("#editor-text", TextArea)
        return text_area.text

    @property
    def is_dirty(self) -> bool:
        """Check if buffer differs from original content."""
        if self.file_path is None:
            return False
        return self.get_content() != self._original_content

    def mark_saved(self) -> None:
        """Reset dirty tracking to current buffer content."""
        self._original_content = self.get_content()
        self.update_header()

    def update_header(self) -> None:
        """Update header label with dirty indicator."""
        if not self.file_path:
            header: Label = self.query_one(".file-header", Label)
            header.update("📄 No file open")
            return

        _, ext = os.path.splitext(self.file_path)
        icon: str = get_icon(ext)
        dirty_str: str = " ●" if self.is_dirty else ""
        header_text: str = f"📝 {icon} {self.file_path}{dirty_str}"

        header_widget: Label = self.query_one(".file-header", Label)
        header_widget.update(header_text)
        if self.is_dirty:
            header_widget.add_class("file-header-dirty")
        else:
            header_widget.remove_class("file-header-dirty")

    @on(TextArea.Changed)
    def on_changed(self, event: TextArea.Changed) -> None:
        """Handle content modification to update dirty indicator."""
        if self.file_path:
            self.update_header()
