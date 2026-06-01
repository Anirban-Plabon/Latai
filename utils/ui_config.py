from textual.theme import Theme

DEV_LOCAL_THEME = {
    "primary": "#90FDAE",    # Light Pink
    "secondary": "#C091FF",   # Light Blue
    "loader_thinking": "loader74",
    "loader_generating": "loader73",
}

# Custom developer theme mapping DEV_LOCAL_THEME colors and Latai's background hexes
dev_color_theme = Theme(
    name="dev_color_theme",
    primary=DEV_LOCAL_THEME["primary"],
    secondary=DEV_LOCAL_THEME["secondary"],
    accent=DEV_LOCAL_THEME["secondary"],  # Accent usually used for highlights, mirroring secondary
    background="#0d1117",
    surface="#161b22",
    panel="#1e1e1e",
    warning="#fbbf24",
    success="#3fb950",
    error="#f85149",
    foreground="#e0e0e0",
    dark=True,
)
