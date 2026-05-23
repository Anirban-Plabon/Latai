"""Project file service for secure filesystem access."""

from pathlib import Path
import os
import shutil


class ProjectFileService:
    """Handles secure file read, write, and directory utilities within a jailed root."""

    def __init__(self, root: Path) -> None:
        """Initialize with a locked project root."""
        self.root: Path = root.resolve()

    def resolve_safe_path(self, rel: str) -> Path:
        """Resolve relative path securely, preventing directory traversal."""
        # Strip leading slashes/backslashes to ensure relativity
        clean_rel: str = rel.lstrip("/\\")
        target_path: Path = (self.root / clean_rel).resolve()
        # Verify it stays within root
        if not str(target_path).startswith(str(self.root)):
            raise ValueError("Path traversal attempt detected.")
        return target_path

    def is_binary(self, path: Path) -> bool:
        """Sniff first 8KB of a file to check if it is binary."""
        if not path.is_file():
            return False
        try:
            with open(path, "rb") as f:
                chunk: bytes = f.read(8192)
                return b"\x00" in chunk
        except Exception:
            return True

    def is_too_large(self, path: Path, limit: int = 1024 * 1024) -> bool:
        """Check if file size exceeds size limit in bytes (default 1MB)."""
        if not path.is_file():
            return False
        return path.stat().st_size > limit

    def detect_language(self, path: Path) -> str:
        """Map file extension to Textual TextArea language name."""
        ext: str = path.suffix.lower()
        mapping: dict[str, str] = {
            ".py": "python",
            ".md": "markdown",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".css": "css",
            ".html": "html",
            ".htm": "html",
            ".js": "javascript",
            ".ts": "javascript",
            ".sh": "bash",
            ".bash": "bash",
            ".toml": "toml",
            ".sql": "sql",
            ".rs": "rust",
            ".go": "go",
            ".java": "java",
            ".xml": "xml",
        }
        return mapping.get(ext, "plain")

    def read_file(self, rel: str) -> tuple[str, str]:
        """Read text file safely, returning content and language."""
        path: Path = self.resolve_safe_path(rel)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {rel}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {rel}")
        if self.is_binary(path):
            raise ValueError("Binary files are not supported.")
        if self.is_too_large(path):
            raise ValueError("File is too large (max 1MB).")

        content: str = path.read_text(encoding="utf-8", errors="replace")
        language: str = self.detect_language(path)
        return content, language

    def write_file(self, rel: str, content: str) -> None:
        """Write file atomically using a temporary backup."""
        path: Path = self.resolve_safe_path(rel)
        # Ensure parent directories exist
        path.parent.mkdir(parents=True, exist_ok=True)

        backup_path: Path | None = None
        if path.exists():
            backup_path = path.with_suffix(path.suffix + ".bak")
            shutil.copy2(path, backup_path)

        try:
            # Write to temporary file in same directory for atomicity
            temp_path: Path = path.with_suffix(path.suffix + ".tmp")
            temp_path.write_text(content, encoding="utf-8")
            if os.path.exists(path):
                os.remove(path)
            os.rename(temp_path, path)
            # Remove backup if save was successful
            if backup_path is not None and backup_path.exists():
                os.remove(backup_path)
        except Exception as e:
            # Restore backup if available
            if backup_path is not None and backup_path.exists():
                if os.path.exists(path):
                    os.remove(path)
                os.rename(backup_path, path)
            raise e
