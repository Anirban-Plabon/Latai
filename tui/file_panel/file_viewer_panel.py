"""Read-only file viewer panel."""

import os
from textual.app import ComposeResult
from textual.widgets import TextArea, Label, Markdown
from textual.containers import Vertical
from services.files.file_type_styler import get_icon
from services.files.language_guard import safe_language


_MARKDOWN_EXTENSIONS: frozenset[str] = frozenset({".md", ".markdown", ".mdown", ".mkd"})


class FileViewerPanel(Vertical):
    """File viewer panel container."""

    def compose(self) -> ComposeResult:
        """Compose the viewer panel widgets."""
        yield Label("🗎 No file open", classes="file-header")
        yield TextArea("", read_only=True, show_line_numbers=True, id="viewer-text", theme="vscode_dark")
        yield Markdown("", id="viewer-markdown")

    def on_mount(self) -> None:
        """Hide markdown viewer by default."""
        self.query_one("#viewer-markdown", Markdown).display = False

    def load_file(self, path: str, content: str, language: str) -> None:
        """Load file content. Uses Markdown widget for .md files, TextArea for all others."""
        _, ext = os.path.splitext(path)
        icon: str = get_icon(ext)

        header: Label = self.query_one(".file-header", Label)
        header.update(f"{icon} {path} (read-only)")

        if ext.lower() in _MARKDOWN_EXTENSIONS:
            self._show_markdown(content)
        else:
            self._show_text(content, language)

    def _show_markdown(self, content: str) -> None:
        """Render content in the Markdown widget."""
        self.query_one("#viewer-text", TextArea).display = False
        md: Markdown = self.query_one("#viewer-markdown", Markdown)
        md.display = True
        md.update(content)

    def _show_text(self, content: str, language: str) -> None:
        """Render content in the read-only TextArea with syntax highlighting."""
        self.query_one("#viewer-markdown", Markdown).display = False
        text_area: TextArea = self.query_one("#viewer-text", TextArea)
        text_area.display = True
        text_area.load_text(content)
        text_area.language = safe_language(language)

    def clear(self) -> None:
        """Clear viewer content and reset to idle state."""
        self.query_one(".file-header", Label).update("🗎 No file open")
        text_area: TextArea = self.query_one("#viewer-text", TextArea)
        text_area.display = True
        text_area.load_text("")
        text_area.language = None
        md: Markdown = self.query_one("#viewer-markdown", Markdown)
        md.display = False
        md.update("")
