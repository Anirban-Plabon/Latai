# tui/command_menu.py
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option
from textual.widgets import OptionList as _OL  # noqa — keep for type hints
from textual.reactive import reactive
from textual.message import Message

# ── Data ──────────────────────────────────────────────────────────────────────

TEXTUAL_THEMES = [
    "textual-dark",
    "textual-light",
    "nord",
    "gruvbox",
    "catppuccin-mocha",
    "catppuccin-latte",
    "tokyo-night",
    "monokai",
    "dracula",
    "solarized-light",
    "solarized-dark",
]

AVAILABLE_MODELS = [
    ("Gemini 2.0 Flash",   "model_gemini"),
    ("GPT-4o  (OpenAI)",   "model_openai"),
    ("Mock    (test)",     "model_mock"),
]

AVAILABLE_COMMANDS = [
    ("/ask", ""),
    ("/model", ""),
    ("/models", ""),
    ("/themes", ""),
    ("/commands", ""),
]

MENU_MAIN     = "main"
MENU_MODELS   = "models"
MENU_THEMES   = "themes"
MENU_COMMANDS = "commands"


# ── Widget ────────────────────────────────────────────────────────────────────

class CommandMenu(Container):
    """
    Centered overlay command palette.

    Navigation:
      • Main menu  →  Models / Themes / Commands sub-menus
      • Esc        →  back one level (or close from main)
      • /models | /themes | /commands  →  jump straight to sub-menu

    Messages posted to app:
      • CommandMenu.ModelSelected(option_id)
      • CommandMenu.ThemeSelected(theme_name)
    """

    # ── Messages ──────────────────────────────────────────────────────────────

    class ModelSelected(Message):
        def __init__(self, option_id: str) -> None:
            super().__init__()
            self.option_id = option_id

    class ThemeSelected(Message):
        def __init__(self, theme_name: str) -> None:
            super().__init__()
            self.theme_name = theme_name

    # ── State ─────────────────────────────────────────────────────────────────

    current_menu: reactive[str] = reactive(MENU_MAIN)

    # ── CSS ───────────────────────────────────────────────────────────────────

    DEFAULT_CSS = """
    /* Full-screen dark scrim — acts as the backdrop */
    CommandMenu {
        layer: overlay;
        width: 100%;
        height: 100%;
        background: $background 50%;   /* semi-transparent dark veil */
        display: none;
        align: center middle;
    }

    CommandMenu.-visible {
        display: block;
    }

    /* The floating popup card */
    .menu-box {
        width: 52;
        height: auto;
        max-height: 24;
        background: $surface-lighten-1;
    }

    /* Header strip inside the card */
    .menu-header {
        width: 1fr;
        height: 1;
        background: $surface-darken-2;
        color: $accent;
        text-style: bold;
        content-align: center middle;
        padding: 0 1;
    }

    /* Dim hint line (Esc binding) */
    .menu-hint {
        width: 1fr;
        height: 1;
        background: $surface-darken-1;
        color: $text-muted;
        content-align: left middle;
        padding: 0 2;
    }

    /* Option list fills remaining space */
    OptionList {
        background: $surface;
        border: $panel;
        height: auto;
        max-height: 18;
        margin: 1 2 1 2;
        outline: none;
    }

    
    
    """

    # ── Composition ───────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        with Vertical(classes="menu-box"):
            yield Static("", id="menu-header", classes="menu-header")
            yield Static("", id="menu-hint",   classes="menu-hint")
            yield OptionList(id="menu-options",compact = True)

    def on_mount(self) -> None:
        self._build_menu(MENU_MAIN)

    # ── Public API ────────────────────────────────────────────────────────────

    def open(self, menu: str = MENU_MAIN) -> None:
        """Show the menu, optionally jumping straight to a sub-menu."""
        self._build_menu(menu)
        self.add_class("-visible")

    def close(self) -> None:
        """Hide and reset to main menu."""
        self.remove_class("-visible")
        self._build_menu(MENU_MAIN)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _build_menu(self, menu: str) -> None:
        self.current_menu = menu

        header = self.query_one("#menu-header", Static)
        hint   = self.query_one("#menu-hint",   Static)
        ol     = self.query_one("#menu-options", OptionList)
        ol.clear_options()
        ol.remove_class("info-list")

        if menu == MENU_MAIN:
            header.update("Command Menu")
            hint.update("Esc  close")
            ol.add_options([
                Option("Models",   id="goto_models"),
                Option("Themes",   id="goto_themes"),
                Option("Commands", id="goto_commands"),
                Option("─" * 36, id="sep", disabled=True),
                Option("✕  Quit",      id="quit"),
            ])

        elif menu == MENU_MODELS:
            header.update("Select Model")
            hint.update("Esc  back")
            for label, opt_id in AVAILABLE_MODELS:
                ol.add_option(Option(label, id=opt_id))

        elif menu == MENU_THEMES:
            header.update("Select Theme")
            hint.update("Esc  back")
            for theme in TEXTUAL_THEMES:
                ol.add_option(Option(theme, id=f"theme__{theme}"))

        elif menu == MENU_COMMANDS:
            header.update("Available Commands")
            hint.update("Esc  back")
            ol.add_class("info-list")
            for cmd, desc in AVAILABLE_COMMANDS:
                ol.add_option(Option(f"{cmd:<30}  {desc}", id=f"cmdref__{cmd.split()[0]}"))

        ol.focus()

    # ── Event handlers ────────────────────────────────────────────────────────

    def on_key(self, event) -> None:
        if event.key == "escape":
            if self.current_menu == MENU_MAIN:
                self.close()
            else:
                self._build_menu(MENU_MAIN)
            event.stop()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        oid = event.option_id or ""

        # ── Navigation ────────────────────────────────────────────────────────
        if   oid == "goto_models":   self._build_menu(MENU_MODELS)
        elif oid == "goto_themes":   self._build_menu(MENU_THEMES)
        elif oid == "goto_commands": self._build_menu(MENU_COMMANDS)
        elif oid == "quit":          self.app.exit()

        # ── Model selection ───────────────────────────────────────────────────
        elif oid in ("model_gemini", "model_openai", "model_mock"):
            self.post_message(self.ModelSelected(oid))
            self.close()

        # ── Theme selection ───────────────────────────────────────────────────
        elif oid.startswith("theme__"):
            self.post_message(self.ThemeSelected(oid[len("theme__"):]))
            self.close()

        # ── Commands are read-only info; no action ────────────────────────────
        elif oid.startswith("cmdref__"):
            pass