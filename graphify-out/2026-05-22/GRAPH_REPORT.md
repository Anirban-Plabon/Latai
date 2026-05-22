# Graph Report - Latai  (2026-05-22)

## Corpus Check
- 39 files · ~5,736 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 246 nodes · 313 edges · 36 communities (31 shown, 5 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `83151d79`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_LangGraph Orchestration|LangGraph Orchestration]]
- [[_COMMUNITY_TUI Core & Header|TUI Core & Header]]
- [[_COMMUNITY_Command Menu & Messaging|Command Menu & Messaging]]
- [[_COMMUNITY_Chat View Rendering|Chat View Rendering]]
- [[_COMMUNITY_UI Resources (LoadersWelcome)|UI Resources (Loaders/Welcome)]]
- [[_COMMUNITY_Command Parsing|Command Parsing]]
- [[_COMMUNITY_LLM Provider Factory|LLM Provider Factory]]
- [[_COMMUNITY_LLM Abstractions|LLM Abstractions]]
- [[_COMMUNITY_Custom Markdown Extensions|Custom Markdown Extensions]]
- [[_COMMUNITY_Gemini CLI Configuration|Gemini CLI Configuration]]
- [[_COMMUNITY_App Lifecycle|App Lifecycle]]
- [[_COMMUNITY_Mock Provider|Mock Provider]]
- [[_COMMUNITY_OpenAI Integration|OpenAI Integration]]
- [[_COMMUNITY_OpenRouter Integration|OpenRouter Integration]]
- [[_COMMUNITY_Chat Agent Specification|Chat Agent Specification]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]

## God Nodes (most connected - your core abstractions)
1. `CommandMenu` - 17 edges
2. `get_api_key()` - 16 edges
3. `LataiApp` - 15 edges
4. `Session` - 12 edges
5. `LataiApp` - 11 edges
6. `get_configured_models()` - 11 edges
7. `Project: LangGraph Chat TUI` - 11 edges
8. `Project: LangGraph Chat TUI` - 11 edges
9. `ChatView` - 10 edges
10. `InputBar` - 10 edges

## Surprising Connections (you probably didn't know these)
- `get_llm()` --calls--> `get_api_key()`  [INFERRED]
  services/llm.py → utils/config.py
- `get_llm()` --calls--> `get_default_key_name()`  [INFERRED]
  services/llm.py → utils/config.py
- `llm_node()` --calls--> `get_llm()`  [EXTRACTED]
  agent/graph.py → services/llm.py
- `execute()` --calls--> `Session`  [EXTRACTED]
  commands/model.py → services/session.py
- `get_llm()` --calls--> `get_base_url()`  [INFERRED]
  services/llm.py → utils/config.py

## Communities (36 total, 5 thin omitted)

### Community 0 - "LangGraph Orchestration"
Cohesion: 0.10
Nodes (12): App, is_command(), parse_command(), Static, CustomHeader, LataiApp, 'ascii', 'blank', 'block', 'dashed', 'double', 'heavy', 'hidden', 'hkey', 'inner, stream_response() (+4 more)

### Community 1 - "TUI Core & Header"
Cohesion: 0.13
Nodes (9): Markdown, MarkdownFence, ScrollableContainer, ChatView, CustomMarkdown, MarkdownFenceWithCopy, Markdown widget that uses our custom code block class., A code block with a 'Copy' button in the top right. (+1 more)

### Community 2 - "Command Menu & Messaging"
Cohesion: 0.12
Nodes (9): build_graph(), Compiled Agent Graph, llm_node(), AgentState, execute(), Debug Graph Script, Welcome Animation Logic, Session (+1 more)

### Community 3 - "Chat View Rendering"
Cohesion: 0.20
Nodes (11): Container, Message, CommandMenu, ModelSelected, Show the menu, optionally jumping straight to a sub-menu., Hide and reset to main menu., Show the menu, optionally jumping straight to a sub-menu., Hide and reset to main menu. (+3 more)

### Community 4 - "UI Resources (Loaders/Welcome)"
Cohesion: 0.16
Nodes (7): ThinkingIndicator, animate_welcome(), get_interpolated_hex(), hex_to_rgb(), Converts #RRGGBB to (R, G, B) tuple., Returns hex string for a color between two RGB tuples., Mounts and animates the welcome logo with a unified structure and dynamic colors

### Community 5 - "Command Parsing"
Cohesion: 0.18
Nodes (10): get_llm(), Factory to return the appropriate LangChain ChatModel instance., Factory to return the appropriate LangChain ChatModel instance., Anthropic Provider, Gemini Provider, get_base_url(), Return base_url for providers like ollama that use URL instead of API key., Return base_url for providers like ollama that use URL instead of API key. (+2 more)

### Community 6 - "LLM Provider Factory"
Cohesion: 0.07
Nodes (39): get_api_key(), get_available_providers(), get_configured_models(), get_default_model(), get_default_provider(), get_installed_ollama_models(), _get_provider_config(), is_provider_configured() (+31 more)

### Community 7 - "LLM Abstractions"
Cohesion: 0.33
Nodes (3): BaseChatModel, get_model(), MockChatModel

### Community 8 - "Custom Markdown Extensions"
Cohesion: 0.29
Nodes (6): 1. `gemini_llm_node`, Graph Structure, LangGraph Simple Agent Specification (Gemini LLM Node), Nodes, Overview, State Schema

### Community 25 - "App Lifecycle"
Cohesion: 0.17
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.17
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 34 - "Community 34"
Cohesion: 0.14
Nodes (14): get_default_key_name(), load_config(), Return the first available key name for a provider., Write current config back to config.yaml., Write current config back to config.yaml., Load config.yaml. Call once at app entry point., Write current config back to config.yaml., Load environment config from .env. Call once at app entry point. (+6 more)

### Community 35 - "Community 35"
Cohesion: 0.40
Nodes (5): Set base_url for a provider in memory., Set base_url for a provider in memory., Set base_url for a provider in memory., Set base_url for a provider in memory., set_provider_base_url()

## Knowledge Gaps
- **31 isolated node(s):** `BeforeTool`, `Identity`, `Code Style`, `Instructions`, `Architecture Rules` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LataiApp` connect `LangGraph Orchestration` to `TUI Core & Header`, `Command Menu & Messaging`, `Chat View Rendering`, `UI Resources (Loaders/Welcome)`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `get_configured_models()` connect `LLM Provider Factory` to `Chat View Rendering`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Why does `get_api_key()` connect `LLM Provider Factory` to `Community 33`, `Command Parsing`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `CommandMenu` (e.g. with `CustomHeader` and `LataiApp`) actually correct?**
  _`CommandMenu` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_api_key()` (e.g. with `get_llm()` and `GEMINI.md`) actually correct?**
  _`get_api_key()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `LataiApp` (e.g. with `CommandMenu` and `command_menu.py`) actually correct?**
  _`LataiApp` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LataiApp` (e.g. with `InputBar` and `CommandMenu`) actually correct?**
  _`LataiApp` has 3 INFERRED edges - model-reasoned connections that need verification._