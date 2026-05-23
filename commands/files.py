"""Command router for file system commands."""

from typing import TypedDict, Literal


class FileAction(TypedDict):
    action: Literal["tree", "open", "edit", "save", "close"]
    path: str
    glob: str


def route(cmd: str, args: str) -> FileAction:
    """Parse file commands and return action descriptors."""
    cmd_lower: str = cmd.lower()
    clean_args: str = args.strip()

    action: Literal["tree", "open", "edit", "save", "close"] = "tree"
    path: str = ""
    glob: str = ""

    if cmd_lower in ("tree", "files"):
        action = "tree"
        glob = clean_args
    elif cmd_lower == "open":
        action = "open"
        path = clean_args
    elif cmd_lower == "edit":
        action = "edit"
        path = clean_args
    elif cmd_lower == "save":
        action = "save"
    elif cmd_lower == "close":
        action = "close"

    return {"action": action, "path": path, "glob": glob}
