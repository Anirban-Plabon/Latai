def is_command(text: str) -> bool:
    return text.startswith("/")

def parse_command(text: str) -> tuple[str, str]:
    parts = text.split(" ", 1)
    cmd = parts[0][1:]
    args = parts[1] if len(parts) > 1 else ""
    return cmd, args
