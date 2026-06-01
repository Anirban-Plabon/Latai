# Graph Report - Latai  (2026-05-30)

## Corpus Check
- 96 files · ~18,722 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 946 nodes · 1129 edges · 129 communities (77 shown, 52 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 165 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b2b97ba6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Chat UI Views|Chat UI Views]]
- [[_COMMUNITY_Agent Graph Logic|Agent Graph Logic]]
- [[_COMMUNITY_State and Commands|State and Commands]]
- [[_COMMUNITY_File Tree Panel|File Tree Panel]]
- [[_COMMUNITY_File Services|File Services]]
- [[_COMMUNITY_Status Panel Splitter|Status Panel Splitter]]
- [[_COMMUNITY_File Editor Panel|File Editor Panel]]
- [[_COMMUNITY_Input Bar Components|Input Bar Components]]
- [[_COMMUNITY_API Server Config|API Server Config]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]
- [[_COMMUNITY_Community 99|Community 99]]
- [[_COMMUNITY_Community 100|Community 100]]
- [[_COMMUNITY_Community 101|Community 101]]
- [[_COMMUNITY_Community 102|Community 102]]
- [[_COMMUNITY_Community 103|Community 103]]
- [[_COMMUNITY_Community 104|Community 104]]
- [[_COMMUNITY_Community 105|Community 105]]
- [[_COMMUNITY_Community 106|Community 106]]
- [[_COMMUNITY_Community 107|Community 107]]
- [[_COMMUNITY_Community 108|Community 108]]
- [[_COMMUNITY_Community 109|Community 109]]
- [[_COMMUNITY_Community 110|Community 110]]
- [[_COMMUNITY_Community 111|Community 111]]
- [[_COMMUNITY_Community 112|Community 112]]
- [[_COMMUNITY_Community 113|Community 113]]
- [[_COMMUNITY_Community 114|Community 114]]
- [[_COMMUNITY_Community 115|Community 115]]
- [[_COMMUNITY_Community 116|Community 116]]
- [[_COMMUNITY_Community 117|Community 117]]
- [[_COMMUNITY_Community 118|Community 118]]
- [[_COMMUNITY_Community 119|Community 119]]
- [[_COMMUNITY_Community 120|Community 120]]
- [[_COMMUNITY_Community 121|Community 121]]
- [[_COMMUNITY_Community 122|Community 122]]
- [[_COMMUNITY_Community 123|Community 123]]
- [[_COMMUNITY_Community 124|Community 124]]
- [[_COMMUNITY_Community 125|Community 125]]
- [[_COMMUNITY_Community 126|Community 126]]
- [[_COMMUNITY_Community 127|Community 127]]
- [[_COMMUNITY_Community 128|Community 128]]

## God Nodes (most connected - your core abstractions)
1. `LataiApp` - 44 edges
2. `StatusUpdate` - 23 edges
3. `FilePanel` - 23 edges
4. `StatusPanel` - 21 edges
5. `ThinkingIndicator` - 19 edges
6. `get_llm()` - 18 edges
7. `Session` - 14 edges
8. `AgentState` - 13 edges
9. `ProjectFileService` - 13 edges
10. `CommandMenu` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Architecture Rules` --references--> `LataiApp`  [INFERRED]
  AGENTS.md → tui/app.py
- `File Panel Layout Design` --rationale_for--> `FilePanel`  [INFERRED]
  implementation_plan.md → tui/file_panel/file_panel.py
- `Relative Path Jail Security Pattern` --rationale_for--> `FilePanel`  [INFERRED]
  implementation_plan.md → tui/file_panel/file_panel.py
- `File Panel Commands Scheme` --conceptually_related_to--> `FilePanel`  [INFERRED]
  implementation_plan.md → tui/file_panel/file_panel.py
- `hooks` --references--> `graphify`  [INFERRED]
  .gemini/settings.json → AGENTS.md

## Hyperedges (group relationships)
- **Agent Module Components** — agent_prompts_py, agent_tools_py, agent_init_py [EXTRACTED 1.00]
- **Provider Implementations** — providers_anthropic_get_model, providers_gemini_get_model, providers_mock_get_model [INFERRED 0.90]
- **Configuration Utility Layer** — utils_config__load_cfg, utils_config_get_api_key, utils_config_get_configured_models, utils_config_is_provider_configured [INFERRED 0.95]
- **Project Guidelines and Standards** — latai_agents_architecture_rules, latai_agents_code_style, latai_agents_streaming [EXTRACTED 1.00]
- **Agent Graph Nodes** — nodes_analyzer_error_analysis_node, nodes_classifier_classifier_node, nodes_generator_generate_code_node, nodes_planner_planner_node, nodes_executor_execute_code_node, nodes_responder_final_response_node, nodes_write_file_write_file_node, nodes_ask_cmd_approval_ask_cmd_approval_node, nodes_ask_file_approval_ask_file_approval_node, nodes_chat_chat_node [INFERRED 0.95]
- **Textual Markdown Diff Render Tests** — test_diff_render_testapp, test_diff_snapshot_testapp, test_nbsp_render_testapp [INFERRED 0.95]
- **Agent Skills** — skills_analyzer_skill, skills_classifier_skill, skills_generator_skill, skills_planner_skill, skills_responder_skill [INFERRED 0.85]
- **File System UI Components** — file_panel_file_panel_filepanel, file_panel_file_editor_panel_fileeditorpanel, file_panel_file_viewer_panel_fileviewerpanel, file_panel_file_tree_panel_filetreepanel [INFERRED 0.85]

## Communities (129 total, 52 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.24
Nodes (8): extract_text(), Invoke LLM, return AIMessage with error on failure., Stream from LLM, yield error AIMessage on failure., Return absolute path to a skill file., safe_llm_call(), safe_llm_stream(), skill_path(), root_node()

### Community 1 - "Chat UI Views"
Cohesion: 0.14
Nodes (11): FileEditorPanel, is_dirty(), on_changed(), Editable file buffer panel., File editor panel container., Initialize editor panel., Compose the editor panel widgets., Load file content into editable TextArea. (+3 more)

### Community 2 - "Agent Graph Logic"
Cohesion: 0.07
Nodes (10): diff_preview(), exec_permission(), file_permission(), plan_approval(), Suspend and show the plan to the user.     Resumes with: { "decision": "approved, Check if file exists. Ask user: create / overwrite / skip.     Resumes with: { ", Generate unified diff and ask user to confirm overwrite.     Resumes with: { "de, Show file path + first 20 lines. Ask user to allow execution.     Resumes with: (+2 more)

### Community 3 - "State and Commands"
Cohesion: 0.07
Nodes (23): build_graph(), graph, execute(), execute(), Execute /term command.      If args is empty, toggle persistent terminal mode., Architecture Rules, debug(), main (+15 more)

### Community 4 - "File Tree Panel"
Cohesion: 0.06
Nodes (34): 1. Feature Design, 2. Command Design, 3. Class Responsibilities, 4. Data Flow, 5. Keybindings, 6. Error Handling, 7. Session State Integration, 8. UI Integration (+26 more)

### Community 5 - "File Services"
Cohesion: 0.09
Nodes (16): FileAction, Command router for file system commands., Parse file commands and return action descriptors., route(), ProjectFileService, Project file service for secure filesystem access., Initialize with a locked project root., Resolve relative path securely, preventing directory traversal. (+8 more)

### Community 6 - "Status Panel Splitter"
Cohesion: 0.05
Nodes (22): FilePanel, Top-level file system panel widget., Handle ctrl+e keybinding to switch from viewer to editor., Update glob filter and reload tree panel., Container panel for file tree, viewer, and editor., Initialize file panel., Set up initial panel visibility., Load file in read-only viewer and focus it. (+14 more)

### Community 8 - "Input Bar Components"
Cohesion: 0.11
Nodes (17): Switch view from FilePanel back to ChatView., Switch view from FilePanel back to ChatView., Switch view from FilePanel back to ChatView., Switch view from FilePanel back to ChatView., Switch view from FilePanel back to ChatView., Handle closing the file panel, checking for unsaved changes., Switch view from FilePanel back to ChatView., Switch view from FilePanel back to ChatView. (+9 more)

### Community 9 - "API Server Config"
Cohesion: 0.14
Nodes (17): get_available_models(), _load_cfg(), ChatRequest, Message, ModelOption, ProviderOptions, chat(), list_models() (+9 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (23): ScrollableContainer, _category_icon(), Append a timestamped status entry., Append a timestamped status entry., Append a timestamped status entry., Shows a loader for the current agent node in the status panel., Strike through all todo entries in the execution monitor and tick them., Strike through all todo entries in the execution monitor and tick them. (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.20
Nodes (8): check_file_approval, route_start(), AgentState, ask_file_approval_node, classifier_node(), Intent Classifier Node.          Analyzes the user's input and classifies their, root_node(), write_file_node()

### Community 12 - "Community 12"
Cohesion: 0.08
Nodes (13): MarkdownFence, ChatView.add_message, ChatView, Stream token into the message — uses lock-free Static path., Call when streaming is done — swaps Static → CustomMarkdown., CustomMarkdown, MarkdownFenceWithCopy, Markdown widget that uses our custom code block class. (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.20
Nodes (5): BaseChatModel, get_model(), get_model(), get_model(), MockChatModel

### Community 15 - "Community 15"
Cohesion: 0.10
Nodes (16): id, name, projectResources, resources, hooks, BeforeTool, Code Style, Commands (+8 more)

### Community 16 - "Community 16"
Cohesion: 0.33
Nodes (6): detect_language, is_binary, is_too_large, read_file, resolve_safe_path, write_file

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (3): get_model(), get_model(), get_model()

### Community 18 - "Community 18"
Cohesion: 0.14
Nodes (13): 1. Non-Blocking Async Background Workers, 1. Persistent Mode Toggle (`/term` without arguments), 2. File Level Details, 2. Single Command Execution (`/term <command>` with arguments), Manual Execution Steps, [MODIFY] [app.css](file:///F:/Anirban_250509/Projects/Latai/tui/app.css), [MODIFY] [app.py](file:///F:/Anirban_250509/Projects/Latai/tui/app.py), [MODIFY] [session.py](file:///F:/Anirban_250509/Projects/Latai/services/session.py) (+5 more)

### Community 20 - "Community 20"
Cohesion: 1.00
Nodes (3): TestApp, TestApp, TestApp

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (3): Terminal Mode Implementation Milestones, Persistent Terminal Mode Pattern, Single Subprocess Shell Command Execution

### Community 34 - "Community 34"
Cohesion: 0.11
Nodes (21): chat_node(), General chat and coding assistant node. Streams response to TUI., _extract_files(), generator_node(), Generator Node. Generates or patches code strictly following the provided skill, Parse ---FILE: path--- blocks from generator output., Parse ---FILE: path--- blocks from generator output., extract_text() (+13 more)

### Community 41 - "Community 41"
Cohesion: 0.40
Nodes (4): Script to calculate the sum of numbers from 1 to 1000., Sum all integers from 1 to 1000., Calculate the sum of integers from 1 to 1000 using the formula for arithmetic se, sum_1_to_1000()

### Community 46 - "Community 46"
Cohesion: 0.10
Nodes (19): Switch view from ChatView to FilePanel., Switch view from ChatView to FilePanel., Switch view from ChatView to FilePanel., Switch view from ChatView to FilePanel., Switch view from ChatView to FilePanel., Switch view from ChatView to FilePanel., Switch view from ChatView to FilePanel., Switch active file from read-only viewer to editable editor. (+11 more)

### Community 55 - "Community 55"
Cohesion: 0.20
Nodes (9): Classifier Skill, Categories, Classifier Skill, code:json ({), CODING, Examples, NON_CODING, Output Format (+1 more)

### Community 56 - "Community 56"
Cohesion: 0.22
Nodes (8): code:block1 (✅ [Task completed successfully / Task completed after N retr), code:block2, Guidelines, Output Format, Responder Skill, Tone, What to Include, Your Role

### Community 57 - "Community 57"
Cohesion: 0.25
Nodes (7): Code Reviewer Skill, code:block1 (## Review Result: PASS | FAIL), Guidelines, Output Format, Severity Levels, What to Check, Your Role

### Community 58 - "Community 58"
Cohesion: 0.18
Nodes (10): Generator Skill, Code Quality Rules, code:block1 (---FILE: path/to/file.py---), code:block2, Generator Skill, Important, Important Constraints, Inputs You Receive (+2 more)

### Community 59 - "Community 59"
Cohesion: 0.25
Nodes (7): env, ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL, ANTHROPIC_MODEL, permissions, allow

### Community 60 - "Community 60"
Cohesion: 0.29
Nodes (6): code:block1 (## Project Structure), Context Gatherer Skill, Guidelines, Output Format, What to Do, Your Role

### Community 61 - "Community 61"
Cohesion: 0.29
Nodes (6): 1. `gemini_llm_node`, Graph Structure, LangGraph Simple Agent Specification (Gemini LLM Node), Nodes, Overview, State Schema

### Community 62 - "Community 62"
Cohesion: 0.33
Nodes (5): Analysis Output Format, code:block1 (## Root Cause), Debugger Skill, Guidelines, Inputs You Receive

### Community 63 - "Community 63"
Cohesion: 0.33
Nodes (5): Code Style, graphify, Identity, Instructions, What to Avoid

### Community 64 - "Community 64"
Cohesion: 0.17
Nodes (11): Architecture Rules, Code Style, Commands, graphify, Identity, Instructions, Naming, Project: LangGraph Chat TUI (+3 more)

### Community 73 - "Community 73"
Cohesion: 0.29
Nodes (6): Planner Skill, code:block1 (Brief one-sentence summary of what will be built.), Guidelines, Output Format, Planner Skill, Your Responsibilities

### Community 77 - "Community 77"
Cohesion: 0.25
Nodes (7): Categories, CHAT, COMPLEX_CODING, Output Format, Routing Skill, SHELL, SIMPLE_CODING

### Community 78 - "Community 78"
Cohesion: 0.11
Nodes (17): Handle closing the file panel, checking for unsaved changes., Switch view from FilePanel back to ChatView., Handle closing the file panel, checking for unsaved changes., Handle closing the file panel, checking for unsaved changes., Handle closing the file panel, checking for unsaved changes., Handle closing the file panel, checking for unsaved changes., Handle closing the file panel, checking for unsaved changes., Handle closing the file panel, checking for unsaved changes. (+9 more)

### Community 85 - "Community 85"
Cohesion: 0.31
Nodes (8): merge(), mergesort(), mergesort_inplace(), Test the mergesort implementation., Merge two sorted lists into a single sorted list.          Args:         left: F, Sort a list using the mergesort algorithm.          Args:         arr: List of e, Sort a list in-place using mergesort algorithm.     This version modifies the or, test_mergesort()

### Community 86 - "Community 86"
Cohesion: 0.22
Nodes (8): extract_text(), Call LLM with error handling. Returns AIMessage with error info on failure., Invoke LLM, return AIMessage with error on failure., Return absolute path to a skill file., safe_llm_call(), skill_path(), code_reviewer_node(), context_gatherer_node()

### Community 87 - "Community 87"
Cohesion: 0.18
Nodes (12): Categories, Classifier Skill, code:block1 ({"route": "<route>", "confidence": "<high|medium|low>"}), CODING_DIRECT, CODING_PLAN, Decision Rules, Examples, NON_CODING (+4 more)

### Community 88 - "Community 88"
Cohesion: 0.11
Nodes (17): Process and execute file operations., Process and execute file operations., Process and execute file operations., Process and execute file operations., Process and execute file operations., Process and execute file operations., Process and execute file operations., Process and execute file operations. (+9 more)

### Community 89 - "Community 89"
Cohesion: 0.11
Nodes (18): Switch active file from read-only viewer to editable editor., Switch active file from read-only viewer to editable editor., Switch active file from read-only viewer to editable editor., Switch active file from read-only viewer to editable editor., Switch active file from read-only viewer to editable editor., Switch active file from read-only viewer to editable editor., Switch active file from read-only viewer to editable editor., Switch active file from read-only viewer to editable editor. (+10 more)

### Community 90 - "Community 90"
Cohesion: 0.25
Nodes (7): dependencies, env, graphs, agent, phase1, phase2, pythonpath

### Community 94 - "Community 94"
Cohesion: 0.38
Nodes (9): _build_project_tree(), _check_syntax(), _extract_files(), _extract_files_from_response(), generate_code_node(), _generate_diff(), generator_node(), Generator Node.          Generates or patches code strictly following the provid (+1 more)

### Community 98 - "Community 98"
Cohesion: 0.08
Nodes (22): is_command(), parse_command(), main(), _extract_content(), LataiApp, on_approval_option_selected(), on_directory_tree_file_selected(), on_input_submitted() (+14 more)

### Community 99 - "Community 99"
Cohesion: 0.13
Nodes (14): code:mermaid (flowchart TD), code:block10 (INTERRUPT: Display the file path and first 20 lines of state), code:block11 (Execute state.file_path in a sandboxed subprocess. Capture:), code:block12 (You are a result evaluator. Read state and set state.evaluat), code:block13 (Read state.evaluator_status and state.retry_count (default 0), code:block2 (You are an intent classifier. Read the user message and clas), code:block3 (The planner was skipped. Write a one-paragraph rationale exp), code:block4 (You are a task planner. Given the user's request and any pri) (+6 more)

### Community 100 - "Community 100"
Cohesion: 0.24
Nodes (8): check_success, Stream from LLM with error handling. Yields error message on failure., Stream from LLM, yield error AIMessage on failure., safe_llm_stream(), error_analysis_node(), final_response_node(), responder_node(), Show the menu, optionally jumping straight to a sub-menu.

### Community 101 - "Community 101"
Cohesion: 0.28
Nodes (8): merge(), merge_inplace(), merge_sort(), merge_sort_inplace(), Sorts a list of integers using the merge sort algorithm.          Args:, Merges two sorted lists into a single sorted list.          Args:         left:, Sorts a list in-place using merge sort.          indices: [start, end), Merges two sorted subarrays in-place.     Subarrays: [start, mid) and [mid, end)

### Community 103 - "Community 103"
Cohesion: 0.11
Nodes (12): Container, Message, CommandMenu, CommandSelected, ModelSelected, Hide and reset to main menu., Centered overlay command palette.      Navigation:       • Main menu  →  Mode, TEXTUAL_THEMES (+4 more)

### Community 109 - "Community 109"
Cohesion: 0.16
Nodes (8): Loading indicator with animated loader frames and elapsed time., Loading indicator with animated loader frames and elapsed time., Render a single animation frame., Render a single animation frame., Mark the indicator as completed., Mark the indicator as completed., ThinkingIndicator, DEV_LOCAL_THEME

### Community 110 - "Community 110"
Cohesion: 0.25
Nodes (6): check_cmd_approval, execute_python_code(), Execute a Python script with timeout and proper error capture.      Args:, ask_cmd_approval_node, execute_code_node(), _run_file()

### Community 111 - "Community 111"
Cohesion: 0.25
Nodes (6): check_coding, chat_node(), planner_node(), Planner Node.          Decomposes the user's requested task or edit into a concr, get_llm(), Legacy wrapper for the new LLM factory.

### Community 117 - "Community 117"
Cohesion: 0.50
Nodes (4): merge(), merge_sort(), Merge two sorted lists into one sorted list.          Args:         left: Sorted, Sort a list using the merge sort algorithm.          Args:         arr: List of

### Community 121 - "Community 121"
Cohesion: 0.08
Nodes (21): DirectoryTree, Compose the file tree and content panels., FileTreePanel, ProjectDirectoryTree, File tree panel widget., Custom DirectoryTree that filters and styles nodes., Initialize directory tree with optional glob filter., Filter out hidden and irrelevant files/folders, and apply optional glob. (+13 more)

### Community 123 - "Community 123"
Cohesion: 0.13
Nodes (10): FileViewerPanel, Read-only file viewer panel., File viewer panel container., Compose the viewer panel widgets., Hide markdown viewer by default., Load file content. Uses Markdown widget for .md files, TextArea for all others., Render content in the Markdown widget., Render content in the read-only TextArea with syntax highlighting. (+2 more)

### Community 124 - "Community 124"
Cohesion: 0.22
Nodes (5): App, TestApp, TestApp, TestApp, Markdown

### Community 125 - "Community 125"
Cohesion: 0.40
Nodes (5): is_language_supported(), Runtime guard for tree-sitter language availability., Return language if its tree-sitter grammar is available, else None., Return True only if the language grammar is actually loadable at runtime.      T, safe_language()

## Knowledge Gaps
- **162 isolated node(s):** `id`, `name`, `resources`, `PreToolUse`, `ANTHROPIC_BASE_URL` (+157 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **52 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LataiApp` connect `Community 98` to `State and Commands`, `File Services`, `Status Panel Splitter`, `Community 103`, `Input Bar Components`, `Community 10`, `Community 12`, `Community 109`, `Community 46`, `Community 78`, `Community 88`, `Community 89`, `Community 124`?**
  _High betweenness centrality (0.246) - this node is a cross-community bridge._
- **Why does `CommandMenu` connect `Community 103` to `Community 98`, `Community 100`, `Status Panel Splitter`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Why does `FilePanel` connect `Status Panel Splitter` to `Chat UI Views`, `Community 98`, `File Services`, `Community 12`, `Community 121`, `Community 123`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `LataiApp` (e.g. with `ChatView` and `InputBar`) actually correct?**
  _`LataiApp` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `StatusUpdate` (e.g. with `LataiApp` and `.on_mount()`) actually correct?**
  _`StatusUpdate` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `FilePanel` (e.g. with `LataiApp` and `ProjectFileService`) actually correct?**
  _`FilePanel` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `StatusPanel` (e.g. with `LataiApp` and `.compose()`) actually correct?**
  _`StatusPanel` has 3 INFERRED edges - model-reasoned connections that need verification._