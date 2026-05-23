"""File tree panel widget."""

from pathlib import Path
from typing import Iterable
from rich.text import Text
from textual.widgets import DirectoryTree, Label
from textual.containers import Vertical
from services.files.file_type_styler import get_icon, get_color


class ProjectDirectoryTree(DirectoryTree):
    """Custom DirectoryTree that filters and styles nodes."""

    def __init__(self, path: Path, glob_filter: str | None = None, **kwargs) -> None:
        """Initialize directory tree with optional glob filter."""
        self.glob_filter: str | None = glob_filter
        super().__init__(path, **kwargs)

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        """Filter out hidden and irrelevant files/folders, and apply optional glob."""
        from fnmatch import fnmatch
        ignored: set[str] = {
            ".git",
            "__pycache__",
            ".venv",
            "node_modules",
            ".gemini",
            "graphify-out",
        }
        filtered: list[Path] = []
        for p in paths:
            if p.name in ignored:
                continue
            if p.is_file() and self.glob_filter:
                if not fnmatch(p.name, self.glob_filter):
                    continue
            filtered.append(p)
        return filtered

    def render_label(self, node, base_style, style) -> Text:
        """Render a custom styled label with file icons."""
        if node.data is None:
            return super().render_label(node, base_style, style)

        path: Path = node.data.path
        if node.is_root:
            return super().render_label(node, base_style, style)

        is_dir: bool = path.is_dir()
        name: str = path.name

        if is_dir:
            icon: str = "📁"
            color: str = "#e3b341"
        else:
            import os
            _, ext = os.path.splitext(name)
            icon = get_icon(ext)
            color = get_color(ext)

        label_text: Text = Text()
        label_text.append(icon + " ", style=color)
        label_text.append(name, style=style)
        return label_text


class FileTreePanel(Vertical):
    """File tree panel container."""

    def __init__(self, root: Path, glob_filter: str | None = None, **kwargs) -> None:
        """Initialize tree panel."""
        self.root: Path = root
        self.glob_filter: str | None = glob_filter
        super().__init__(**kwargs)

    def compose(self):
        """Compose the tree panel widgets."""
        header_text: str = "📁 Workspace"
        if self.glob_filter:
            header_text += f" ({self.glob_filter})"
        yield Label(header_text, classes="file-header")
        yield ProjectDirectoryTree(self.root, glob_filter=self.glob_filter, id="project-tree")

    def refresh_tree(self, glob: str | None) -> None:
        """Update the glob filter and reload the tree."""
        self.glob_filter = glob
        tree: ProjectDirectoryTree = self.query_one("#project-tree", ProjectDirectoryTree)
        tree.glob_filter = glob
        header_text: str = "📁 Workspace"
        if glob:
            header_text += f" ({glob})"
        header: Label = self.query_one(".file-header", Label)
        header.update(header_text)
        tree.reload()
