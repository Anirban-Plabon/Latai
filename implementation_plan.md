# Implementation Plan — File Browser, Reader & Editor

Add a modular, command-driven file system feature to Latai TUI:
file tree browsing, syntax-highlighted reading, and inline editing — all inside the existing two-column layout.

---

## 1. Feature Design

The file panel **replaces the ChatView** in the `#main-panel` when active, and restores it on `/close`. This avoids layout complexity — one view at a time in the main column.

```
Normal mode:
┌─────────────────────────────────┬─────────────┐
│  ChatView                       │  StatusPanel │
│                                 │              │
├─────────────────────────────────┤              │
│  InputBar                       │              │
└─────────────────────────────────┴─────────────┘

File mode:
┌───────────┬─────────────────────┬─────────────┐
│  FileTree │  FileViewer/Editor  │  StatusPanel │
│           │                     │              │
├───────────┴─────────────────────┤              │
│  InputBar                       │              │
└─────────────────────────────────┴─────────────┘
```

The file panel is a `Horizontal` container with two sub-panels:
- **Left**: `FileTreePanel` (collapsible, ~30% width)
- **Right**: `FileViewerPanel` or `FileEditorPanel` (main content, ~70%)

---

## 2. Command Design

| Command | Action | Notes |
|---------|--------|-------|
| `/tree` or `/files` | Show project directory tree | Replaces ChatView in main panel |
| `/open <path>` | Open file in read-only viewer | Syntax-highlighted, scrollable |
| `/edit <path>` | Open file in editable TextArea | Syntax-highlighted, line numbers |
| `/save` | Save current editor buffer | Only when editor is active |
| `/close` | Close file panel, restore chat | Warns on unsaved changes |
| `/files <glob>` | Filter tree by glob pattern | e.g. `/files *.py` |

All paths are **relative to project root**. Absolute paths and `../` traversal are blocked.

---

## 3. Class Responsibilities

### Service Layer — `services/files/`

#### [NEW] `services/files/__init__.py`
Empty init.

#### [NEW] `services/files/project_file_service.py` — `ProjectFileService`
The **only** module that touches the filesystem. All reads/writes go through here.

| Method | Responsibility |
|--------|---------------|
| `__init__(root: Path)` | Lock to project root |
| `resolve_safe_path(rel: str) -> Path` | Resolve + jail to root, reject `..` |
| `read_file(rel: str) -> tuple[str, str]` | Returns `(content, language)`, rejects binary/large |
| `write_file(rel: str, content: str) -> None` | Atomic write with `.bak` |
| `list_tree(glob: str \| None) -> list[dict]` | Walk tree, return `{path, is_dir, ext, size}` |
| `detect_language(path: Path) -> str` | Map extension → TextArea language name |
| `is_binary(path: Path) -> bool` | Sniff first 8KB for null bytes |
| `is_too_large(path: Path, limit: int) -> bool` | Default 1MB |

#### [NEW] `services/files/file_type_styler.py` — `FileTypeStyler`
Pure-function module for extension → icon/color mapping.

```python
EXTENSION_STYLES: dict[str, tuple[str, str]] = {
    ".py":    ("🐍", "#3572A5"),
    ".md":    ("📝", "#083fa1"),
    ".json":  ("📦", "#cb8622"),
    ".yaml":  ("⚙️",  "#cb171e"),
    ".yml":   ("⚙️",  "#cb171e"),
    ".toml":  ("⚙️",  "#9c4221"),
    ".txt":   ("📄", "#8b949e"),
    ".css":   ("🎨", "#563d7c"),
    ".html":  ("🌐", "#e34c26"),
    ".js":    ("⚡", "#f1e05a"),
    ".ts":    ("💠", "#3178c6"),
    ".rs":    ("🦀", "#dea584"),
    ".go":    ("🔷", "#00add8"),
    ".sql":   ("🗃️",  "#e38c00"),
    ".sh":    ("🖥️",  "#89e051"),
    ".bash":  ("🖥️",  "#89e051"),
    ".gitignore": ("🚫", "#6e7681"),
}
```

Functions:
- `get_icon(ext: str) -> str`
- `get_color(ext: str) -> str`
- `get_label(name: str, is_dir: bool) -> str` — returns `"📁 dirname"` or `"🐍 script.py"`

---

### TUI Layer — `tui/file_panel/`

#### [NEW] `tui/file_panel/__init__.py`
Re-exports `FilePanel`.

#### [NEW] `tui/file_panel/file_panel.py` — `FilePanel(Horizontal)`
The top-level container that orchestrates tree + viewer/editor.

| Method | Responsibility |
|--------|---------------|
| `compose()` | Yields `FileTreePanel` + `FileViewerPanel` |
| `open_file(path: str)` | Load file into viewer via service |
| `edit_file(path: str)` | Load file into editor via service |
| `save_file()` | Delegate to service, clear dirty flag |
| `close_panel()` | Check dirty → warn or close |
| `show_tree(glob: str \| None)` | Refresh tree with optional filter |
| `has_unsaved_changes -> bool` | Property checking editor dirty state |

#### [NEW] `tui/file_panel/file_tree_panel.py` — `FileTreePanel(Vertical)`
Wraps Textual's `DirectoryTree` with custom filtering and extension icons.

| Method | Responsibility |
|--------|---------------|
| `compose()` | Header label + filtered `DirectoryTree` |
| `on_directory_tree_file_selected()` | Post `FileSelected` message |
| `refresh_tree(glob: str \| None)` | Re-filter the tree |

Subclasses `DirectoryTree` as `ProjectDirectoryTree`:
- `filter_paths()` — hide `.git/`, `__pycache__/`, `.venv/`, `node_modules/`
- `render_label()` — prepend extension icons + colors via `FileTypeStyler`

#### [NEW] `tui/file_panel/file_viewer_panel.py` — `FileViewerPanel(Vertical)`
Read-only file viewer with syntax highlighting.

| Method | Responsibility |
|--------|---------------|
| `compose()` | File header (name + icon) + `TextArea(read_only=True)` |
| `load_file(path: str, content: str, language: str)` | Set text + language |
| `clear()` | Reset to empty state |

Uses `TextArea` with:
- `read_only=True`, `show_line_numbers=True`
- `language` set dynamically based on extension
- Custom dark theme matching the app

#### [NEW] `tui/file_panel/file_editor_panel.py` — `FileEditorPanel(Vertical)`
Editable file buffer with syntax highlighting and dirty tracking.

| Method | Responsibility |
|--------|---------------|
| `compose()` | File header (name + modified indicator) + `TextArea.code_editor()` |
| `load_file(path: str, content: str, language: str)` | Set text, clear dirty |
| `get_content() -> str` | Return current buffer text |
| `is_dirty -> bool` | Compare buffer to original |
| `mark_saved()` | Reset dirty tracking |

Uses `TextArea.code_editor()` with:
- `show_line_numbers=True`, `tab_size=4`
- `language` set dynamically
- Tracks `_original_content` for dirty comparison

---

### Command Layer — `commands/`

#### [NEW] `commands/files.py` — `FileCommandRouter`
Pure command router — no UI, no filesystem access. Returns instruction dicts.

```python
def route(cmd: str, args: str) -> dict:
    """Parse file commands and return action descriptors."""
    # Returns: {"action": "tree|open|edit|save|close", "path": "...", "glob": "..."}
```

---

## 4. Data Flow

```
User types "/open utils/config.py"
    │
    ▼
LataiApp.on_input_submitted()
    │  parses cmd="open", args="utils/config.py"
    │
    ▼
commands/files.route("open", "utils/config.py")
    │  returns {"action": "open", "path": "utils/config.py"}
    │
    ▼
LataiApp.handle_file_command(action_dict)
    │  calls ProjectFileService.read_file("utils/config.py")
    │  → returns (content, "python")
    │  → guards: binary? too large? path escape?
    │
    ▼
LataiApp swaps ChatView ↔ FilePanel in #main-panel
    │
    ▼
FilePanel.open_file("utils/config.py")
    │  → FileViewerPanel.load_file(path, content, "python")
    │  → StatusUpdate("tool", "Opened utils/config.py")
```

---

## 5. Keybindings

| Key | Context | Action |
|-----|---------|--------|
| `ctrl+s` | Editor active | Save file |
| `ctrl+w` | File panel active | Close file panel |
| `ctrl+e` | Viewer active | Switch to editor mode |
| `escape` | File panel active | Close (with unsaved warning) |
| `ctrl+g` | Editor active | Go to line number |

These bindings are scoped to the `FilePanel` widget (not global) so they don't conflict with existing app bindings like `q` to quit.

---

## 6. Error Handling

| Scenario | Behavior |
|----------|----------|
| Path traversal (`../../../etc/passwd`) | Reject, show error in chat |
| Binary file (`.png`, `.exe`) | Reject: "Binary file, cannot display" |
| Large file (>1MB) | Reject: "File too large (X MB). Max 1MB" |
| File not found | Show error in chat |
| Permission denied | Show error in chat |
| Unsaved changes on `/close` | Show warning: "Unsaved changes. /save or /close!" |
| Write failure | Show error, keep buffer intact |

---

## 7. Session State Integration

#### [MODIFY] `services/session.py`
Add fields to track file panel state:

```python
self.is_file_panel_open: bool = False
self.current_file_path: str | None = None
self.is_editing: bool = False
```

---

## 8. UI Integration

#### [MODIFY] `tui/app.py`
- Import `FilePanel`, `ProjectFileService`, `FileCommandRouter`
- Add `ProjectFileService(root=Path("."))` instance
- Add method `handle_file_command(action: dict)` — orchestrates swap
- Add method `swap_to_file_panel()` — hides `ChatView`, mounts `FilePanel`
- Add method `swap_to_chat()` — hides `FilePanel`, shows `ChatView`
- Extend `on_input_submitted()` to route `tree|files|open|edit|save|close` commands
- Add keybindings: `ctrl+s` → save, `ctrl+w` → close file panel

#### [MODIFY] `tui/app.css`
Add CSS rules for file panel components:

```css
/* ── File Panel ──────────────────────────────── */
FilePanel          { height: 1fr; width: 100%; }
FileTreePanel      { width: 30%; min-width: 20; border-right: tall #30363d; }
FileViewerPanel    { width: 1fr; }
FileEditorPanel    { width: 1fr; }

.file-header       { height: 1; background: #161b22; color: #e6edf3; padding: 0 1; text-style: bold; }
.file-header-dirty  { color: #f85149; }  /* red dot for unsaved */

ProjectDirectoryTree { background: #0d1117; }
TextArea            { background: #0d1117; }
TextArea.-read-only { border: none; }
```

#### [MODIFY] `tui/command_menu.py`
Add `/tree`, `/open`, `/edit`, `/save`, `/close` to `AVAILABLE_COMMANDS` list.

---

## Proposed Changes Summary

| File | Action | Component |
|------|--------|-----------|
| `services/files/__init__.py` | NEW | Package init |
| `services/files/project_file_service.py` | NEW | Filesystem service |
| `services/files/file_type_styler.py` | NEW | Extension → icon/color |
| `tui/file_panel/__init__.py` | NEW | Package init |
| `tui/file_panel/file_panel.py` | NEW | Top-level file container |
| `tui/file_panel/file_tree_panel.py` | NEW | Directory tree widget |
| `tui/file_panel/file_viewer_panel.py` | NEW | Read-only viewer |
| `tui/file_panel/file_editor_panel.py` | NEW | Editable buffer |
| `commands/files.py` | NEW | Command router |
| `services/session.py` | MODIFY | Add file panel state |
| `tui/app.py` | MODIFY | Wire commands + panel swap |
| `tui/app.css` | MODIFY | File panel styling |
| `tui/command_menu.py` | MODIFY | Register new commands |

---

## Verification Plan

### Manual Verification
1. `python main.py` → type `/tree` → project directory tree appears in left sub-panel
2. Click a `.py` file in the tree → viewer opens with syntax highlighting
3. `/open README.md` → markdown-highlighted viewer opens
4. `/edit tui/app.py` → editable TextArea with line numbers opens
5. Make a change → header shows `●` dirty indicator
6. `/save` → file saved, indicator clears, status panel logs "Saved"
7. `/close` with unsaved changes → warning message displayed
8. `/close` after saving → chat view restored
9. Try `/open ../../etc/passwd` → path traversal blocked
10. Try `/open image.png` → binary rejection
11. Press `ctrl+s` in editor → saves, same as `/save`
12. Press `ctrl+w` → closes panel, same as `/close`
