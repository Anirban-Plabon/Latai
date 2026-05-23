# /term Command Implementation — Task Tracker

- `[x]` Modify `services/session.py` — Add `self.is_terminal_mode: bool = False`
- `[x]` Create `commands/term.py` — Create terminal command execution handler
- `[x]` Modify `tui/app.css` — Set `.rd-prefix` to `width: auto`
- `[x]` Modify `tui/app.py` — Wire `/term` routing, background worker, and UI prefix/placeholder updates
- `[x]` Verify — Test manual command execution and toggle persistent mode
- `[x]` Run `graphify update .` to index the changes
