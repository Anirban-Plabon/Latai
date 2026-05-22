# Graph Report - Latai  (2026-05-22)

## Corpus Check
- 44 files · ~7,257 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 310 nodes · 410 edges · 48 communities (39 shown, 9 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0db73b9d`
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
- [[_COMMUNITY_Anthropic Provider|Anthropic Provider]]
- [[_COMMUNITY_Gemini Provider|Gemini Provider]]
- [[_COMMUNITY_OpenRouter Provider|OpenRouter Provider]]
- [[_COMMUNITY_OpenAI Provider|OpenAI Provider]]
- [[_COMMUNITY_App Lifecycle|App Lifecycle]]
- [[_COMMUNITY_Mock Provider|Mock Provider]]
- [[_COMMUNITY_OpenAI Integration|OpenAI Integration]]
- [[_COMMUNITY_OpenRouter Integration|OpenRouter Integration]]
- [[_COMMUNITY_Chat Agent Specification|Chat Agent Specification]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]

## God Nodes (most connected - your core abstractions)
1. `LataiApp` - 20 edges
2. `CommandMenu` - 18 edges
3. `get_api_key()` - 17 edges
4. `ChatView` - 16 edges
5. `ThinkingIndicator` - 14 edges
6. `Session` - 13 edges
7. `get_llm()` - 12 edges
8. `LataiApp` - 12 edges
9. `InputBar` - 12 edges
10. `get_configured_models()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `CustomHeader` --uses--> `ThinkingIndicator`  [INFERRED]
  tui/app.py → res/ui/loaders.py
- `LataiApp` --uses--> `ThinkingIndicator`  [INFERRED]
  tui/app.py → res/ui/loaders.py
- `stream_response()` --calls--> `get_llm()`  [INFERRED]
  tui/app.py → services/llm.py
- `get_llm()` --calls--> `get_api_key()`  [INFERRED]
  services/llm.py → utils/config.py
- `get_llm()` --calls--> `get_base_url()`  [INFERRED]
  services/llm.py → utils/config.py

## Communities (48 total, 9 thin omitted)

### Community 0 - "LangGraph Orchestration"
Cohesion: 0.14
Nodes (6): is_command(), parse_command(), LataiApp, stream_response(), format_error_message(), Standardizes error messages across different providers (OpenAI, Anthropic, Gemin

### Community 1 - "TUI Core & Header"
Cohesion: 0.16
Nodes (7): Markdown, MarkdownFence, CustomMarkdown, MarkdownFenceWithCopy, Markdown widget that uses our custom code block class., A code block with a 'Copy' button in the top right., ChatMessage

### Community 2 - "Command Menu & Messaging"
Cohesion: 0.10
Nodes (9): build_graph(), Compiled Agent Graph, llm_node(), AgentState, execute(), Debug Graph Script, Welcome Animation Logic, Session (+1 more)

### Community 3 - "Chat View Rendering"
Cohesion: 0.10
Nodes (20): App, Container, Horizontal, Message, Static, CustomHeader, LataiApp, 'ascii', 'blank', 'block', 'dashed', 'double', 'heavy', 'hidden', 'hkey', 'inner (+12 more)

### Community 4 - "UI Resources (Loaders/Welcome)"
Cohesion: 0.31
Nodes (6): animate_welcome(), get_interpolated_hex(), hex_to_rgb(), Converts #RRGGBB to (R, G, B) tuple., Returns hex string for a color between two RGB tuples., Mounts and animates the welcome logo with a unified structure and dynamic colors

### Community 5 - "Command Parsing"
Cohesion: 0.13
Nodes (4): ScrollableContainer, CustomFooter, ChatView, ThinkingIndicator

### Community 6 - "LLM Provider Factory"
Cohesion: 0.06
Nodes (46): get_api_key(), get_available_providers(), get_base_url(), get_configured_models(), get_default_model(), get_default_provider(), get_installed_ollama_models(), _get_provider_config() (+38 more)

### Community 7 - "LLM Abstractions"
Cohesion: 0.36
Nodes (4): BaseChatModel, get_model(), _llm_type(), MockChatModel

### Community 8 - "Custom Markdown Extensions"
Cohesion: 0.29
Nodes (6): 1. `gemini_llm_node`, Graph Structure, LangGraph Simple Agent Specification (Gemini LLM Node), Nodes, Overview, State Schema

### Community 25 - "App Lifecycle"
Cohesion: 0.15
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.17
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 34 - "Community 34"
Cohesion: 0.10
Nodes (20): get_llm(), Legacy wrapper for the new LLM factory., Factory to return the appropriate LangChain ChatModel instance., Factory to return the appropriate LangChain ChatModel instance., Anthropic Provider, Gemini Provider, get_default_key_name(), load_config() (+12 more)

### Community 35 - "Community 35"
Cohesion: 0.40
Nodes (5): Set base_url for a provider in memory., Set base_url for a provider in memory., Set base_url for a provider in memory., Set base_url for a provider in memory., set_provider_base_url()

### Community 36 - "Community 36"
Cohesion: 0.27
Nodes (9): get_available_models(), _load_cfg(), ChatRequest, Message, ModelOption, ProviderOptions, list_models(), Returns a filtered structure of all currently available model options. (+1 more)

### Community 37 - "Community 37"
Cohesion: 0.29
Nodes (8): chat(), Instantiate the matching LangChain chat model and invoke it with messages., get_base_url(), get_chat_model(), _load_cfg(), Resolve API key based on provider and model rules., Instantiate LangChain chat model with explicit parameters., resolve_key()

## Knowledge Gaps
- **31 isolated node(s):** `BeforeTool`, `Identity`, `Code Style`, `Instructions`, `Architecture Rules` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_llm()` connect `Community 34` to `LangGraph Orchestration`, `Command Menu & Messaging`, `Community 37`, `LLM Provider Factory`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Why does `LataiApp` connect `LangGraph Orchestration` to `Command Menu & Messaging`, `Chat View Rendering`, `UI Resources (Loaders/Welcome)`, `Command Parsing`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Why does `get_api_key()` connect `LLM Provider Factory` to `Community 33`, `Community 34`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `LataiApp` (e.g. with `CommandMenu` and `ThinkingIndicator`) actually correct?**
  _`LataiApp` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CommandMenu` (e.g. with `CustomHeader` and `CustomFooter`) actually correct?**
  _`CommandMenu` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_api_key()` (e.g. with `get_llm()` and `GEMINI.md`) actually correct?**
  _`get_api_key()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ChatView` (e.g. with `CustomHeader` and `CustomFooter`) actually correct?**
  _`ChatView` has 7 INFERRED edges - model-reasoned connections that need verification._