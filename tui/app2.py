import uuid
from textual.app import App, ComposeResult
from textual.widgets import Input, Static, Rule, Button, OptionList
from textual.containers import Horizontal, Vertical
from textual import work

from tui.chat_view import ChatView
from tui.input_bar import InputBar
from tui.command_menu import CommandMenu
from commands.base import is_command, parse_command
from commands import model as cmd_model
from services.session import session
from agent.graph import graph
from langchain_core.messages import HumanMessage

class CustomHeader(Static):
    def compose(self) -> ComposeResult:
        yield Static("⛏️ craftChat", id="app-title")

class LataiApp(App):
    """
    'ascii', 'blank', 'block', 'dashed', 'double', 'heavy', 'hidden', 'hkey', 'inner', 'none', 'outer', 'panel', 'round', 'solid',
   │   'tab', 'tall', 'thick', 'vkey', or 'wide'"""
    CSS = """
    LataiApp {
        background: transparent;
        layers: base overlay;
    }
    
    CustomHeader {
        dock: top;
        height: 1;
        background: transparent;
        color: white;
        text-style: bold;
        content-align: center middle;
        padding-top: 1;
    }

    #app-title {
        background: transparent;
    }

    ChatView {
        height: 1fr;
        background: transparent;
        padding: 0;
        overflow-y: scroll;
        scrollbar-gutter: stable;
        scrollbar-size-vertical: 1;
        scrollbar-color: #ADD8E6;
        scrollbar-color-hover: #ADD8E6;
        scrollbar-color-active: #ADD8E6;
        scrollbar-background: transparent;
    }

    ChatMessage {
        margin: 1 1 1 1;
        padding: 1 1 1 1;
        height: auto;
        background: transparent;
    }

    ChatMessage.user {
        background: #2a2a2a;
        border-left: tall #F4C2C2;
    }

    ChatMessage.ai {
        background: transparent;
        border-left: tall #FFB6C1;
    }

    .message-row {
        height: auto;
    }

    .message-role    { color: white; text-style: bold; width: auto; min-width: 5; }
    .message-content { color: #e0e0e0; width: 1fr; height: auto; }

    Markdown {
        height: auto;
        overflow-y: hidden;
        background: transparent;
        margin: 0;
        padding: 0;
    }
    
    InputBar {
        height: auto;
        min-height: 3;
        width: 1fr;
        background: transparent;
        padding: 0 1;
        border: round #555555;
        align: left middle;
    }
    
    .rd-row {
        height: auto;
        min-height: 1;
        width: 1fr;
    }

    .rd-prefix {
        color: $text-muted;
        width: 2;
        content-align: left middle;
        text-style: bold;
    }

    Input {
        border: none;
        background: transparent;
        width: 1fr;
        height: auto;
        min-height: 1;
    }
    
    Input:focus {
        border: none;
    }

    #cmd-menu-btn {
        min-width: 5;
        width: auto;
        min-height: 1;
        height: 1;
        padding: 0;
        margin: 0;
        border: none;
        background: transparent;
        color: #888888;
        text-style: bold;
        content-align: center middle;
    }

    #cmd-menu-btn:hover {
        color: white;
    }
    
    .bottom-zone {
        dock: bottom;
        height: auto;
        background: transparent;
    }
    
    .zone-separator {
        color: #444444;
        margin: 0;
    }
    
    .input-wrapper {
        layout: horizontal;
        height: 3;
        margin: 0 2 1 2;
    }
    
    Rule {
        color: #444444;
        margin: 1 0;
    }
    
    .loading-text {
        color: #aaaaaa;
        margin: 1 0;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield CustomHeader()
        yield ChatView(id="chat-view")
        
        with Vertical(classes="bottom-zone"):
            yield Rule(classes="zone-separator")
            with Horizontal(classes="input-wrapper"):
                yield InputBar()
        yield CommandMenu(id="cmd-menu")

    def on_mount(self) -> None:
        self.query_one(InputBar).focus_input()
        
        # Post initial system message
        chat_view = self.query_one("#chat-view", ChatView)
        # Pink: #FFB6C1, Blue: #ADD8E6
        welcome_markup = (
            "[#FFB6C1]  ____________  [/][#ADD8E6]____________  [/]\n"
            "[#FFB6C1]||    //\\\\    ||[/][#ADD8E6]    //\\\\    ||[/]\n"
            "[#FFB6C1]||   //  \\\\   ||[/][#ADD8E6]   //  \\\\   ||[/]\n"
            "[#FFB6C1]||  //    \\\\  ||[/][#ADD8E6]  //    \\\\  ||   [/]Welcome to LATAI !!\n"
            "[#FFB6C1]|| //      \\\\ ||[/][#ADD8E6] //      \\\\ ||[/]\n"
            "[#FFB6C1]||//        \\\\||[/][#ADD8E6]//        \\\\||[/]"
        )
        chat_view.add_message("system", Static(welcome_markup))
        chat_view.add_message("system", f"Active model: {session.provider}/{session.model_name}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cmd-menu-btn":
            menu = self.query_one(CommandMenu)
            if menu.has_class("-visible"):
                menu.remove_class("-visible")
            else:
                menu.add_class("-visible")
                menu.query_one(OptionList).focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        menu = self.query_one(CommandMenu)
        menu.remove_class("-visible")
        option_id = event.option_id
        
        chat_view = self.query_one("#chat-view", ChatView)
        
        if option_id == "quit":
            self.exit()
        elif option_id == "theme":
            self.dark = not self.dark
        elif option_id == "model_gemini":
            session.set_model("gemini", "gemini-2.0-flash")
            chat_view.add_message("system", "Switched to gemini-2.0-flash")
        elif option_id == "model_openai":
            session.set_model("openai", "gpt-4o")
            chat_view.add_message("system", "Switched to gpt-4o")
        elif option_id == "model_mock":
            session.set_model("mock", "test")
            chat_view.add_message("system", "Switched to mock model")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value.strip()
        if not user_input:
            return

        event.input.value = ""
        chat_view = self.query_one("#chat-view", ChatView)
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
        msg_id = f"msg-{uuid.uuid4()}"
        
        chat_view.show_loading()

        accumulated_content = ""
        first_chunk_received = False
        message_added = False

        try:
            if bypass_history:
                messages = [HumanMessage(content=user_input)]
            else:
                messages = session.get_messages()

            state = {"messages": messages}

            async for msg, metadata in graph.astream(state, stream_mode="messages"):
                # Extract text content from message chunk
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
                        chat_view.hide_loading()
                        chat_view.add_message("ai", "", msg_id)
                        message_added = True
                        
                    accumulated_content += content
                    chat_view.update_message(msg_id, accumulated_content)

            if not message_added:
                chat_view.hide_loading()
                if accumulated_content:
                    chat_view.add_message("ai", accumulated_content, msg_id)
                else:
                    chat_view.add_message("system", "No response from model.")

            if not bypass_history:
                session.add_ai_message(accumulated_content)

        except Exception as e:
            chat_view.hide_loading()
            if not message_added:
                chat_view.add_message("system", f"Error: {str(e)}", msg_id)
            else:
                chat_view.update_message(msg_id, f"Error: {str(e)}")

if __name__ == "__main__":
    app = LataiApp()
    app.run()
