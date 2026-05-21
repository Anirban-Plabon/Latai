from typing import TYPE_CHECKING, Dict, List, Tuple
from textual.widgets import Static
from services.session import session
import time
import math

if TYPE_CHECKING:
    from tui.app import LataiApp
    from tui.chat_view import ChatView

# --- Unified Logo Assets ---

LOGOS: Dict[str, List[str]] = {
    "v1": [
        "⣶⣶⣶⣶⣶⣶⣶⣶  ⣶⣶⣶⣶⣶⣶⣶⣶",
        "⣿⡇ ⣾⣷ ⢸⣿  ⣿⡇ ⣾⣷ ⢸⣿",
        "⣿⡇⢰⡟⢻⡆⢸⣿  ⣿⡇⢰⡟⢻⡆⢸⣿",
        "⣿⣧⣿⠁⠈⣿⣼⣿  ⣿⣧⣿⠁⠈⣿⣼⣿",
        "⣿⣿⠃⠀⠀⠘⣿⣿  ⣿⣿⠃⠀⠀⠘⣿⣿",
        "⣿⠏⠀⠀⠀⠀⠹⣿  ⣿⠏⠀⠀⠀⠀⠹⣿"
    ],
    "v2": [
        "⣿⡇  ⣶⣶⣶⣶  ⣶⣶⣶⣶  ⢸⣿",
        "⣿⡇ ⣾⣷ ⢸⣿  ⣿  ⣾⣷   ",
        "⣿⡇⢰⡟⢻⡆⢸⣿  ⣿⡇⢰⡟⢻⡆⢸⣿",
        "⣿⣧⣿⠁⠈⣿⣼⣿  ⣿⣧⣿⠁⠈⣿⣼⣿",
        "⣿⣿⠃⠀⠀⠘⣿⣿  ⣿⣿⠃⠀⠀⠘⣿⣿",
        "⣿⠏⠀⠀⠀⠀⠹⣿  ⣿⠏⠀⠀⠀⠀⠹⣿"
    ],
    "v3": [
        "⣿⡇  ⣶⣶⣶⣶  ⣶⣶⣶⣶  ⢸⣿",
        "⣿⡇ ⣾⣷  ⣿  ⣿  ⣾⣷   ",
        "⣿⡇⢰⡟⢻⡆ ⣿  ⣿ ⢰⡟⢻⡆⢸⣿",
        "⣿⣧⣿⠁⠈⣿⣼⣿  ⣿⣧⣿⠁⠈⣿⣼⣿",
        "⣿⣿⠃⠀⠀⠘⣿⣿  ⣿⣿⠃⠀⠀⠘⣿⣿",
        "⣿⠏⠀⠀⠀⠀⠹⣿  ⣿⠏⠀⠀⠀⠀⠹⣿"
    ],
    "v4": [
        "⣿⣿     ⣶⣶⣶⣶  ⣶⣶⣶⣶  ⢸⣿",
        "⣿⣿    ⣾⣷  ⣿  ⣿  ⣾⣷   ",
        "⣿⣿   ⢰⡟⢻⡆ ⣿  ⣿ ⢰⡟⢻⡆⢸⣿",
        "⣿⣿   ⣿⠁⠈⣿⣼⣿  ⣿⣧⣿⠁⠈⣿⣼⣿",
        "⣿⣿  ⣿⠃⠀⠀⠘⣿⣿  ⣿⣿⠃⠀⠀⠘⣿⣿",
        "⣿⣿⣿⣿⠏⠀⠀⠀⠀⠹⣿  ⣿⠏⠀⠀⠀⠀⠹⣿"
    ],
    "v5": [
        "██    ██████████████████    ██",
        "██    ████    ██    ████    ██",
        "██   ██  ██   ██   ██  ██   ██",
        "██  ██    ██  ██  ██    ██  ██",
        "██ ██      ██ ██ ██      ██ ██",
        "████        ██████        ████",
    ]
}

DEFAULT_LOGO = "v5"
WELCOME_TEXT = "   Welcome to LATAI !!"

def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Converts #RRGGBB to (R, G, B) tuple."""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def get_interpolated_hex(start_rgb: Tuple[int, int, int], end_rgb: Tuple[int, int, int], factor: float) -> str:
    """Returns hex string for a color between two RGB tuples."""
    f = max(0.0, min(1.0, factor))
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * f)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * f)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * f)
    return f"#{r:02x}{g:02x}{b:02x}"

def animate_welcome(
    app: "LataiApp", 
    chat_view: "ChatView", 
    color_start: str = "#FFB6C1", 
    color_end: str = "#ADD8E6",
    logo_key: str = DEFAULT_LOGO
) -> None:
    """Mounts and animates the welcome logo with a unified structure and dynamic colors."""
    logo_lines = LOGOS.get(logo_key, LOGOS[DEFAULT_LOGO])
    rgb_start = hex_to_rgb(color_start)
    rgb_end = hex_to_rgb(color_end)
    
    welcome_widget = Static("")
    chat_view.add_message("system", welcome_widget)

    logo_width = max(len(line) for line in logo_lines)
    total_width = logo_width + len(WELCOME_TEXT)

    start_time = time.time()

    def render_frame(progress: int) -> str:
        elapsed = time.time() - start_time
        lines = []
        for i, logo_line in enumerate(logo_lines):
            full_content = logo_line.ljust(logo_width)
            if i == 3:
                full_content += WELCOME_TEXT
            
            visible = full_content[:progress]
            colored_line = ""
            
            for j, char in enumerate(visible):
                if char.isspace():
                    colored_line += char
                    continue
                
                # Spatial factor across the unified logo
                spatial_factor = j / logo_width if logo_width > 0 else 0
                
                # Dynamic shimmer
                shift = math.sin(elapsed * 4 + spatial_factor * 2) * 0.2
                factor = spatial_factor + shift
                
                color = get_interpolated_hex(rgb_start, rgb_end, factor)
                colored_line += f"[{color}]{char}[/]"
            
            lines.append(colored_line)
        return "\n".join(lines)

    app._welcome_progress = 0

    def step_animation() -> None:
        app._welcome_progress += 1
        welcome_widget.update(render_frame(app._welcome_progress))

        if app._welcome_progress >= total_width:
            app._welcome_timer.stop()
            chat_view.add_message(
                "system",
                f"Active model: {session.provider}/{session.model_name}"
            )

    app._welcome_timer = app.set_interval(0.02, step_animation)
