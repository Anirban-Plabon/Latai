"""File type styling and icons."""

EXTENSION_STYLES: dict[str, tuple[str, str]] = {
    ".py": ("🐍", "#3572A5"),
    ".md": ("📝", "#083fa1"),
    ".json": ("📦", "#cb8622"),
    ".yaml": ("⚙️", "#cb171e"),
    ".yml": ("⚙️", "#cb171e"),
    ".toml": ("⚙️", "#9c4221"),
    ".txt": ("📄", "#8b949e"),
    ".css": ("🎨", "#563d7c"),
    ".html": ("🌐", "#e34c26"),
    ".js": ("⚡", "#f1e05a"),
    ".ts": ("💠", "#3178c6"),
    ".rs": ("🦀", "#dea584"),
    ".go": ("🔷", "#00add8"),
    ".sql": ("🗃️", "#e38c00"),
    ".sh": ("🖥️", "#89e051"),
    ".bash": ("🖥️", "#89e051"),
    ".gitignore": ("🚫", "#6e7681"),
}


def get_icon(ext: str) -> str:
    """Get file extension icon."""
    style: tuple[str, str] | None = EXTENSION_STYLES.get(ext.lower())
    if style is not None:
        return style[0]
    return "📄"


def get_color(ext: str) -> str:
    """Get file extension color."""
    style: tuple[str, str] | None = EXTENSION_STYLES.get(ext.lower())
    if style is not None:
        return style[1]
    return "#8b949e"


def get_label(name: str, is_dir: bool) -> str:
    """Get iconified label for a file or directory."""
    if is_dir:
        return f"📁 {name}"
    import os
    _, ext = os.path.splitext(name)
    icon: str = get_icon(ext)
    return f"{icon} {name}"
