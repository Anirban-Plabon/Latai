import asyncio
import os
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

    args = args.strip()

    if not hasattr(session, "cwd"):
        session.cwd = os.getcwd()

    # Intercept `cd` commands
    if args.startswith("cd ") or args == "cd":
        target = args[3:].strip()
        if not target:
            target = os.path.expanduser("~")
        
        new_cwd = os.path.abspath(os.path.join(session.cwd, target))
        if os.path.isdir(new_cwd):
            session.cwd = new_cwd
            return f"Changed directory to {session.cwd}"
        else:
            return f"cd: {target}: No such file or directory"

    try:
        import sys
        if sys.platform == "win32":
            process = await asyncio.create_subprocess_exec(
                "powershell.exe",
                "-NoProfile",
                "-Command",
                args,
                cwd=session.cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            process = await asyncio.create_subprocess_shell(
                args,
                cwd=session.cwd,
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
