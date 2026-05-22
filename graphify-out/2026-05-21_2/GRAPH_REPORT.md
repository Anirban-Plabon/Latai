# Graph Report - Latai  (2026-05-21)

## Corpus Check
- 33 files · ~4,520 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 176 nodes · 195 edges · 41 communities (29 shown, 12 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 29 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `508dfc9a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_TUI Application Core|TUI Application Core]]
- [[_COMMUNITY_Command Interface|Command Interface]]
- [[_COMMUNITY_Chat View Display|Chat View Display]]
- [[_COMMUNITY_UI Components|UI Components]]
- [[_COMMUNITY_LangGraph Definition|LangGraph Definition]]
- [[_COMMUNITY_Session State Management|Session State Management]]
- [[_COMMUNITY_LLM Provider Factory|LLM Provider Factory]]
- [[_COMMUNITY_LLM Base Implementation|LLM Base Implementation]]
- [[_COMMUNITY_Gemini CLI Settings|Gemini CLI Settings]]
- [[_COMMUNITY_Graph Compilation|Graph Compilation]]
- [[_COMMUNITY_Debug Utilities|Debug Utilities]]
- [[_COMMUNITY_Main Entry Point|Main Entry Point]]
- [[_COMMUNITY_Anthropic Provider|Anthropic Provider]]
- [[_COMMUNITY_Gemini Provider|Gemini Provider]]
- [[_COMMUNITY_OpenRouter Provider|OpenRouter Provider]]
- [[_COMMUNITY_OpenAI Provider|OpenAI Provider]]
- [[_COMMUNITY_Session Management|Session Management]]
- [[_COMMUNITY_Main Execution|Main Execution]]
- [[_COMMUNITY_LLM Abstraction|LLM Abstraction]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 30|Community 30]]

## God Nodes (most connected - your core abstractions)
1. `LataiApp` - 17 edges
2. `CommandMenu` - 17 edges
3. `ChatView` - 14 edges
4. `LataiApp` - 12 edges
5. `InputBar` - 11 edges
6. `Project: LangGraph Chat TUI` - 11 edges
7. `Session` - 8 edges
8. `ChatMessage` - 8 edges
9. `get_llm()` - 7 edges
10. `CustomHeader` - 7 edges

## Surprising Connections (you probably didn't know these)
- `LataiApp` --implements--> `Token-by-Token Streaming`  [INFERRED]
  tui/app.py → GEMINI.md
- `LataiApp` --conceptually_related_to--> `UI Layer Isolation`  [INFERRED]
  tui/app.py → GEMINI.md
- `get_llm()` --references--> `Mock LLM Implementation`  [INFERRED]
  /mnt/l/projects/Latai/services/llm.py → services/providers/mock.py
- `get_llm()` --implements--> `LLM Provider Abstraction`  [INFERRED]
  /mnt/l/projects/Latai/services/llm.py → services/llm.py
- `CustomHeader` --uses--> `CommandMenu`  [INFERRED]
  tui/app.py → /mnt/l/projects/Latai/tui/command_menu.py

## Hyperedges (group relationships)
- **LLM Orchestration Layer** — services_llm_get_llm, services_providers_mock_mockchatmodel, agent_graph_llm_node [INFERRED 0.85]
- **Centralized State Management** — services_session_session_instance, agent_state_agentstate, agent_graph_llm_node [INFERRED 0.80]
- **TUI Orchestration Pattern** — tui_app_lataiapp, tui_chat_view_chatview, tui_input_bar_inputbar, tui_command_menu_commandmenu [EXTRACTED 1.00]
- **Swappable LLM Provider Pattern** — arch_llm_factory, utils_config_get_api_key, tui_command_menu_commandmenu [INFERRED 0.90]

## Communities (41 total, 12 thin omitted)

### Community 0 - "TUI Application Core"
Cohesion: 0.11
Nodes (10): App, Token-by-Token Streaming, UI Layer Isolation, Static, CustomHeader, LataiApp, 'ascii', 'blank', 'block', 'dashed', 'double', 'heavy', 'hidden', 'hkey', 'inner, CustomHeader (+2 more)

### Community 1 - "Command Interface"
Cohesion: 0.20
Nodes (7): Message, CommandMenu, ModelSelected, Show the menu, optionally jumping straight to a sub-menu., Hide and reset to main menu., Centered overlay command palette.      Navigation:       • Main menu  →  Models, ThemeSelected

### Community 2 - "Chat View Display"
Cohesion: 0.16
Nodes (5): Container, ScrollableContainer, ChatView, ThinkingIndicator, ChatMessage

### Community 3 - "UI Components"
Cohesion: 0.27
Nodes (4): is_command(), parse_command(), stream_response(), stream_response()

### Community 4 - "LangGraph Definition"
Cohesion: 0.18
Nodes (7): build_graph(), llm_node(), AgentState, execute(), Runtime Model Swapping, Global Session Singleton, TypedDict

### Community 6 - "LLM Provider Factory"
Cohesion: 0.17
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 7 - "LLM Base Implementation"
Cohesion: 0.36
Nodes (4): BaseChatModel, get_model(), _llm_type(), MockChatModel

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (6): 1. `gemini_llm_node`, Graph Structure, LangGraph Simple Agent Specification (Gemini LLM Node), Nodes, Overview, State Schema

### Community 30 - "Community 30"
Cohesion: 0.20
Nodes (6): LLM Provider Abstraction, get_llm(), Factory to return the appropriate LangChain ChatModel instance., Mock LLM Implementation, get_api_key(), Retrieve the API key for a given provider from environment variables.

## Knowledge Gaps
- **20 isolated node(s):** `BeforeTool`, `Identity`, `Code Style`, `Instructions`, `Architecture Rules` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LataiApp` connect `TUI Application Core` to `Community 27`, `Command Interface`, `Chat View Display`, `UI Components`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `CommandMenu` connect `Command Interface` to `TUI Application Core`, `Chat View Display`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `ChatView` connect `Chat View Display` to `TUI Application Core`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `LataiApp` (e.g. with `Token-by-Token Streaming` and `UI Layer Isolation`) actually correct?**
  _`LataiApp` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CommandMenu` (e.g. with `CustomHeader` and `CustomHeader`) actually correct?**
  _`CommandMenu` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ChatView` (e.g. with `CustomHeader` and `CustomHeader`) actually correct?**
  _`ChatView` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `LataiApp` (e.g. with `ChatView` and `InputBar`) actually correct?**
  _`LataiApp` has 4 INFERRED edges - model-reasoned connections that need verification._