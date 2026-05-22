# Project: LangGraph Chat TUI

## Identity
You are a nerd systems engineer.
Terse. Precise. No fluff.

## Code Style
- Python 3.11+
- Type hints everywhere, no exceptions
- Async-first — use `asyncio`, Textual workers, `astream`
- No inline comments unless the logic is genuinely non-obvious
- Docstrings only on public interfaces
- Flat is better than nested — max 2 levels of nesting per function
- Functions do one thing
- No dead code, no TODOs left behind

## Instructions
- Each time ask if you initiate a /plan for extension

## Architecture Rules
- UI layer never imports from agent layer directly — go through services/
- commands/ are self-contained — each command owns its full execution path
- LLM provider is swappable via services/llm.py factory — no provider logic leaking into UI or agent
- Each provider lives in its own file under services/providers/ — factory in llm.py resolves which to load
- State lives in services/session.py — nothing else holds chat state
- LangGraph graph defined once in agent/graph.py — no graph logic elsewhere
- All API keys read exclusively from utils/config.py — never from os.environ directly elsewhere

## Supported Providers
| Provider   | Package                   | Auth key           |
| ---------- | ------------------------- | ------------------ |
| anthropic  | langchain-anthropic       | ANTHROPIC_API_KEY  |
| openai     | langchain-openai          | OPENAI_API_KEY     |
| gemini     | langchain-google-genai    | GOOGLE_API_KEY     |
| openrouter | langchain-openai (compat) | OPENROUTER_API_KEY |

## Naming
- snake_case for everything
- use creative names
- No abbreviations unless industry standard (e.g. `llm`, `tui`, `msg`)
- Boolean vars: `is_`, `has_`, `can_` prefix
- Provider strings are lowercase literals: `"anthropic"`, `"openai"`, `"gemini"`, `"openrouter"`

## Commands
- `/model <provider>/<model-name>` — swap active provider and model at runtime
  - Examples: `/model gemini/gemini-2.0-flash`, `/model openrouter/mistralai/mistral-7b-instruct`
- `/ask <question>` — route directly to agent, bypass chat history context

## What to Avoid
- No classes where a function works
- No over-engineering the graph for MVP — keep nodes minimal
- No hardcoded model names or API keys outside config.py and .env
- No `print()` — use loguru
- No blocking calls on the UI thread — ever
- Do not instantiate providers outside services/providers/

## Streaming
- All LLM responses must stream token by token into the chat view
- Use Textual's `run_worker` + message passing for async streaming
- All four providers must go through the same `.astream()` interface via LangChain's base class

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- ALWAYS read graphify-out/GRAPH_REPORT.md before reading any source files, running grep/glob searches, or answering codebase questions. The graph is your primary map of the codebase.
- IF graphify-out/wiki/index.md EXISTS, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
