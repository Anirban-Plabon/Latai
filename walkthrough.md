# Walkthrough: General Terminal Mode `/term`

We have implemented the `/term` command and the toggleable persistent **General Terminal Mode** for Latai!

## What Changed

### 1. Persistent Mode Toggle (`/term` without arguments)
- Toggles the persistent **General Terminal Mode**.
- When activated:
  - Chat input prefix changes visually to `(term) ❯ `.
  - Chat input placeholder changes to `"Enter terminal command (e.g. dir, git status)..."`.
  - All subsequent entries in the input box are routed and executed directly as system shell commands.
  - TUI Execution Monitor status panel logs updates asynchronously in real-time.
- Type `/term` again to deactivate and return to standard AI chat mode.

### 2. Single Command Execution (`/term <command>` with arguments)
- Executes the specified system shell command immediately.
- The output of the command is rendered beautifully inside a formatted Markdown code block in the chat view.
- Persistent mode is **not** toggled, allowing quick one-off commands.

---

## Technical Architecture

### 1. Non-Blocking Async Background Workers
- The TUI interface remains fully responsive.
- Command execution is offloaded using Textual's `@work(exclusive=True)` worker.
- Underlying execution uses `asyncio.create_subprocess_shell` for asynchronous standard stream piping.

### 2. File Level Details

#### [NEW] [term.py](file:///F:/Anirban_250509/Projects/Latai/commands/term.py)
- Owns the complete terminal mode toggle logic and subprocess command execution flow.

#### [MODIFY] [session.py](file:///F:/Anirban_250509/Projects/Latai/services/session.py)
- Adds `is_terminal_mode` state to the session singleton.

#### [MODIFY] [app.py](file:///F:/Anirban_250509/Projects/Latai/tui/app.py)
- Integrates the `/term` parsing inside `on_input_submitted`.
- Automatically routes user input to `run_term_command_worker` if persistent terminal mode is enabled.
- Dynamically updates the input prefix and placeholder via `update_input_bar_ui()`.

#### [MODIFY] [app.css](file:///F:/Anirban_250509/Projects/Latai/tui/app.css)
- Adjusted `.rd-prefix` from `width: 2` to `width: auto` to prevent visual clipping of the `(term) ❯ ` prompt.

---

## Verification

### Manual Execution Steps
1. Start the app: `python main.py`
2. **Toggle Persistent Mode**: Type `/term` and press Enter.
   - Prefix changes to `(term) ❯ `.
   - System message announces terminal activation.
   - Status monitor shows "Terminal mode toggled".
3. **Execute shell command in persistent mode**: Type `git status` or `dir` or `pip --version` and press Enter.
   - The status panel logs "Executing shell: <command>".
   - The spinner runs in the loader zone.
   - Command output is rendered inside a scrollable code block.
   - Spinner hides and status monitor logs "Command completed".
4. **Deactivate Persistent Mode**: Type `/term` and press Enter to return to chat mode.
5. **One-Off execution**: Type `/term git diff` to see differential outputs cleanly inside standard chat mode.
