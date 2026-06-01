import uuid
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Rule, Button, DirectoryTree, OptionList, TextArea
from textual.containers import Horizontal, Vertical
from textual import work, on, events
from langchain_core.messages import HumanMessage

from tui.chat_view import ChatView
from tui.input_bar import InputBar, ChatInput
from tui.command_menu import CommandMenu, MENU_MODELS, MENU_THEMES, MENU_COMMANDS
from tui.status_panel import StatusPanel
from tui.status_event import StatusUpdate
from tui.splitter import VerticalSplitter
from commands.base import is_command, parse_command
from commands import model as cmd_model
from services.session import session
from agent.graph import phase1_graph
from res.ui.welcome import animate_welcome
from res.ui.loaders import ThinkingIndicator
from tui.header import CustomHeader
from tui.footer import CustomFooter

from tui.file_panel import FilePanel
from services.files.project_file_service import ProjectFileService
from commands import files as cmd_files
from utils.ui_config import DEV_LOCAL_THEME, dev_color_theme


class LataiApp(App):
    """The main Latai TUI chat application class."""

    def __init__(self, **kwargs) -> None:
        """Initialize LataiApp with file service."""
        super().__init__(**kwargs)
        workspace_path = Path("test") if Path("test").is_dir() else Path(".")
        session.cwd = str(workspace_path.resolve())
        self.file_service = ProjectFileService(workspace_path)

    CSS_PATH = "app.css"

    BINDINGS = [
        ("q",      "quit",         "Quit"),
        ("ctrl+p", "open_menu",    "Command menu"),
        ("[",      "resize_left",  "Shrink panel"),
        ("]",      "resize_right", "Expand panel"),
    ]

    def compose(self) -> ComposeResult:
        workspace_path = Path("test") if Path("test").is_dir() else Path(".")
        yield CustomHeader()
        with Horizontal(id="app-columns"):
            with Vertical(id="main-panel"):
                yield ChatView(id="chat-view")
                yield FilePanel(workspace_path, self.file_service, id="file-panel")
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
        self.register_theme(dev_color_theme)
        self.theme = "dev_color_theme"
        self.post_message(StatusUpdate("plan", "Initializing Latai..."))
        self.query_one(InputBar).focus_input()
        self.update_input_bar_ui()
        self.query_one("#file-panel", FilePanel).display = False
        chat_view = self.query_one("#chat-view", ChatView)
        animate_welcome(
            self, 
            chat_view, 
            color_start=DEV_LOCAL_THEME["primary"], 
            color_end=DEV_LOCAL_THEME["secondary"]
        )
        self.post_message(StatusUpdate("done", "Ready"))

    def show_loading(self) -> None:
        container = self.query_one("#loading-container", Vertical)
        indicators = container.query(ThinkingIndicator)
        
        if indicators:
            indicator = indicators.first()
            if hasattr(indicator, "cleanup_timer"):
                indicator.cleanup_timer.stop()
            indicator.change_state(DEV_LOCAL_THEME["loader_thinking"], "AI is thinking...", reset_timer=True)
        else:
            for child in container.query("*"):
                child.remove()
            container.mount(ThinkingIndicator(
                loader_name=DEV_LOCAL_THEME["loader_thinking"],
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
        container = self.query_one("#loading-container", Vertical)
        indicators = container.query(ThinkingIndicator)
        
        if indicators:
            indicator = indicators.first()
            if hasattr(indicator, "cleanup_timer"):
                indicator.cleanup_timer.stop()
            indicator.change_state(DEV_LOCAL_THEME["loader_generating"], "Generating...")
        else:
            container.mount(ThinkingIndicator(
                loader_name=DEV_LOCAL_THEME["loader_generating"],
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

    def on_command_menu_command_selected(self, event: CommandMenu.CommandSelected) -> None:
        cmd_str = event.command
        input_bar = self.query_one(InputBar)
        input_widget = input_bar.query_one(Input)

        needs_args = False
        prefix = cmd_str
        for arg_cmd in ("/open", "/edit", "/ask", "/tree", "/model"):
            if cmd_str.startswith(arg_cmd):
                needs_args = True
                prefix = arg_cmd + " "
                break

        if needs_args:
            input_widget.value = prefix
            input_bar.focus_input()
        else:
            input_widget.value = cmd_str
            self.post_message(Input.Submitted(input_widget, value=cmd_str))

    @on(events.Key)
    def handle_keys(self, event: events.Key) -> None:
        try:
            input_widget = self.query_one(ChatInput)
            if input_widget.has_focus and input_widget.text.startswith("/"):
                if event.key in ("up", "down"):
                    event.stop()
                    status_panel = self.query_one("#status-panel", StatusPanel)
                    new_cmd = status_panel.navigate_commands(event.key)
                    if new_cmd:
                        input_widget.text = new_cmd + " "
                        input_widget.move_cursor((0, len(input_widget.text)))
        except Exception:
            pass

    @on(TextArea.Changed, "#chat-input")
    def on_chat_input_changed(self, event: TextArea.Changed) -> None:
        try:
            val = event.text_area.text
            input_widget = event.text_area
            status_panel = self.query_one("#status-panel", StatusPanel)
            if val.startswith("/"):
                input_widget.add_class("command-active")
                status_panel.show_inline_commands()
            else:
                input_widget.remove_class("command-active")
                status_panel.hide_inline_commands()
        except Exception:
            pass

    @on(OptionList.OptionSelected, "#approval-options")
    def on_approval_option_selected(self, event: OptionList.OptionSelected) -> None:
        if session.pending_state is None:
            return
            
        input_bar = self.query_one(InputBar)
        input_bar.hide_approval()
        
        selected = str(event.option.prompt)
        chat_view = self.query_one("#chat-view", ChatView)
        
        if session.pending_state.get("type") == "plan_approval":
            if "Approved" in selected:
                chat_view.add_message("user", "Approved")
                state = session.pending_state
                session.pending_state = None
                self.run_generator_worker(session.get_messages())
                return
            elif "Revise" in selected:
                chat_view.add_message("user", "Revise")
                state = session.pending_state
                session.pending_state = None
                
                original_prompt = state.get("user_input", "")
                revision_instruction = (
                    f"Please revise the plan for the request: '{original_prompt}'. "
                    "Check if there are any major unfocused areas and revise the plan to address them."
                )
                session.add_user_message(revision_instruction)
                self.stream_response(revision_instruction, bypass_history=False, route="new_task")
                return
            elif "Cancel" in selected:
                session.pending_state = None
                chat_view.add_message("user", "Cancel")
                chat_view.add_message("system", "Plan rejected. Operation cancelled.")
                self.post_message(StatusUpdate("done", "Cancelled"))
                return
            elif "Feedback" in selected:
                session.pending_state["type"] = "plan_feedback"
                chat_view.add_message("system", "Please enter your feedback in the input box below. If you submit without adding feedback, it will be automatically approved.")
                input_widget = self.query_one(ChatInput)
                input_widget.text = "Write your feedback here: "
                input_widget.move_cursor((0, len(input_widget.text)))
                return

        elif session.pending_state.get("type") == "file_write_permission":
            if "Write File" in selected:
                chat_view.add_message("user", "Write File")
                session.pending_state["type"] = "file_write_filename"
                files = session.pending_state.get("file_writes", [])
                default_path = files[0].get("path", "script.py") if files else "script.py"
                chat_view.add_message("system", "Please confirm or enter the filename to write to:")
                input_widget = self.query_one(ChatInput)
                input_widget.text = default_path
                input_widget.move_cursor((0, len(input_widget.text)))
                input_bar.hide_approval()
                return
            elif "Cancel" in selected:
                chat_view.add_message("user", "Cancel")
                session.pending_state = None
                chat_view.add_message("system", "File write skipped.")
                self.post_message(StatusUpdate("done", "Skipped"))
                return

        elif session.pending_state.get("type") == "file_write_exists":
            filename = session.pending_state.get("filename")
            content = session.pending_state.get("content")
            if "Overwrite" in selected:
                chat_view.add_message("user", "Overwrite")
                try:
                    self.file_service.write_file(filename, content)
                    chat_view.add_message("system", f"✓ File `{filename}` overwritten successfully!")
                    try:
                        self.query_one(DirectoryTree).reload()
                    except Exception:
                        pass
                except Exception as e:
                    chat_view.add_message("system", f"Error overwriting file: {e}")
                session.pending_state = None
                return
            elif "New File" in selected:
                chat_view.add_message("user", "New File")
                import re
                path = Path(filename)
                stem = path.stem
                suffix = path.suffix
                match = re.search(r"_(?P<num>\d+)$", stem)
                if match:
                    num = int(match.group("num")) + 1
                    new_stem = re.sub(r"_\d+$", f"_{num}", stem)
                else:
                    new_stem = f"{stem}_1"
                new_filename = str(path.parent / f"{new_stem}{suffix}")
                try:
                    full_path = self.file_service.resolve_safe_path(new_filename)
                    is_exists = full_path.exists()
                except Exception as e:
                    chat_view.add_message("system", f"Invalid incremented path: {e}")
                    session.pending_state = None
                    return
                if not is_exists:
                    try:
                        self.file_service.write_file(new_filename, content)
                        chat_view.add_message("system", f"✓ File `{new_filename}` created and written successfully!")
                        try:
                            self.query_one(DirectoryTree).reload()
                        except Exception:
                            pass
                    except Exception as e:
                        chat_view.add_message("system", f"Error writing file: {e}")
                    session.pending_state = None
                else:
                    chat_view.add_message("system", f"File `{new_filename}` also exists. How do you want to proceed?")
                    session.pending_state.update({
                        "filename": new_filename,
                    })
                    self.query_one(InputBar).show_approval(["1. Overwrite", "2. New File", "3. Cancel"])
                return
            elif "Cancel" in selected:
                chat_view.add_message("user", "Cancel")
                session.pending_state = None
                chat_view.add_message("system", "File write cancelled.")
                return

    @on(ChatInput.Submitted)
    async def on_input_submitted(self, event: ChatInput.Submitted) -> None:
        raw_value = event.value
        user_input = raw_value.strip()
        chat_view = self.query_one("#chat-view", ChatView)

        # Check pending state first
        if session.pending_state is not None:
            self.query_one(ChatInput).text = ""
            if session.pending_state.get("type") == "plan_feedback":
                feedback_str = user_input.replace("Write your feedback here:", "").strip()
                if not feedback_str or feedback_str == "Write your feedback here":
                    chat_view.add_message("user", "Approved (No feedback provided)")
                    state = session.pending_state
                    session.pending_state = None
                    self.run_generator_worker(session.get_messages())
                else:
                    chat_view.add_message("user", f"Feedback: {feedback_str}")
                    session.add_user_message(f"Please revise the plan based on this feedback: {feedback_str}")
                    state = session.pending_state
                    session.pending_state = None
                    self.swap_to_chat()
                    self.stream_response(feedback_str, bypass_history=False, route="new_task")
                return
            elif session.pending_state.get("type") == "file_write_filename":
                filename = user_input.strip()
                if not filename:
                    chat_view.add_message("system", "Filename cannot be empty. Please enter a valid filename.")
                    return
                try:
                    full_path = self.file_service.resolve_safe_path(filename)
                    is_exists = full_path.exists()
                except Exception as e:
                    chat_view.add_message("system", f"Invalid filename/path: {e}")
                    return
                content = session.pending_state.get("generated_code", "")
                if not is_exists:
                    try:
                        self.file_service.write_file(filename, content)
                        chat_view.add_message("system", f"✓ File `{filename}` created and written successfully!")
                        try:
                            self.query_one(DirectoryTree).reload()
                        except Exception:
                            pass
                    except Exception as e:
                        chat_view.add_message("system", f"Error writing file: {e}")
                    session.pending_state = None
                else:
                    session.pending_state.update({
                        "type": "file_write_exists",
                        "filename": filename,
                        "content": content,
                    })
                    chat_view.add_message("system", f"File `{filename}` already exists. How do you want to proceed?")
                    self.query_one(InputBar).show_approval(["1. Overwrite", "2. New File", "3. Cancel"])
                return
            else:
                chat_view.add_message("system", "Please use the option list to approve or cancel.")
                return

        if not user_input:
            return

        self.query_one(ChatInput).text = ""
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
                self.swap_to_chat()
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
                self.swap_to_chat()
                self.stream_response(user_input, bypass_history=False)

    # ── Streaming nodes that should display in chat ──────────────────────────
    _STREAMING_NODES = frozenset({"planner_node", "chat_node"})

    @work(exclusive=True)
    async def stream_response(self, user_input: str, bypass_history: bool, route: str | None = None) -> None:
        """Phase 1: classify → (chat | plan → generate)."""
        chat_view = self.query_one("#chat-view", ChatView)
        msg_id = f"msg-{uuid.uuid4()}"

        self.show_loading()
        try:
            self.query_one(StatusPanel).show_agent_loader("root_node")
        except Exception:
            pass

        import asyncio
        await asyncio.sleep(0.05)

        accumulated = ""
        first_token = False
        message_added = False
        generator_files = []
        generator_code = ""

        try:
            messages = (
                [HumanMessage(content=user_input)]
                if bypass_history
                else session.get_messages()
            )

            current_node = None
            should_pause = False
            initial_state = {"messages": messages}
            if route:
                initial_state["route"] = route

            async for chunk in phase1_graph.astream(
                initial_state,
                stream_mode=["messages", "updates", "debug"],
            ):
                if len(chunk) != 2:
                    continue
                event_type, payload = chunk

                if event_type == "debug" and isinstance(payload, dict):
                    if payload.get("type") in ("task:runs", "task:run", "task:new"):
                        task_data = payload.get("payload", {})
                        if isinstance(task_data, dict) and "name" in task_data:
                            node = task_data["name"]
                            if node and node != current_node and node not in ("__start__", "__end__", "start", "end"):
                                current_node = node
                                try:
                                    self.query_one(StatusPanel).show_agent_loader(node)
                                except Exception:
                                    pass
                    continue

                if event_type == "updates" and isinstance(payload, dict):
                    for node_name, node_update in payload.items():
                        if node_update is None:
                            continue
                        if node_name == "generator_node":
                            files = node_update.get("file_writes", [])
                            generator_files = files
                            filenames = ", ".join(f['path'] for f in files) if files else "script.py"
                            code_preview = node_update.get("generated_code", "")
                            generator_code = code_preview
                            diff_text = node_update.get("diff_text", "")
                            file_exists = node_update.get("file_exists", False)
                            lang = "python" if filenames.endswith(".py") else ""

                            if file_exists and diff_text:
                                preview_block = f"**Diff Generated for `{filenames}`:**\n```diff\n{diff_text}\n```"
                            else:
                                preview_block = f"**Code Generated for `{filenames}`:**\n```{lang}\n{code_preview}\n```" if code_preview else ""

                            chat_view.add_message("system", preview_block)
                            self.query_one(StatusPanel).mark_todos_completed()
                        elif node_name == "write_file_node":
                            if generator_files:
                                session.pending_state = {
                                    "type": "file_write_permission",
                                    "file_writes": generator_files,
                                    "generated_code": generator_code,
                                }
                                chat_view.add_message("system", "**Do you approve writing the generated file(s) to your workspace?**")
                                should_pause = True
                                break
                        if node_name == "root_node":
                            route = node_update.get("route", "")
                            if route:
                                try:
                                    if route in ("new_task", "edit_request"):
                                        next_node = "planner_node"
                                    elif route == "skip_plan":
                                        next_node = "chat_node"
                                    else:
                                        next_node = "generator_node"
                                    self.query_one(StatusPanel).show_agent_loader(next_node)
                                except Exception:
                                    pass
                        if node_name == "planner_node":
                            session.pending_state = {
                                "type": "plan_approval",
                                "messages": list(messages),
                                "user_input": user_input,
                            }
                            for todo in node_update.get("plan_todos", []):
                                self.post_message(StatusUpdate("todo", todo))
                            chat_view.add_message("system", "**Do you approve the execution plan?**")
                            should_pause = True
                            break
                    if should_pause:
                        break

                if event_type == "messages":
                    msg, metadata = payload
                    if metadata.get("langgraph_node", "") not in self._STREAMING_NODES:
                        continue
                    if "nostream" in metadata.get("tags", []):
                        continue
                    content = self._extract_content(msg)
                    if content:
                        if not first_token:
                            first_token = True
                            self.show_generating()
                            chat_view.add_message("ai", "", msg_id)
                            message_added = True
                        accumulated += content
                        chat_view.update_message(msg_id, accumulated)

            if message_added:
                chat_view.finalize_message(msg_id, accumulated)
                self.show_done()
            else:
                self.hide_loading()

            if not bypass_history and accumulated:
                session.add_ai_message(accumulated)

        except Exception as e:
            self.hide_loading()
            import traceback
            err_str = traceback.format_exc()
            self.post_message(StatusUpdate("error", f"Stream error: {e}"))
            if message_added:
                chat_view.update_message(msg_id, f"**Error:**\n```\n{err_str}\n```")
            else:
                chat_view.add_message("system", f"**Error:**\n```\n{err_str}\n```")
        finally:
            try:
                self.query_one(StatusPanel).mark_agent_done()
                if session.pending_state and session.pending_state.get("type") == "plan_approval":
                    self.query_one(InputBar).show_approval(["1. Approved", "2. Revise", "3. Cancel", "4. Feedback"])
                elif session.pending_state and session.pending_state.get("type") == "file_write_permission":
                    self.query_one(InputBar).show_approval(["1. Write File", "2. Cancel"])
            except Exception:
                pass

    @staticmethod
    def _extract_content(msg) -> str:
        content = getattr(msg, "content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "".join(
                p.get("text", "") if isinstance(p, dict) and p.get("type") == "text" else ""
                for p in content
            )
        return ""

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

    @work(exclusive=True)
    async def run_generator_worker(self, messages: list) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        msg_id = f"msg-{uuid.uuid4()}"

        self.show_loading()
        try:
            self.query_one(StatusPanel).show_agent_loader("generator_node")
        except Exception:
            pass

        accumulated = ""
        first_token = False
        message_added = False
        generator_files = []
        generator_code = ""
        should_pause = False

        try:
            async for chunk in phase1_graph.astream(
                {"messages": messages, "route": "skip_plan"},
                stream_mode=["messages", "updates", "debug"],
            ):
                if len(chunk) != 2:
                    continue
                event_type, payload = chunk

                if event_type == "updates" and isinstance(payload, dict):
                    for node_name, node_update in payload.items():
                        if node_name == "generator_node":
                            files = node_update.get("file_writes", [])
                            generator_files = files
                            filenames = ", ".join(f['path'] for f in files) if files else "script.py"
                            code_preview = node_update.get("generated_code", "")
                            generator_code = code_preview
                            diff_text = node_update.get("diff_text", "")
                            file_exists = node_update.get("file_exists", False)
                            lang = "python" if filenames.endswith(".py") else ""

                            if file_exists and diff_text:
                                preview_block = f"**Diff Generated for `{filenames}`:**\n```diff\n{diff_text}\n```"
                            else:
                                preview_block = f"**Code Generated for `{filenames}`:**\n```{lang}\n{code_preview}\n```" if code_preview else ""

                            chat_view.add_message("system", preview_block)
                            self.query_one(StatusPanel).mark_todos_completed()
                        elif node_name == "write_file_node":
                            if generator_files:
                                session.pending_state = {
                                    "type": "file_write_permission",
                                    "file_writes": generator_files,
                                    "generated_code": generator_code,
                                }
                                chat_view.add_message("system", "**Do you approve writing the generated file(s) to your workspace?**")
                                should_pause = True
                                break
                    if should_pause:
                        break

                if event_type == "messages":
                    msg, metadata = payload
                    if metadata.get("langgraph_node", "") not in self._STREAMING_NODES:
                        continue
                    if "nostream" in metadata.get("tags", []):
                        continue
                    content = self._extract_content(msg)
                    if content:
                        if not first_token:
                            first_token = True
                            self.show_generating()
                            chat_view.add_message("ai", "", msg_id)
                            message_added = True
                        accumulated += content
                        chat_view.update_message(msg_id, accumulated)

            if message_added:
                chat_view.finalize_message(msg_id, accumulated)
                self.show_done()
            else:
                self.hide_loading()

            if accumulated:
                session.add_ai_message(accumulated)

        except Exception as e:
            self.hide_loading()
            import traceback
            err_str = traceback.format_exc()
            self.post_message(StatusUpdate("error", f"Stream error: {e}"))
            if message_added:
                chat_view.update_message(msg_id, f"**Error:**\n```\n{err_str}\n```")
            else:
                chat_view.add_message("system", f"**Error:**\n```\n{err_str}\n```")
        finally:
            try:
                self.query_one(StatusPanel).mark_agent_done()
                if session.pending_state and session.pending_state.get("type") == "file_write_permission":
                    self.query_one(InputBar).show_approval(["1. Write File", "2. Cancel"])
            except Exception:
                pass

    def update_input_bar_ui(self) -> None:
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
            if file_panel.has_unsaved_changes:
                try:
                    target_path = str(self.file_service.resolve_safe_path(path).resolve())
                    current_path = str(self.file_service.resolve_safe_path(file_panel.current_file_path).resolve())
                    is_same_file = target_path == current_path
                except Exception:
                    is_same_file = False

                if not is_same_file:
                    chat_view.add_message(
                        "system",
                        "Warning: Unsaved changes in active editor. Save with /save or discard changes before opening another file."
                    )
                    self.post_message(StatusUpdate("warning", "Unsaved changes in editor"))
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
            if file_panel.has_unsaved_changes:
                try:
                    target_path = str(self.file_service.resolve_safe_path(path).resolve())
                    current_path = str(self.file_service.resolve_safe_path(file_panel.current_file_path).resolve())
                    is_same_file = target_path == current_path
                except Exception:
                    is_same_file = False

                if not is_same_file:
                    chat_view.add_message(
                        "system",
                        "Warning: Unsaved changes in active editor. Save with /save or discard changes before opening another file."
                    )
                    self.post_message(StatusUpdate("warning", "Unsaved changes in editor"))
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
            file_panel = self.query_one("#file-panel", FilePanel)
            if file_panel.has_unsaved_changes:
                try:
                    target_path = event.path.resolve()
                    current_path = self.file_service.resolve_safe_path(file_panel.current_file_path).resolve()
                    is_same_file = target_path == current_path
                except Exception:
                    is_same_file = False

                if not is_same_file:
                    chat_view = self.query_one("#chat-view", ChatView)
                    chat_view.add_message(
                        "system",
                        "Warning: Unsaved changes in active editor. Save with /save or discard changes before opening another file."
                    )
                    self.post_message(StatusUpdate("warning", "Unsaved changes in editor"))
                    return

            rel_path = event.path.relative_to(self.file_service.root)
            self.handle_file_command_by_name("open", str(rel_path))
        except Exception as e:
            chat_view = self.query_one("#chat-view", ChatView)
            chat_view.add_message("system", f"Error opening tree item: {str(e)}")
            self.post_message(StatusUpdate("error", str(e)))
if __name__ == "__main__":
    LataiApp().run()
