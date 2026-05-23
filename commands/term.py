import asyncio
from services.session import session


async def execute(args: str) -> str:
    """Execute /term command.

    If args is empty, toggle persistent terminal mode.
    If args is provided, run the command once.
    """
    if not args:
        is_active = not getattr(session, "is_terminal_mode", False)
        session.is_terminal_mode = is_active
        if is_active:
            return (
                "Terminal mode activated. Any input will be executed as a system shell command. "
                "Type /term again to exit."
            )
        return "Terminal mode deactivated."

    try:
        import sys
        if sys.platform == "win32":
            process = await asyncio.create_subprocess_exec(
                "powershell.exe",
                "-NoProfile",
                "-Command",
                args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            process = await asyncio.create_subprocess_shell(
                args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        stdout, stderr = await process.communicate()

        output = stdout.decode(errors="replace")
        error_output = stderr.decode(errors="replace")

        result = ""
        if output:
            result += output
        if error_output:
            if result:
                result += "\n"
            result += f"Error:\n{error_output}"
        if not result:
            result = f"Command exited with code {process.returncode} (no output)"
        return result
    except Exception as e:
        return f"Error executing command: {str(e)}"
