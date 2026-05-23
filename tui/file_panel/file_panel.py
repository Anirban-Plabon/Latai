"""Top-level file system panel widget."""

from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.binding import Binding
from services.files.project_file_service import ProjectFileService
from tui.file_panel.file_tree_panel import FileTreePanel
from tui.file_panel.file_viewer_panel import FileViewerPanel
from tui.file_panel.file_editor_panel import FileEditorPanel


class FilePanel(Horizontal):
    """Container panel for file tree, viewer, and editor."""

    BINDINGS = [
        Binding("ctrl+s", "save_current_file", "Save file", show=True),
        Binding("ctrl+w", "close_file_panel", "Close panel", show=True),
        Binding("ctrl+e", "switch_to_editor", "Edit file", show=True),
    ]

    def __init__(
        self, root: Path, file_service: ProjectFileService, **kwargs
    ) -> None:
        """Initialize file panel."""
        self.root: Path = root
        self.file_service: ProjectFileService = file_service
        self.current_file_path: str | None = None
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """Compose the file tree and content panels."""
        yield FileTreePanel(self.root, id="file-tree-panel")
        yield FileViewerPanel(id="file-viewer-panel")
        yield FileEditorPanel(id="file-editor-panel")

    def on_mount(self) -> None:
        """Set up initial panel visibility."""
        self.query_one("#file-editor-panel", FileEditorPanel).display = False
        self.query_one("#file-viewer-panel", FileViewerPanel).display = True

    def open_file(self, path: str, content: str, language: str) -> None:
        """Load file in read-only viewer and focus it."""
        self.current_file_path = path

        viewer: FileViewerPanel = self.query_one("#file-viewer-panel", FileViewerPanel)
        editor: FileEditorPanel = self.query_one("#file-editor-panel", FileEditorPanel)

        editor.display = False
        viewer.display = True

        viewer.load_file(path, content, language)
        viewer.focus()

    def edit_file(self, path: str, content: str, language: str) -> None:
        """Load file in editable TextArea and focus it."""
        self.current_file_path = path

        viewer: FileViewerPanel = self.query_one("#file-viewer-panel", FileViewerPanel)
        editor: FileEditorPanel = self.query_one("#file-editor-panel", FileEditorPanel)

        viewer.display = False
        editor.display = True

        editor.load_file(path, content, language)
        editor.focus()

    @property
    def has_unsaved_changes(self) -> bool:
        """Check if active editor has unsaved modifications."""
        editor: FileEditorPanel = self.query_one("#file-editor-panel", FileEditorPanel)
        if editor.display:
            return editor.is_dirty
        return False

    def action_save_current_file(self) -> None:
        """Handle ctrl+s keybinding to save active editor."""
        editor: FileEditorPanel = self.query_one("#file-editor-panel", FileEditorPanel)
        if not editor.display or not self.current_file_path:
            return

        try:
            content: str = editor.get_content()
            self.file_service.write_file(self.current_file_path, content)
            editor.mark_saved()
            self.app.post_message(
                self.app.StatusUpdate("done", f"Saved {self.current_file_path}")
            )
            # Add system message to chat log
            chat_view = self.app.query_one("#chat-view")
            chat_view.add_message("system", f"Saved file: {self.current_file_path}")
        except Exception as e:
            self.app.post_message(
                self.app.StatusUpdate("error", f"Save failed: {str(e)}")
            )

    def action_close_file_panel(self) -> None:
        """Handle ctrl+w keybinding to request closing the panel."""
        self.app.handle_close_command()

    def action_switch_to_editor(self) -> None:
        """Handle ctrl+e keybinding to switch from viewer to editor."""
        viewer: FileViewerPanel = self.query_one("#file-viewer-panel", FileViewerPanel)
        if viewer.display and self.current_file_path:
            self.app.handle_edit_from_viewer(self.current_file_path)

    def show_tree(self, glob: str | None) -> None:
        """Update glob filter and reload tree panel."""
        self.query_one("#file-tree-panel", FileTreePanel).refresh_tree(glob)
