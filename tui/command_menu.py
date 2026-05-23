# tui/command_menu.py
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option
from textual.widgets import OptionList as _OL  # noqa — keep for type hints
from textual.reactive import reactive
from textual.message import Message

# ── Data ──────────────────────────────────────────────────────────────────────

from utils.config import get_configured_models

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

AVAILABLE_COMMANDS = [
    ("/ask", "Route directly to agent, bypass history"),
    ("/model", "Swap provider and model at runtime"),
    ("/models", "Show models selection menu"),
    ("/themes", "Show themes selection menu"),
    ("/commands", "Show available commands list"),
    ("/tree [glob]", "Show project directory tree"),
    ("/open <path>", "Open a file in read-only viewer"),
    ("/edit <path>", "Open a file in editable TextArea"),
    ("/save", "Save current editor buffer"),
    ("/close", "Close the file panel and return to chat"),
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
            configured = get_configured_models()
            if not configured:
                ol.add_option(Option("No providers configured", id="no_models", disabled=True))
            else:
                current_provider = None
                for provider, label, model in configured:
                    if provider != current_provider:
                        current_provider = provider
                        ol.add_option(Option(f"── {provider.upper()} ──", id=f"sep_{provider}", disabled=True))
                    opt_id = f"model__{provider}__{model}"
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
        elif oid.startswith("model_"):
            self.post_message(self.ModelSelected(oid))
            self.close()

        # ── Theme selection ───────────────────────────────────────────────────
        elif oid.startswith("theme__"):
            self.post_message(self.ThemeSelected(oid[len("theme__"):]))
            self.close()

        # ── Commands are read-only info; no action ────────────────────────────
        elif oid.startswith("cmdref__"):
            pass