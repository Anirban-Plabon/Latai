from textual.containers import ScrollableContainer
from tui.message import ChatMessage


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