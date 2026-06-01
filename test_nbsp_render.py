from textual.app import App, ComposeResult
from textual.widgets import Markdown

CSS = """
Markdown { background: #111111; }
Syntax .syntax--generic.syntax--inserted { background: rgba(70, 254, 122, 0.5); color: #46FE7A; }
Syntax .syntax--generic.syntax--deleted { background: rgba(248, 81, 73, 0.5); color: #f85149; }
"""

class TestApp(App):
    CSS = CSS
    def compose(self) -> ComposeResult:
        md = "```diff\n+ added line" + "\xa0" * 30 + "\n- deleted line" + "\xa0" * 30 + "\n```"
        yield Markdown(md)

if __name__ == "__main__":
    app = TestApp()
    app.run(headless=True, size=(80, 24))
