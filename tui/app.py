import uuid
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Input, Rule, Button, DirectoryTree
from textual.containers import Horizontal, Vertical
from textual import work, on
from langchain_core.messages import HumanMessage

from tui.chat_view import ChatView
from tui.input_bar import InputBar
from tui.command_menu import CommandMenu, MENU_MODELS, MENU_THEMES, MENU_COMMANDS
from tui.status_panel import StatusPanel
from tui.status_event import StatusUpdate
from tui.splitter import VerticalSplitter
from commands.base import is_command, parse_command
from commands import model as cmd_model
from services.session import session
from agent.graph import graph
from res.ui.welcome import animate_welcome
from res.ui.loaders import ThinkingIndicator
from tui.header import CustomHeader
from tui.footer import CustomFooter

from tui.file_panel import FilePanel
from services.files.project_file_service import ProjectFileService
from commands import files as cmd_files


class LataiApp(App):
    """The main Latai TUI chat application class."""

    def __init__(self, **kwargs) -> None:
        """Initialize LataiApp with file service."""
        super().__init__(**kwargs)
        self.file_service = ProjectFileService(Path("."))

    CSS_PATH = "app.css"

    DEV_LOCAL_THEME = {
        "primary": "#FFB6C1",    # Light Pink
        "secondary": "#ADD8E6",   # Light Blue
        "loader_thinking": "loader76",
        "loader_generating": "loader77",
    }

    BINDINGS = [
        ("q",      "quit",         "Quit"),
        ("ctrl+p", "open_menu",    "Command menu"),
        ("[",      "resize_left",  "Shrink panel"),
        ("]",      "resize_right", "Expand panel"),
    ]

    def compose(self) -> ComposeResult:
        yield CustomHeader()
        with Horizontal(id="app-columns"):
            with Vertical(id="main-panel"):
                yield ChatView(id="chat-view")
                yield FilePanel(Path("."), self.file_service, id="file-panel")
                with Vertical(classes="bottom-zone"):
                    yield Rule(classes="zone-separator")
                    yield Vertical(id="loading-container")
                    with Horizontal(classes="input-wrapper"):
                        yield InputBar()
            yield VerticalSplitter()
            yield StatusPanel(id="status-panel")

        yield CustomFooter()
        yield CommandMenu(id="cmd-menu")

    def on_status_update(self, event: StatusUpdate) -> None:
        self.query_one(StatusPanel).post_status(event.category, event.text)

    def action_resize_left(self) -> None:
        self.adjust_splitter(-2)

    def action_resize_right(self) -> None:
        self.adjust_splitter(2)

    def adjust_splitter(self, delta: int) -> None:
        main_panel = self.query_one("#main-panel")
        status_panel = self.query_one("#status-panel")

        current_main_width = main_panel.size.width
        screen_width = self.size.width

        new_main_width = current_main_width + delta
        new_status_width = screen_width - new_main_width - 1

        min_main_width = 30
        min_status_width = 20

        if new_main_width >= min_main_width and new_status_width >= min_status_width:
            main_panel.styles.width = new_main_width
            status_panel.styles.width = new_status_width

    def on_mount(self) -> None:
        self.post_message(StatusUpdate("plan", "Initializing Latai..."))
        self.query_one(InputBar).focus_input()
        self.update_input_bar_ui()
        self.query_one("#file-panel", FilePanel).display = False
        chat_view = self.query_one("#chat-view", ChatView)
        animate_welcome(
            self, 
            chat_view, 
            color_start=self.DEV_LOCAL_THEME["primary"], 
            color_end=self.DEV_LOCAL_THEME["secondary"]
        )
        self.post_message(StatusUpdate("done", "Ready"))

    def show_loading(self) -> None:
        self.post_message(StatusUpdate("agent", "AI is thinking..."))
        container = self.query_one("#loading-container", Vertical)
        indicators = container.query(ThinkingIndicator)
        
        if indicators:
            indicator = indicators.first()
            if hasattr(indicator, "cleanup_timer"):
                indicator.cleanup_timer.stop()
            indicator.change_state(self.DEV_LOCAL_THEME["loader_thinking"], "AI is thinking...", reset_timer=True)
        else:
            for child in container.query("*"):
                child.remove()
            container.mount(ThinkingIndicator(
                loader_name=self.DEV_LOCAL_THEME["loader_thinking"],
                label="AI is thinking...",
                classes="loading-text"
            ))
            
        container.add_class("-active")

    def hide_loading(self) -> None:
        try:
            container = self.query_one("#loading-container", Vertical)
            for child in container.query("*"):
                if hasattr(child, "stop"):
                    child.stop()
                if hasattr(child, "cleanup_timer"):
                    child.cleanup_timer.stop()
                child.remove()
            container.remove_class("-active")
        except Exception:
            pass

    def show_generating(self) -> None:
        self.post_message(StatusUpdate("agent", "Generating..."))
        container = self.query_one("#loading-container", Vertical)
        indicators = container.query(ThinkingIndicator)
        
        if indicators:
            indicator = indicators.first()
            if hasattr(indicator, "cleanup_timer"):
                indicator.cleanup_timer.stop()
            indicator.change_state(self.DEV_LOCAL_THEME["loader_generating"], "Generating...")
        else:
            container.mount(ThinkingIndicator(
                loader_name=self.DEV_LOCAL_THEME["loader_generating"],
                label="Generating...",
                classes="loading-text"
            ))
            
        container.add_class("-active")

    def show_done(self) -> None:
        self.post_message(StatusUpdate("done", "Response complete"))
        try:
            container = self.query_one("#loading-container", Vertical)
            indicators = container.query(ThinkingIndicator)
            
            if indicators:
                indicator = indicators.first()
                if hasattr(indicator, "stop"):
                    indicator.stop()
                indicator.mark_done()
                
                def cleanup() -> None:
                    try:
                        container.remove_class("-active")
                        indicator.remove()
                    except Exception:
                        pass
                indicator.cleanup_timer = indicator.set_timer(2.0, cleanup)
        except Exception:
            pass

    def action_open_menu(self) -> None:
        self.query_one(CommandMenu).open()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cmd-menu-btn":
            self.query_one(CommandMenu).open()

    def on_command_menu_model_selected(self, event: CommandMenu.ModelSelected) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        oid = event.option_id

        if not oid.startswith("model__"):
            return

        parts = oid.split("__")
        if len(parts) != 3:
            return

        provider, model = parts[1], parts[2]
        session.set_model(provider, model)
        chat_view.add_message("system", f"Switched to {provider}/{model}")
        self.post_message(StatusUpdate("done", f"Model: {provider}/{model}"))

    def on_command_menu_theme_selected(self, event: CommandMenu.ThemeSelected) -> None:
        self.theme = event.theme_name
        self.query_one("#chat-view", ChatView).add_message(
            "system", f"Theme set to: {event.theme_name}"
        )
        self.post_message(StatusUpdate("done", f"Theme: {event.theme_name}"))

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value.strip()
        if not user_input:
            return

        event.input.value = ""
        chat_view = self.query_one("#chat-view", ChatView)
        menu      = self.query_one(CommandMenu)

        if user_input in ("/models", "/model"):
            menu.open(MENU_MODELS)
            return
        if user_input == "/themes":
            menu.open(MENU_THEMES)
            return
        if user_input == "/commands":
            menu.open(MENU_COMMANDS)
            return

        chat_view.add_message("user", user_input)

        if is_command(user_input):
            cmd, args = parse_command(user_input)
            self.post_message(StatusUpdate("tool", f"Running /{cmd}..."))
            if cmd in ("tree", "files", "open", "edit", "save", "close", "close!"):
                self.handle_file_command_by_name(cmd, args)
            elif cmd == "model":
                result = cmd_model.execute(args)
                chat_view.add_message("system", result)
                self.post_message(StatusUpdate("done", "Model switched"))
            elif cmd == "ask":
                self.stream_response(args, bypass_history=True)
            elif cmd == "term":
                self.run_term_command_worker(args, is_toggle=not bool(args))
            else:
                chat_view.add_message("system", f"Unknown command: /{cmd}")
                self.post_message(StatusUpdate("error", f"Unknown command: /{cmd}"))
        else:
            if getattr(session, "is_terminal_mode", False):
                self.run_term_command_worker(user_input, is_toggle=False)
            else:
                session.add_user_message(user_input)
                self.stream_response(user_input, bypass_history=False)

    @work(exclusive=True)
    async def stream_response(self, user_input: str, bypass_history: bool) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        msg_id    = f"msg-{uuid.uuid4()}"

        self.post_message(StatusUpdate("agent", "Streaming response..."))
        self.show_loading()

        accumulated_content   = ""
        first_chunk_received  = False
        message_added         = False

        try:
            messages = (
                [HumanMessage(content=user_input)]
                if bypass_history
                else session.get_messages()
            )
            state = {"messages": messages}

            async for msg, metadata in graph.astream(state, stream_mode="messages"):
                content = ""
                if hasattr(msg, "content"):
                    if isinstance(msg.content, str):
                        content = msg.content
                    elif isinstance(msg.content, list):
                        for part in msg.content:
                            if isinstance(part, dict) and part.get("type") == "text":
                                content += part.get("text", "")
                            elif isinstance(part, str):
                                content += part

                if content:
                    if not first_chunk_received:
                        first_chunk_received = True
                        self.show_generating()
                        chat_view.add_message("ai", "", msg_id)
                        message_added = True

                    accumulated_content += content
                    chat_view.update_message(msg_id, accumulated_content)

            if message_added:
                self.show_done()
            else:
                self.hide_loading()
                if accumulated_content:
                    chat_view.add_message("ai", accumulated_content, msg_id)
                else:
                    chat_view.add_message("system", "No response from model.")
                    self.post_message(StatusUpdate("error", "No response from model"))

            if not bypass_history:
                session.add_ai_message(accumulated_content)

        except Exception as e:
            self.hide_loading()
            self.post_message(StatusUpdate("error", f"Stream error: {e}"))
            if not message_added:
                chat_view.add_message("system", f"Error: {str(e)}", msg_id)
            else:
                chat_view.update_message(msg_id, f"Error: {str(e)}")

    @work(exclusive=True)
    async def run_term_command_worker(self, args: str, is_toggle: bool) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        self.show_loading()

        if is_toggle:
            from commands import term as cmd_term
            result = await cmd_term.execute("")
            chat_view.add_message("system", result)
            self.post_message(StatusUpdate("done", "Terminal mode toggled"))
            self.update_input_bar_ui()
        else:
            self.post_message(StatusUpdate("tool", f"Executing shell: {args}"))
            from commands import term as cmd_term
            result = await cmd_term.execute(args)
            chat_view.add_message("system", f"```\n{result}\n```")
            self.post_message(StatusUpdate("done", "Command completed"))

        self.hide_loading()

    def update_input_bar_ui(self) -> None:
        try:
            prefix = self.query_one(".rd-prefix", Static)
            chat_input = self.query_one("#chat-input", Input)
            is_term = getattr(session, "is_terminal_mode", False)

            prefix.update("(term) ❯ " if is_term else "❯ ")
            if is_term:
                chat_input.placeholder = "Enter terminal command (e.g. dir, git status)..."
            else:
                chat_input.placeholder = "Type a message or command (e.g., /model, /ask)..."
        except Exception:
            pass

    def swap_to_file_panel(self) -> None:
        """Switch view from ChatView to FilePanel."""
        chat_view = self.query_one("#chat-view", ChatView)
        file_panel = self.query_one("#file-panel", FilePanel)
        chat_view.display = False
        file_panel.display = True
        session.is_file_panel_open = True

    def swap_to_chat(self) -> None:
        """Switch view from FilePanel back to ChatView."""
        chat_view = self.query_one("#chat-view", ChatView)
        file_panel = self.query_one("#file-panel", FilePanel)
        file_panel.display = False
        chat_view.display = True
        session.is_file_panel_open = False
        self.query_one(InputBar).focus_input()

    def handle_close_command(self, force: bool = False) -> None:
        """Handle closing the file panel, checking for unsaved changes."""
        file_panel = self.query_one("#file-panel", FilePanel)
        chat_view = self.query_one("#chat-view", ChatView)
        if not force and file_panel.has_unsaved_changes:
            chat_view.add_message(
                "system",
                "Warning: Unsaved changes in active editor. Type /save to save or /close! to force close without saving."
            )
            self.post_message(StatusUpdate("warning", "Unsaved changes in editor"))
            return

        self.swap_to_chat()
        chat_view.add_message("system", "Closed file panel.")
        self.post_message(StatusUpdate("done", "File panel closed"))

    def handle_edit_from_viewer(self, path: str) -> None:
        """Switch active file from read-only viewer to editable editor."""
        self.handle_file_command_by_name("edit", path)

    def handle_file_command_by_name(self, cmd: str, args: str) -> None:
        """Process and execute file operations."""
        chat_view = self.query_one("#chat-view", ChatView)
        file_panel = self.query_one("#file-panel", FilePanel)

        action_dict = cmd_files.route(cmd, args)
        action = action_dict["action"]

        if action == "tree":
            self.swap_to_file_panel()
            file_panel.show_tree(action_dict["glob"] or None)
            chat_view.add_message(
                "system",
                f"Showing workspace tree. Filter: {action_dict['glob'] or 'None'}"
            )
            self.post_message(StatusUpdate("done", "Workspace tree loaded"))

        elif action == "open":
            path = action_dict["path"]
            if not path:
                chat_view.add_message("system", "Error: Usage: /open <path>")
                self.post_message(StatusUpdate("error", "No path provided"))
                return
            try:
                content, language = self.file_service.read_file(path)
                self.swap_to_file_panel()
                file_panel.open_file(path, content, language)
                chat_view.add_message("system", f"Opened file: {path} (read-only)")
                self.post_message(StatusUpdate("done", f"Opened {path}"))
            except Exception as e:
                chat_view.add_message("system", f"Error: {str(e)}")
                self.post_message(StatusUpdate("error", str(e)))

        elif action == "edit":
            path = action_dict["path"]
            if not path:
                chat_view.add_message("system", "Error: Usage: /edit <path>")
                self.post_message(StatusUpdate("error", "No path provided"))
                return
            try:
                content, language = self.file_service.read_file(path)
                self.swap_to_file_panel()
                file_panel.edit_file(path, content, language)
                chat_view.add_message("system", f"Opened file for editing: {path}")
                self.post_message(StatusUpdate("done", f"Editing {path}"))
            except Exception as e:
                chat_view.add_message("system", f"Error: {str(e)}")
                self.post_message(StatusUpdate("error", str(e)))

        elif action == "save":
            if not session.is_file_panel_open:
                chat_view.add_message("system", "Error: File panel must be open to save.")
                self.post_message(StatusUpdate("error", "File panel not open"))
                return
            file_panel.action_save_current_file()

        elif action == "close":
            force = (cmd == "close!" or args.strip() == "!" or args.strip() == "force")
            self.handle_close_command(force=force)

    @on(DirectoryTree.FileSelected)
    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle double-clicking or pressing Enter on a file in the tree."""
        try:
            rel_path = event.path.relative_to(self.file_service.root)
            self.handle_file_command_by_name("open", str(rel_path))
        except Exception as e:
            chat_view = self.query_one("#chat-view", ChatView)
            chat_view.add_message("system", f"Error opening tree item: {str(e)}")
            self.post_message(StatusUpdate("error", str(e)))


if __name__ == "__main__":
    LataiApp().run()