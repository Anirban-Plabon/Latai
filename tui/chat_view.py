from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Rule, Static
from tui.message import ChatMessage

LOADERS = {
    "loader1": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
    "loader2": "✳❇❈❋✽❋❈❇",
    "loader3": "✳❅❇❈❋✽❉❄❆❁❆❄❉✽❋❈❇❅",
    "loader4": "∙-⇢⇥>|",
    "loader5": "➸➹➴➵➶➷➸➹➴➵➶➷",
    "loader6": "°⍤☄☀☉⌖",
    "loader7": "⣾⣽⣻⢿⡿⣟⣯⣷",
    "loader8": "⣀⣄⣤⣦⣴⣶⣷⣿",
    "loader9": "∙▪⧈⧇⧆⊛⊚⊙⊡⊠⊡⊙⊚⊛⧆⧇⧈▪",
    "loader10": "⌜⌝⌟⌞",
    "loader11": "⌽⍉⦲",
    "loader12": "☉✺✳⌖⑅∙⑅⌖✳✺",
    "loader13": "┤ ┘ ┴ └ ├ ┌ ┬ ┐",
    "loader14": "▥▨▤▧",
    "loader15": ".●⬤⁂∘°∘∵",
    "loader16": "⊞⊠",
    "loader17": "⧰⧱⧳⧯⧮⧲",
    "loader18": "⦶⊘⊖⦸",
    "loader19": "⏄⏅",
    "loader20": "⬖⬘⬗⬙",
    "loader21": "◫◰",
    "loader22": "◧▥▨◩▨▤⬒▤▨◪▨▥◨▥▨◩▨▤⬓▤▨◪▨▥",
    "loader23": "◧◩⬒◪◨◩⬓◪",
    "loader23": "◧⬒◨⬓",
    "loader24": "⚆⚇⚉⚈",
    "loader25": "◸◹◿◺",
    "loader26": "◩⬔◪⬕",
    "loader27": "🀲🀷🂍🁪🀸🁛🁩🁤",
    "loader28": "🁤🁥🁦🁧🁨🁩🁯🁵🁻🂁🂇🂍🂆🁿🁸🁱🁪🁣",
    "loader29": "🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🂪🂩🂨🂧🂦🂥🂤🂣🂢🂡",
    "loader30": "🃡🃤🃬🃥",
    "loader31": "🃦🃧🃨🃩"
}
ACTIVE_LOADER = "loader28"

class ThinkingIndicator(Static):
    def on_mount(self) -> None:
        self.frames = LOADERS.get(ACTIVE_LOADER, LOADERS["loader1"])
        self.frame_index = 0
        
        # Colors transitioning from Light Pink (#FFB6C1) to Light Blue (#ADD8E6) and back
        self.animation_colors = [
            "#FFB6C1", "#E5BED1", "#CCC6E1", "#B2CEF1", "#ADD8E6",
            "#ADD8E6", "#B2CEF1", "#CCC6E1", "#E5BED1", "#FFB6C1", "#FFB6C1"
        ]
        
        self.update_timer = self.set_interval(0.08, self.update_frame)

    def update_frame(self) -> None:
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.styles.color = self.animation_colors[self.frame_index % len(self.animation_colors)]
        self.update(f"{self.frames[self.frame_index]}  AI is thinking...")

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
            
    def show_loading(self) -> None:
        indicator = ThinkingIndicator("⁎ AI is thinking...", id="loading-indicator", classes="loading-text")
        self.mount(indicator)
        self.call_after_refresh(self.scroll_end, animate=False)
        
    def hide_loading(self) -> None:
        try:
            indicator = self.query_one("#loading-indicator")
            indicator.remove()
        except Exception:
            pass
