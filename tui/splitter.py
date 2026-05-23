from textual.events import MouseDown, MouseMove, MouseUp
from textual.widgets import Static


class VerticalSplitter(Static):
    """A draggable vertical splitter widget to resize adjacent panels."""

    DEFAULT_CSS = """
    VerticalSplitter {
        width: 1;
        height: 100%;
        background: #161b22;
        color: #30363d;
        content-align: center middle;
    }
    VerticalSplitter:hover {
        background: #21262d;
        color: #8b949e;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__("┃", **kwargs)
        self._dragging: bool = False

    def on_mouse_down(self, event: MouseDown) -> None:
        self.capture_mouse()
        self._dragging = True

    def on_mouse_move(self, event: MouseMove) -> None:
        if self._dragging:
            screen_width = self.app.size.width
            mouse_x = event.screen_x

            min_main_width = 30
            min_status_width = 20

            new_main_width = mouse_x
            new_status_width = screen_width - new_main_width - 1

            if new_main_width >= min_main_width and new_status_width >= min_status_width:
                self.app.query_one("#main-panel").styles.width = new_main_width
                self.app.query_one("#status-panel").styles.width = new_status_width

    def on_mouse_up(self, event: MouseUp) -> None:
        self.release_mouse()
        self._dragging = False
