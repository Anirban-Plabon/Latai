from textual.app import App, ComposeResult
from textual.widgets import Markdown
from textual.widgets.markdown import MarkdownFenceWithCopy
import re

CSS = """
Markdown {
    background: #111111;
}
Syntax .syntax--generic.syntax--inserted {
    background: rgba(70, 254, 122, 0.5);
    color: #46FE7A;
}
Syntax .syntax--generic.syntax--deleted {
    background: rgba(248, 81, 73, 0.5);
    color: #f85149;
}
"""

class TestApp(App):
    CSS = CSS
    def compose(self) -> ComposeResult:
        md = """
```diff
+ padded inserted line                      
- padded deleted line                       
```
"""
        yield Markdown(md)

if __name__ == "__main__":
    app = TestApp()
    app.run()
