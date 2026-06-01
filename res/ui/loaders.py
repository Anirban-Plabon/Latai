from typing import List, Tuple
from textual.widgets import Static

LOADERS = {
    "loader1": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
    "loader2": "✳❇❈❋✽❋❈❇",
    "loader2_1": "✳❈✽❋❈❇",
    "loader3": "✳❅❇❈❋✽❉❄❆❁❆❄❉✽❋❈❇❅",
    "loader4": "∙∙⇢⇥>|",
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
    "loader23": "◧⬒◨⬓",
    "loader24": "⚆⚇⚉⚈",
    "loader25": "◸◹◿◺",
    "loader26": "◩⬔◪⬕",
    "loader27": "🀲🀷🂍🁪🀸🁛🁩🁤",
    "loader28": "🁤🁥🁦🁧🁨🁩⁯🁵🁻🂁🂇🂍🂆🁿🁸🁱🁪🁣",
    "loader29": "🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🂪🂩🂨🂧🂦🂥🂤🂣🂢₡",
    "loader30": "🃡🃤🃬🃥",
    "loader31": "🃦🃧🃨🃩",
    "loader32": "ᖰᖱᖲᖳ",
    "loader33": "ᚁᚂᚃᚄᚅᚊᚉᚈᚇᚆ",
    "loader34": "ᚐᚑᚒᚓᚔ",
    "loader35": "ᚋᚌᚍᚎᚏ",
    "loader36": "ᚨᚩᚪᚫ",
    "loader37": "⁕⁑⁂⁖⁘⁛⁜",
    "loader38": "↑↗→↘↓↙←↖",
    "loader39": "∬∭∰∯∮∲∳∱",
    "loader40": "⏀⏁⏂⏅⏄⏃",
    "loader41": "░ ▒ ▓ ▒",
    "loader42": "▖▘▝▙▚▛▜▝▞▟▗",
    "loader43": "▗▞▙▚▝▗▘▛▜▟▞",
    "loader44": "☂☔",
    "loader45": "𐂂𐂃𐂄𐂅",
    "loader46": "𑪞𑪟𑪠𑪢",
    "loader47": "⠁⠂⠄⡀⠂⠁⠂⠄⡀⠂",
    "loader48": "𒀠𒀡𒀢𒀣𒀤𒀥𒀦𒀧運",
    "loader49": "𒉒𒉔𒉕𒉓𒀭𒀮𒀯",
    "loader50": "🌍🌎🌏",
    "loader51": "বরকধঝ",
    "loader52": "𖦹꩜🌀𖣠",
    "loader53": "◯ ☽ ◑ ● ◐ ❨ ◯",
    "loader54": "𐦂𖨆𐀪𖠋𐀪𐀪",
    "loader55": "🀢🀣🀦🀤",
    "loader56": "𖡼𖤣▧𖡼𓋼𖤣▥𓋼𓍊",
    "loader57": "𓅰 𓅬 𓅭 𓅮 𓅯",
    "loader58": "𒅒𒈔𒅒𒇫𒄆",
    "loader59": ":･ﾟ✧:･.☽˚｡･ﾟ✧:･.:",
    "loader60": "𖡼.𖤣▧𖡼.𖤣▧",
    "loader61": "⏹🅾⏺🔴⚪",   
    "loader62": "𓆝 𓆟 𓆞 𓆝 𓆟",
    "loader63": [
        "    ●    \n  ●   ●  \n●       ●",
        "  ●   ●  \n●       ●\n  ●   ●  ",
        "●       ●\n  ●   ●  \n    ●    ",
        "  ●   ●  \n    ●    \n  ●   ●  ",
    ],
    "loader64": [
        "▁▃▅█▅▃▁",
        "▃▅█▅▃▁▁",
        "▅█▅▃▁▁▃",
        "█▅▃▁▁▃▅",
    ],
    "loader641": [
        "▁▄█▄▁",
        "▄█▄▁▁",
        "█▄▁▁▄",
        "▄▁▁▄█",
        "▁▁▄█▄",
    ],
    "loader642": [
        "⣀⣠⣾⣷⣄⣀",
        "⣠⣾⣷⣄⣀⣠",
        "⣾⣷⣄⣀⣠⣾",
        "⣷⣄⣀⣠⣾⣷",
        "⣄⣀⣠⣾⣷⣄",
    ],
    "loader643": [
        "⣀⣴⣦⣀",
        "⣴⣦⣀⣴",
        "⣦⣀⣴⣦",
        "⣀⣴⣦⣀",
    ],
    "loader65": [
        "○   ○\n \\ /\n  ○\n / \\\n○   ○",
        "●   ○\n \\ /\n  ○\n / \\\n○   ○",
        "○   ●\n \\ /\n  ○\n / \\\n○   ○",
        "○   ○\n \\ /\n  ●\n / \\\n○   ○",
        "○   ○\n \\ /\n  ○\n / \\\n●   ●",
        "○   ○\n \\ /\n  ○\n / \\\n○   ●",
    ],
    "loader66": [
        "○○○\n○○○\n○○○",
        "●○○\n○○○\n○○●",
        "○●○\n○○●\n●○○",
        "○○●\n●○○\n○●○",
        "○○○\n○●○\n○○○",
    ],
    "loader67": [
        "█            |",
        "██           |",
        "●██          |",
        "○●██         |",
        "○○●██        |",
        "○○○●██       |",
        "○○○○●██      |",
        "○○○○○○●██    |",
        "○○○○○○○●██   |",
        "○○○○○○○○●██  |",
        "○○○○○○○○○●██ |",
    ],
    "loader68": [
        "▄             ├",
        ".▄▄           ├",
        "..▄▄▄         ├",
        "...▄▄▄▄       ├",
        "....▄▄▄▄▄     ├",
        ".....▄▄▄▄▄▄   ├",
        "......▄▄▄▄▄▄▄ ├",
    ],
    "loader69": [
        "▄             ├",
        ".▄▄           ├",
        "..▄▄▄         ├",
        "...▄▄▄▄       ├",
        "....▄▄▄▄▄     ├",
        ".....▄▄▄▄▄▄   ├",
        "......▄▄▄▄▄▄▄ ├",
    ],
    
    "loader70": [
        "▄             ",
        ".▄▄           ",
        "..▄▄▄         ",
        "...▄▄▄▄       ",
        "....▄▄▄▄▄     ",
        ".....▄▄▄▄▄▄   ",
        "......▄▄▄▄▄▄▄ ",  
    ],
    "loader71": [
        "▄             ",
        ".▄▄           ",
        "..▄▄▄         ",
        "...▄▄▄▄       ",
        "....▄▄▄▄▄     ",
        ".....▄▄▄▄▄▄   ",
        "......▄▄▄▄▄▄▄ ",
        ".......▄▄▄▄▄▄ ",
        "........▄▄▄▄▄ ",
        ".........▄▄▄▄ ",
        "..........▄▄▄ ",
        "...........▄▄ ",
        "............▄ ",
    ],
    
    "loader72": [
        "▄             ",
        ".▄▄           ",
        "..▄▄▄         ",
        "...▄▄▄▄       ",
        "....▄▄▄▄▄     ",
        ".....▄▄▄▄▄▄   ",
        "......▄▄▄▄▄▄▄ ",
        ".......▄▄▄▄▄▄ ",
        "........▄▄▄▄▄ ",
        ".........▄▄▄▄ ",
        "..........▄▄▄ ",
        "...........▄▄ ",
        "............▄ ",
        "...........▄▄ ",
        "..........▄▄▄ ",
        ".........▄▄▄▄ ",
        "........▄▄▄▄▄ ",
        ".......▄▄▄▄▄▄ ",
        "......▄▄▄▄▄▄▄ ",
        ".....▄▄▄▄▄▄   ",
        "....▄▄▄▄▄     ",
        "...▄▄▄▄       ",
        "..▄▄▄         ",
        ".▄▄           ",
    ],
    
    
    
    "loader73": [
        "█             ",
        "∙██           ",
        "∙∙███         ",
        "∙∙∙████       ",
        "∙∙∙∙█████     ",
        "∙∙∙∙∙██████   ",
        "∙∙∙∙∙∙███████ ",
        "∙∙∙∙∙∙∙██████ ",
        "∙∙∙∙∙∙∙∙█████ ",
        "∙∙∙∙∙∙∙∙∙████ ",
        "∙∙∙∙∙∙∙∙∙∙███ ",
        "∙∙∙∙∙∙∙∙∙∙∙██ ",
        "∙∙∙∙∙∙∙∙∙∙∙∙█ ",
        "∙∙∙∙∙∙∙∙∙∙∙██ ",
        "∙∙∙∙∙∙∙∙∙∙███ ",
        "∙∙∙∙∙∙∙∙∙████ ",
        "∙∙∙∙∙∙∙∙█████ ",
        "∙∙∙∙∙∙∙██████ ",
        "∙∙∙∙∙∙███████ ",
        "∙∙∙∙∙██████   ",
        "∙∙∙∙█████     ",
        "∙∙∙████       ",
        "∙∙███         ",
        "∙██           ",
    ],
    
    "loader74": [
        "❯            ",
        "∙▒❯          ",
        "∙∙▒▒❯        ",
        "∙∙∙▒▒▒❯      ",
        "∙∙∙∙▒▒▒▒❯    ",
        "∙∙∙∙∙▒▒▒▒▒❯  ",
        "∙∙∙∙∙∙▒▒▒▒▒▒❯",
        "∙∙∙∙∙∙∙▒▒▒▒▒❯",
        "∙∙∙∙∙∙∙∙▒▒▒▒❯",
        "∙∙∙∙∙∙∙∙∙▒▒▒❯",
        "∙∙∙∙∙∙∙∙∙∙▒▒❯",
        "∙∙∙∙∙∙∙∙∙∙∙▒❯",
        "∙∙∙∙∙∙∙∙∙∙∙∙❯",
        "∙∙∙∙∙∙∙∙∙∙∙▒❮",
        "∙∙∙∙∙∙∙∙∙∙▒▒❮",
        "∙∙∙∙∙∙∙∙∙▒▒▒❮",
        "∙∙∙∙∙∙∙∙▒▒▒▒❮",
        "∙∙∙∙∙∙∙▒▒▒▒▒❮",
        "∙∙∙∙∙∙▒▒▒▒▒▒❮",
        "∙∙∙∙∙▒▒▒▒▒❮  ",
        "∙∙∙∙▒▒▒▒❮    ",
        "∙∙∙▒▒▒❮      ",
        "∙∙▒▒❮        ",
        "∙▒❮          ",
        "▒❮           ",
    ],

    "loader75": [
        "⧯            ",
        "∙⧮⧯          ",
        "∙∙⧮⧮⧯        ",
        "∙∙∙⧮⧮⧮⧯      ",
        "∙∙∙∙⧮⧮⧮⧮⧯    ",
        "∙∙∙∙∙⧮⧮⧮⧮⧮⧯  ",
        "∙∙∙∙∙∙⧮⧮⧮⧮⧮⧮⧯",
        "∙∙∙∙∙∙∙⧮⧮⧮⧮⧮⧯",
        "∙∙∙∙∙∙∙∙⧮⧮⧮⧮⧯",
        "∙∙∙∙∙∙∙∙∙⧮⧮⧮⧯",
        "∙∙∙∙∙∙∙∙∙∙⧮⧮⧯",
        "∙∙∙∙∙∙∙∙∙∙∙⧮⧯",
        "∙∙∙∙∙∙∙∙∙∙∙∙⧯",
        "∙∙∙∙∙∙∙∙∙∙∙⧮⧯",
        "∙∙∙∙∙∙∙∙∙∙⧮⧮⧯",
        "∙∙∙∙∙∙∙∙∙⧮⧮⧮⧯",
        "∙∙∙∙∙∙∙∙⧮⧮⧮⧮⧯",
        "∙∙∙∙∙∙∙⧮⧮⧮⧮⧮⧯",
        "∙∙∙∙∙∙⧮⧮⧮⧮⧮⧮⧯",
        "∙∙∙∙∙⧮⧮⧮⧮⧮⧯  ",
        "∙∙∙∙⧮⧮⧮⧮⧯    ",
        "∙∙∙⧮⧮⧮⧯      ",
        "∙∙⧮⧮⧯        ",
        "∙⧮⧯          ",
    ],

    "loader76":[
        "◩",
        "-◩⬔",
        "--◩⬔◪",
        "---◩⬔◪⬕",
        "----◩⬔◪⬕◩",
        "-----◩⬔◪⬕◩⬔",
        "------◩⬔◪⬕◩⬔◪",
        "-------◩⬔◪⬕◩⬔◪⬕",
        "--------◩⬔◪⬕◩⬔◪",
        "---------◩⬔◪⬕◩⬔",
        "----------◩⬔◪⬕◩",
        "-----------◩⬔◪⬕",
        "------------◩⬔◪",
        "-------------◩⬔",
        "--------------◩",
        "-------------◩⬔",
        "------------◩⬔◪",
        "-----------◩⬔◪⬕",
        "----------◩⬔◪⬕◩",
        "---------◩⬔◪⬕◩⬔",
        "--------◩⬔◪⬕◩⬔◪",
        "-------◩⬔◪⬕◩⬔◪⬕",
        "------◩⬔◪⬕◩⬔◪",
        "-----◩⬔◪⬕◩⬔",
        "----◩⬔◪⬕◩",
        "---◩⬔◪⬕",
        "--◩⬔◪",
        "-◩⬔",
        "◩"
    ],
    
    "loader77":[
        "◩",
        "-◩⬔",
        "--◩⬔◪",
        "---◩⬔◪⬕",
        "----◩⬔◪⬕◩",
        "-----◩⬔◪⬕◩⬔",
        "------◩⬔◪⬕◩⬔◪",
        "-------◩⬔◪⬕◩⬔◪⬕",
        "------◩⬔◪⬕◩⬔◪",
        "-----◩⬔◪⬕◩⬔",
        "----◩⬔◪⬕◩",
        "---◩⬔◪⬕",
        "--◩⬔◪",
        "-◩⬔",
        "◩"
    ],
    "loader78":[
        "◧",
        "-◧⬒",
        "--◧⬒◨",
        "---◧⬒◨⬓",
        "----◧⬒◨⬓◧",
        "-----◧⬒◨⬓◧⬒",
        "------◧⬒◨⬓◧⬒◨",
        "-------◧⬒◨⬓◧⬒◨⬓",
        "--------◧⬒◨⬓◧⬒◨",
        "---------◧⬒◨⬓◧⬒",
        "----------◧⬒◨⬓◧",
        "-----------◧⬒◨⬓",
        "------------◧⬒◨",
        "-------------◧⬒",
        "--------------◧",
        "-------------◧⬒",
        "------------◧⬒◨",
        "-----------◧⬒◨⬓",
        "----------◧⬒◨⬓◧",
        "---------◧⬒◨⬓◧⬒",
        "--------◧⬒◨⬓◧⬒◨",
        "-------◧⬒◨⬓◧⬒◨⬓",
        "------◧⬒◨⬓◧⬒◨",
        "-----◧⬒◨⬓◧⬒",
        "----◧⬒◨⬓◧",
        "---◧⬒◨⬓",
        "--◧⬒◨",
        "-◧⬒",
        "◧"
    ],
    
    "loader79":[
        "◧                  |",
        "-◧⬒               |",
        "--◧⬒◨             |"
        "---◧⬒◨⬓          |",
        "----◧⬒◨⬓◧        |",
        "-----◧⬒◨⬓◧⬒",
        "------◧⬒◨⬓◧⬒◨",
        "-------◧⬒◨⬓◧⬒◨⬓",
        "------◧⬒◨⬓◧⬒◨",
        "-----◧⬒◨⬓◧⬒",
        "----◧⬒◨⬓◧",
        "---◧⬒◨⬓",
        "--◧⬒◨",
        "-◧⬒",
        "◧"
    ],
  
}


ACTIVE_LOADER = "loader74"


class ThinkingIndicator(Static):
    """Loading indicator with animated loader frames and elapsed time."""

    def __init__(self, *args, loader_name: str = ACTIVE_LOADER, label: str = "Thinking...", **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._loader_name = loader_name
        self._label = label
        import time
        self._start_time: float = time.time()

    def on_mount(self) -> None:
        self.frames: list[str] = LOADERS.get(self._loader_name, LOADERS[ACTIVE_LOADER])
        self.frame_index: int = 0
        self.color_cycle_index: int = 0

        from utils.ui_config import DEV_LOCAL_THEME
        primary = DEV_LOCAL_THEME.get("primary", "#FFB6C1")
        secondary = DEV_LOCAL_THEME.get("secondary", "#ADD8E6")

        self.animation_colors = self._generate_color_steps(primary, secondary, 10)
        self._render_frame()
        self.update_timer = self.set_interval(0.08, self._render_frame)

    def stop(self) -> None:
        if hasattr(self, "update_timer"):
            self.update_timer.stop()

    def change_state(self, loader_name: str, label: str, reset_timer: bool = False) -> None:
        self._loader_name = loader_name
        self._label = label
        self.frames = LOADERS.get(self._loader_name, LOADERS[ACTIVE_LOADER])
        self.frame_index = 0
        if reset_timer:
            import time
            self._start_time = time.time()
        self.stop()
        self._render_frame()
        self.update_timer = self.set_interval(0.08, self._render_frame)

    def _generate_color_steps(self, start_hex: str, end_hex: str, steps: int) -> List[str]:
        def hex_to_rgb(h: str) -> Tuple[int, int, int]:
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

        s_rgb = hex_to_rgb(start_hex)
        e_rgb = hex_to_rgb(end_hex)
        palette: list[str] = []

        for i in range(steps + 1):
            f = i / steps
            r = int(s_rgb[0] + (e_rgb[0] - s_rgb[0]) * f)
            g = int(s_rgb[1] + (e_rgb[1] - s_rgb[1]) * f)
            b = int(s_rgb[2] + (e_rgb[2] - s_rgb[2]) * f)
            palette.append(rgb_to_hex((r, g, b)))

        for i in range(steps - 1, 0, -1):
            f = i / steps
            r = int(s_rgb[0] + (e_rgb[0] - s_rgb[0]) * f)
            g = int(s_rgb[1] + (e_rgb[1] - s_rgb[1]) * f)
            b = int(s_rgb[2] + (e_rgb[2] - s_rgb[2]) * f)
            palette.append(rgb_to_hex((r, g, b)))

        return palette

    def _render_frame(self) -> None:
        """Render a single animation frame."""
        import time
        try:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.color_cycle_index = (self.color_cycle_index + 1) % len(self.animation_colors)
            color = self.animation_colors[self.color_cycle_index]
            elapsed = time.time() - self._start_time
            frame_char = self.frames[self.frame_index]
            markup = f"[{color}]{frame_char}[/] {self._label}  {elapsed:.1f}s"
            self.update(markup)
        except Exception:
            pass

    def mark_done(self) -> None:
        """Mark the indicator as completed."""
        self.stop()
        import time
        elapsed = time.time() - self._start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        done_text = self._label.replace("Working", "Done")
        markup = f"[green bold]✓[/] {done_text} {time_str}"
        self.update(markup)
