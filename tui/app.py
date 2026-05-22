import uuid
from textual.app import App, ComposeResult
from textual.widgets import Input, Rule, Button
from textual.containers import Horizontal, Vertical
from textual import work
from langchain_core.messages import HumanMessage

from tui.chat_view import ChatView
from tui.input_bar import InputBar
from tui.command_menu import CommandMenu, MENU_MODELS, MENU_THEMES, MENU_COMMANDS
from commands.base import is_command, parse_command
from commands import model as cmd_model
from services.session import session
from agent.graph import graph
from res.ui.welcome import animate_welcome
from res.ui.loaders import ThinkingIndicator
from tui.header import CustomHeader
from tui.footer import CustomFooter


class LataiApp(App):
    """The main Latai TUI chat application class."""

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
    ]

    def compose(self) -> ComposeResult:
        yield CustomHeader()
        yield ChatView(id="chat-view")

        with Vertical(classes="bottom-zone"):
            yield Rule(classes="zone-separator")
            yield Vertical(id="loading-container")
            with Horizontal(classes="input-wrapper"):
                yield InputBar()

        yield CustomFooter()
        yield CommandMenu(id="cmd-menu")

    def on_mount(self) -> None:
        self.query_one(InputBar).focus_input()
        chat_view = self.query_one("#chat-view", ChatView)
        animate_welcome(
            self, 
            chat_view, 
            color_start=self.DEV_LOCAL_THEME["primary"], 
            color_end=self.DEV_LOCAL_THEME["secondary"]
        )

    def show_loading(self) -> None:
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

    def on_command_menu_theme_selected(self, event: CommandMenu.ThemeSelected) -> None:
        self.theme = event.theme_name
        self.query_one("#chat-view", ChatView).add_message(
            "system", f"Theme set to: {event.theme_name}"
        )

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
            if cmd == "model":
                result = cmd_model.execute(args)
                chat_view.add_message("system", result)
            elif cmd == "ask":
                self.stream_response(args, bypass_history=True)
            else:
                chat_view.add_message("system", f"Unknown command: /{cmd}")
        else:
            session.add_user_message(user_input)
            self.stream_response(user_input, bypass_history=False)

    @work(exclusive=True)
    async def stream_response(self, user_input: str, bypass_history: bool) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        msg_id    = f"msg-{uuid.uuid4()}"

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

            if not bypass_history:
                session.add_ai_message(accumulated_content)

        except Exception as e:
            self.hide_loading()
            if not message_added:
                chat_view.add_message("system", f"Error: {str(e)}", msg_id)
            else:
                chat_view.update_message(msg_id, f"Error: {str(e)}")


if __name__ == "__main__":
    LataiApp().run()