# Graph Report - Latai  (2026-05-23)

## Corpus Check
- 61 files · ~11,271 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 503 nodes · 664 edges · 56 communities (44 shown, 12 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 85 edges (avg confidence: 0.72)
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
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 55|Community 55]]

## God Nodes (most connected - your core abstractions)
1. `LataiApp` - 43 edges
2. `ThinkingIndicator` - 21 edges
3. `CommandMenu` - 19 edges
4. `StatusUpdate` - 18 edges
5. `FilePanel` - 18 edges
6. `ChatView` - 16 edges
7. `StatusPanel` - 16 edges
8. `Session` - 14 edges
9. `ProjectFileService` - 12 edges
10. `InputBar` - 12 edges

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

## Communities (56 total, 12 thin omitted)

### Community 0 - "UI Components & Rendering"
Cohesion: 0.05
Nodes (19): App, Container, Horizontal, ScrollableContainer, Static, CustomHeader, LataiApp, 'ascii', 'blank', 'block', 'dashed', 'double', 'heavy', 'hidden', 'hkey', 'inner (+11 more)

### Community 1 - "Main TUI App & Orchestration"
Cohesion: 0.08
Nodes (19): graph, is_command(), parse_command(), main(), LataiApp, on_directory_tree_file_selected(), The main Latai TUI chat application class., The main Latai TUI chat application class. (+11 more)

### Community 2 - "Command Menus & Navigation"
Cohesion: 0.19
Nodes (9): Message, CommandMenu, ModelSelected, Show the menu, optionally jumping straight to a sub-menu., Show the menu, optionally jumping straight to a sub-menu., Hide and reset to main menu., Centered overlay command palette.      Navigation:       • Main menu  →  Mode, Centered overlay command palette.      Navigation:       • Main menu  →  Mode (+1 more)

### Community 3 - "Markdown Parsing & Fences"
Cohesion: 0.05
Nodes (23): DirectoryTree, FilePanel, Top-level file system panel widget., Handle ctrl+e keybinding to switch from viewer to editor., Update glob filter and reload tree panel., Container panel for file tree, viewer, and editor., Initialize file panel., Compose the file tree and content panels. (+15 more)

### Community 4 - "Agentic Graph Definition"
Cohesion: 0.10
Nodes (11): build_graph(), llm_node(), execute(), debug(), Session, animate_welcome(), get_interpolated_hex(), hex_to_rgb() (+3 more)

### Community 5 - "Model Loading & Discovery"
Cohesion: 0.11
Nodes (19): get_available_models(), _load_cfg(), ChatRequest, Message, ModelOption, ProviderOptions, chat(), list_models() (+11 more)

### Community 6 - "LLM Abstractions"
Cohesion: 0.18
Nodes (6): BaseChatModel, get_model(), get_model(), get_model(), _llm_type(), MockChatModel

### Community 7 - "Service Abstractions"
Cohesion: 0.14
Nodes (13): 1. Non-Blocking Async Background Workers, 1. Persistent Mode Toggle (`/term` without arguments), 2. File Level Details, 2. Single Command Execution (`/term <command>` with arguments), Manual Execution Steps, [MODIFY] [app.css](file:///F:/Anirban_250509/Projects/Latai/tui/app.css), [MODIFY] [app.py](file:///F:/Anirban_250509/Projects/Latai/tui/app.py), [MODIFY] [session.py](file:///F:/Anirban_250509/Projects/Latai/services/session.py) (+5 more)

### Community 8 - "Environment Config & Secrets"
Cohesion: 0.29
Nodes (12): get_api_key(), get_base_url(), get_configured_models(), get_default_model(), get_default_provider(), is_provider_configured(), _load_cfg(), Get key from config.yaml. Supports model-level resolution for openrouter. (+4 more)

### Community 10 - "LLM Concrete Providers"
Cohesion: 0.25
Nodes (3): get_model(), get_model(), get_model()

### Community 11 - "Agent State & Types"
Cohesion: 0.22
Nodes (6): AgentState, FileAction, Command router for file system commands., Parse file commands and return action descriptors., route(), TypedDict

### Community 14 - "Application Entry Point"
Cohesion: 0.20
Nodes (6): Markdown, MarkdownFence, CustomMarkdown, MarkdownFenceWithCopy, Markdown widget that uses our custom code block class., A code block with a 'Copy' button in the top right.

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
Cohesion: 0.11
Nodes (14): Render a custom styled label with file icons., FileViewerPanel, Read-only file viewer panel., Compose the viewer panel widgets., Load file content into read-only viewer., Clear viewer content., File viewer panel container., get_color() (+6 more)

### Community 42 - "Community 42"
Cohesion: 0.18
Nodes (7): _category_icon(), Right-column execution monitor. Auto-shows on activity, auto-hides when idle., Right-column execution monitor. Auto-shows on activity, auto-hides when idle., Append a timestamped status entry., Append a timestamped status entry., Append a timestamped status entry and auto-show the panel., StatusPanel

### Community 43 - "Community 43"
Cohesion: 0.07
Nodes (29): 1. Feature Design, 1. Update Session State, 2. Command Design, 2. Create the Terminal Command Executor, 3. Adjust Input Bar CSS, 4. Data Flow, 4. Wire Terminal Mode inside TUI App, 5. Keybindings (+21 more)

### Community 47 - "Community 47"
Cohesion: 0.13
Nodes (11): ProjectFileService, Project file service for secure filesystem access., Initialize with a locked project root., Resolve relative path securely, preventing directory traversal., Sniff first 8KB of a file to check if it is binary., Check if file size exceeds size limit in bytes (default 1MB)., Map file extension to Textual TextArea language name., Read text file safely, returning content and language. (+3 more)

### Community 48 - "Community 48"
Cohesion: 0.14
Nodes (11): FileEditorPanel, is_dirty(), on_changed(), Editable file buffer panel., File editor panel container., Initialize editor panel., Compose the editor panel widgets., Load file content into editable TextArea. (+3 more)

### Community 49 - "Community 49"
Cohesion: 0.13
Nodes (15): 3. Class Responsibilities, code:python (EXTENSION_STYLES: dict[str, tuple[str, str]] = {), code:python (def route(cmd: str, args: str) -> dict:), Command Layer — `commands/`, [NEW] `commands/files.py` — `FileCommandRouter`, [NEW] `services/files/file_type_styler.py` — `FileTypeStyler`, [NEW] `services/files/__init__.py`, [NEW] `services/files/project_file_service.py` — `ProjectFileService` (+7 more)

## Knowledge Gaps
- **62 isolated node(s):** `BeforeTool`, `Identity`, `Code Style`, `Instructions`, `Architecture Rules` (+57 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LataiApp` connect `Main TUI App & Orchestration` to `UI Components & Rendering`, `Command Menus & Navigation`, `Markdown Parsing & Fences`, `Agentic Graph Definition`, `UI Assets & Animation`, `Community 42`, `Community 46`, `Community 47`?**
  _High betweenness centrality (0.262) - this node is a cross-community bridge._
- **Why does `FilePanel` connect `Markdown Parsing & Fences` to `UI Components & Rendering`, `Main TUI App & Orchestration`, `Community 47`, `Community 48`, `Community 31`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Why does `Session` connect `Agentic Graph Definition` to `Environment Config & Secrets`, `Main TUI App & Orchestration`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `LataiApp` (e.g. with `StatusPanel` and `StatusUpdate`) actually correct?**
  _`LataiApp` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ThinkingIndicator` (e.g. with `LataiApp` and `.show_loading()`) actually correct?**
  _`ThinkingIndicator` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CommandMenu` (e.g. with `.compose()` and `CustomHeader`) actually correct?**
  _`CommandMenu` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `StatusUpdate` (e.g. with `LataiApp` and `StatusPanel`) actually correct?**
  _`StatusUpdate` has 14 INFERRED edges - model-reasoned connections that need verification._