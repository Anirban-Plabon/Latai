from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Rule, Static
from tui.message import ChatMessage
from res.ui.loaders import ThinkingIndicator


# class ChatView(ScrollableContainer):
#     def add_message(self, role: str, content: str, msg_id: str | None = None) -> ChatMessage:
#         msg = ChatMessage(role, content, id=msg_id)
#         if role == "user":
#             msg.add_class("user")
#         elif role == "ai":
#             msg.add_class("ai")
#         elif role == "system":
#             msg.add_class("system")
            
#         self.mount(msg)
#         self.call_after_refresh(self.scroll_end, animate=False)
#         return msg

#     def update_message(self, msg_id: str, new_content: str) -> None:
#         try:
#             msg = self.query_one(f"#{msg_id}", ChatMessage)
#             msg.content = new_content
#             self.call_after_refresh(self.scroll_end, animate=False)
#         except Exception:
#             pass
            
#     def show_loading(self) -> None:
#         self.app.show_loading()
        
#     def hide_loading(self) -> None:
#         self.app.hide_loading()



class ChatView(ScrollableContainer):
    def add_message(self, role: str, content: str, msg_id: str | None = None) -> ChatMessage:
        msg = ChatMessage(role, content, id=msg_id)
        if role == "user":
            msg.add_class("user")
        elif role == "ai":
            msg.add_class("ai")
        elif role == "system":
            msg.add_class("system")
            
        self.mount(msg)
        self.call_after_refresh(self.scroll_end, animate=False)
        return msg

    def update_message(self, msg_id: str, new_content: str) -> None:
        try:
            msg = self.query_one(f"#{msg_id}", ChatMessage)
            msg.content = new_content
            self.call_after_refresh(self.scroll_end, animate=False)
        except Exception:
            pass