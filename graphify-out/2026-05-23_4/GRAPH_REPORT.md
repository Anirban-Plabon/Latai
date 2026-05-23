# Graph Report - Latai  (2026-05-23)

## Corpus Check
- 47 files · ~6,621 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 301 nodes · 424 edges · 43 communities (37 shown, 6 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 63 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `65312ff0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_UI Components & Rendering|UI Components & Rendering]]
- [[_COMMUNITY_Main TUI App & Orchestration|Main TUI App & Orchestration]]
- [[_COMMUNITY_Command Menus & Navigation|Command Menus & Navigation]]
- [[_COMMUNITY_Markdown Parsing & Fences|Markdown Parsing & Fences]]
- [[_COMMUNITY_Agentic Graph Definition|Agentic Graph Definition]]
- [[_COMMUNITY_Model Loading & Discovery|Model Loading & Discovery]]
- [[_COMMUNITY_LLM Abstractions|LLM Abstractions]]
- [[_COMMUNITY_Service Abstractions|Service Abstractions]]
- [[_COMMUNITY_Environment Config & Secrets|Environment Config & Secrets]]
- [[_COMMUNITY_UI Assets & Animation|UI Assets & Animation]]
- [[_COMMUNITY_LLM Concrete Providers|LLM Concrete Providers]]
- [[_COMMUNITY_Agent State & Types|Agent State & Types]]
- [[_COMMUNITY_CLI Settings & Hooks|CLI Settings & Hooks]]
- [[_COMMUNITY_Error Formatting|Error Formatting]]
- [[_COMMUNITY_Application Entry Point|Application Entry Point]]
- [[_COMMUNITY_Project Guidelines|Project Guidelines]]
- [[_COMMUNITY_LLM Node Abstraction|LLM Node Abstraction]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 42|Community 42]]

## God Nodes (most connected - your core abstractions)
1. `LataiApp` - 28 edges
2. `ThinkingIndicator` - 21 edges
3. `CommandMenu` - 18 edges
4. `ChatView` - 16 edges
5. `StatusPanel` - 16 edges
6. `Session` - 14 edges
7. `StatusUpdate` - 14 edges
8. `InputBar` - 12 edges
9. `Project: LangGraph Chat TUI` - 12 edges
10. `LataiApp` - 12 edges

## Surprising Connections (you probably didn't know these)
- `get_model()` --semantically_similar_to--> `get_model()`  [INFERRED] [semantically similar]
  services/providers/ollama.py → /mnt/l/projects/Latai/services/providers/openai.py
- `main()` --calls--> `LataiApp`  [INFERRED]
  main.py → tui/app.py
- `LataiApp` --uses--> `ThinkingIndicator`  [INFERRED]
  tui/app.py → /mnt/l/projects/Latai/res/ui/loaders.py
- `CustomHeader` --uses--> `ThinkingIndicator`  [INFERRED]
  tui/app.py → /mnt/l/projects/Latai/res/ui/loaders.py
- `CustomFooter` --uses--> `ThinkingIndicator`  [INFERRED]
  tui/app.py → /mnt/l/projects/Latai/res/ui/loaders.py

## Hyperedges (group relationships)
- **LLM Invocation Flow** — api_server_chat, agent_graph_llm_node, services_llm_factory_get_chat_model [INFERRED 0.85]
- **Provider Implementations** — providers_anthropic_get_model, providers_gemini_get_model, providers_mock_get_model [INFERRED 0.90]
- **TUI Core Components** — tui_app_lataiapp, tui_chat_view_chatview, tui_input_bar_inputbar, tui_command_menu_commandmenu [INFERRED 0.95]

## Communities (43 total, 6 thin omitted)

### Community 0 - "UI Components & Rendering"
Cohesion: 0.08
Nodes (13): Container, Horizontal, ScrollableContainer, Static, CustomHeader, CustomFooter, CustomHeader, ChatView (+5 more)

### Community 1 - "Main TUI App & Orchestration"
Cohesion: 0.09
Nodes (14): graph, App, is_command(), parse_command(), main(), LataiApp, 'ascii', 'blank', 'block', 'dashed', 'double', 'heavy', 'hidden', 'hkey', 'inner, stream_response() (+6 more)

### Community 2 - "Command Menus & Navigation"
Cohesion: 0.22
Nodes (7): Message, CommandMenu, ModelSelected, Show the menu, optionally jumping straight to a sub-menu., Hide and reset to main menu., Centered overlay command palette.      Navigation:       • Main menu  →  Mode, ThemeSelected

### Community 3 - "Markdown Parsing & Fences"
Cohesion: 0.20
Nodes (6): Markdown, MarkdownFence, CustomMarkdown, MarkdownFenceWithCopy, Markdown widget that uses our custom code block class., A code block with a 'Copy' button in the top right.

### Community 4 - "Agentic Graph Definition"
Cohesion: 0.11
Nodes (7): build_graph(), llm_node(), execute(), debug(), get_llm(), Legacy wrapper for the new LLM factory., Session

### Community 5 - "Model Loading & Discovery"
Cohesion: 0.35
Nodes (7): get_available_models(), _load_cfg(), ChatRequest, Message, ModelOption, ProviderOptions, BaseModel

### Community 6 - "LLM Abstractions"
Cohesion: 0.18
Nodes (6): BaseChatModel, get_model(), get_model(), get_model(), _llm_type(), MockChatModel

### Community 7 - "Service Abstractions"
Cohesion: 0.23
Nodes (10): chat(), list_models(), Returns a filtered structure of all currently available model options., Instantiate the matching LangChain chat model and invoke it with messages., get_base_url(), get_chat_model(), _load_cfg(), Resolve API key based on provider and model rules. (+2 more)

### Community 8 - "Environment Config & Secrets"
Cohesion: 0.29
Nodes (12): get_api_key(), get_base_url(), get_configured_models(), get_default_model(), get_default_provider(), is_provider_configured(), _load_cfg(), Get key from config.yaml. Supports model-level resolution for openrouter. (+4 more)

### Community 10 - "LLM Concrete Providers"
Cohesion: 0.25
Nodes (3): get_model(), get_model(), get_model()

### Community 25 - "Project Guidelines"
Cohesion: 0.17
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 27 - "Community 27"
Cohesion: 0.15
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 28 - "Community 28"
Cohesion: 0.29
Nodes (6): 1. `gemini_llm_node`, Graph Structure, LangGraph Simple Agent Specification (Gemini LLM Node), Nodes, Overview, State Schema

### Community 30 - "Community 30"
Cohesion: 0.40
Nodes (4): id, name, projectResources, resources

### Community 31 - "Community 31"
Cohesion: 0.31
Nodes (6): animate_welcome(), get_interpolated_hex(), hex_to_rgb(), Converts #RRGGBB to (R, G, B) tuple., Returns hex string for a color between two RGB tuples., Mounts and animates the welcome logo with a unified structure and dynamic colors

### Community 42 - "Community 42"
Cohesion: 0.20
Nodes (6): _category_icon(), Right-column execution monitor. Auto-shows on activity, auto-hides when idle., Right-column execution monitor. Auto-shows on activity, auto-hides when idle., Append a timestamped status entry., Append a timestamped status entry and auto-show the panel., StatusPanel

## Knowledge Gaps
- **29 isolated node(s):** `BeforeTool`, `Identity`, `Code Style`, `Instructions`, `Architecture Rules` (+24 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LataiApp` connect `Main TUI App & Orchestration` to `UI Components & Rendering`, `Command Menus & Navigation`, `Agentic Graph Definition`, `UI Assets & Animation`, `Community 42`, `Application Entry Point`, `Community 31`?**
  _High betweenness centrality (0.266) - this node is a cross-community bridge._
- **Why does `Session` connect `Agentic Graph Definition` to `Environment Config & Secrets`, `Main TUI App & Orchestration`, `Community 31`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `LataiApp` (e.g. with `StatusPanel` and `StatusUpdate`) actually correct?**
  _`LataiApp` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ThinkingIndicator` (e.g. with `LataiApp` and `.show_loading()`) actually correct?**
  _`ThinkingIndicator` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CommandMenu` (e.g. with `.compose()` and `CustomHeader`) actually correct?**
  _`CommandMenu` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `ChatView` (e.g. with `.compose()` and `ThinkingIndicator`) actually correct?**
  _`ChatView` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `StatusPanel` (e.g. with `LataiApp` and `StatusUpdate`) actually correct?**
  _`StatusPanel` has 3 INFERRED edges - model-reasoned connections that need verification._