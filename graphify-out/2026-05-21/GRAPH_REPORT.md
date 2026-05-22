# Graph Report - Latai  (2026-05-20)

## Corpus Check
- 33 files · ~4,030 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 149 nodes · 171 edges · 30 communities (24 shown, 6 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 29 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2ec551c8`
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
- [[_COMMUNITY_Session Management|Session Management]]
- [[_COMMUNITY_Main Execution|Main Execution]]
- [[_COMMUNITY_LLM Abstraction|LLM Abstraction]]
- [[_COMMUNITY_Community 27|Community 27]]

## God Nodes (most connected - your core abstractions)
1. `LataiApp` - 16 edges
2. `CommandMenu` - 16 edges
3. `ChatView` - 14 edges
4. `LataiApp` - 12 edges
5. `Project: LangGraph Chat TUI` - 11 edges
6. `InputBar` - 10 edges
7. `ChatMessage` - 8 edges
8. `Session` - 7 edges
9. `CustomHeader` - 7 edges
10. `CustomHeader` - 7 edges

## Surprising Connections (you probably didn't know these)
- `LataiApp` --implements--> `Token-by-Token Streaming`  [INFERRED]
  tui/app.py → GEMINI.md
- `LataiApp` --conceptually_related_to--> `UI Layer Isolation`  [INFERRED]
  tui/app.py → GEMINI.md
- `llm_node()` --references--> `Global Session Singleton`  [EXTRACTED]
  agent/graph.py → services/session.py
- `get_llm()` --calls--> `get_api_key()`  [INFERRED]
  services/llm.py → utils/config.py
- `llm_node()` --calls--> `get_llm()`  [EXTRACTED]
  agent/graph.py → services/llm.py

## Hyperedges (group relationships)
- **LLM Orchestration Layer** — services_llm_get_llm, services_providers_mock_mockchatmodel, agent_graph_llm_node [INFERRED 0.85]
- **Centralized State Management** — services_session_session_instance, agent_state_agentstate, agent_graph_llm_node [INFERRED 0.80]
- **TUI Orchestration Pattern** — tui_app_lataiapp, tui_chat_view_chatview, tui_input_bar_inputbar, tui_command_menu_commandmenu [EXTRACTED 1.00]
- **Swappable LLM Provider Pattern** — arch_llm_factory, utils_config_get_api_key, tui_command_menu_commandmenu [INFERRED 0.90]

## Communities (30 total, 6 thin omitted)

### Community 0 - "TUI Application Core"
Cohesion: 0.12
Nodes (10): App, Token-by-Token Streaming, UI Layer Isolation, is_command(), parse_command(), LataiApp, 'ascii', 'blank', 'block', 'dashed', 'double', 'heavy', 'hidden', 'hkey', 'inner, stream_response() (+2 more)

### Community 1 - "Command Interface"
Cohesion: 0.20
Nodes (7): Message, CommandMenu, ModelSelected, Show the menu, optionally jumping straight to a sub-menu., Hide and reset to main menu., Centered overlay command palette.      Navigation:       • Main menu  →  Models, ThemeSelected

### Community 2 - "Chat View Display"
Cohesion: 0.16
Nodes (5): Container, ScrollableContainer, ChatView, ThinkingIndicator, ChatMessage

### Community 3 - "UI Components"
Cohesion: 0.24
Nodes (4): Static, CustomHeader, CustomHeader, InputBar

### Community 4 - "LangGraph Definition"
Cohesion: 0.12
Nodes (13): build_graph(), llm_node(), AgentState, execute(), Runtime Model Swapping, LLM Provider Abstraction, get_llm(), Factory to return the appropriate LangChain ChatModel instance. (+5 more)

### Community 6 - "LLM Provider Factory"
Cohesion: 0.17
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 7 - "LLM Base Implementation"
Cohesion: 0.33
Nodes (3): BaseChatModel, get_model(), MockChatModel

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (6): 1. `gemini_llm_node`, Graph Structure, LangGraph Simple Agent Specification (Gemini LLM Node), Nodes, Overview, State Schema

## Knowledge Gaps
- **20 isolated node(s):** `BeforeTool`, `Identity`, `Code Style`, `Instructions`, `Architecture Rules` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LataiApp` connect `TUI Application Core` to `Community 27`, `Command Interface`, `Chat View Display`, `UI Components`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `CommandMenu` connect `Command Interface` to `TUI Application Core`, `Chat View Display`, `UI Components`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `ChatView` connect `Chat View Display` to `TUI Application Core`, `UI Components`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `LataiApp` (e.g. with `Token-by-Token Streaming` and `UI Layer Isolation`) actually correct?**
  _`LataiApp` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CommandMenu` (e.g. with `CustomHeader` and `CustomHeader`) actually correct?**
  _`CommandMenu` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ChatView` (e.g. with `CustomHeader` and `CustomHeader`) actually correct?**
  _`ChatView` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `LataiApp` (e.g. with `ChatView` and `InputBar`) actually correct?**
  _`LataiApp` has 4 INFERRED edges - model-reasoned connections that need verification._