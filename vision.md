

```mermaid
flowchart TD
    S(["__start__"]) --> root_node

    root_node["root_node\nclassify intent"]
    root_node -->|new task / edit| planner_node
    root_node -->|skip plan| summary_log

    summary_log["summary_log\nlog rationale to state"]
    summary_log --> plan_approval

    planner_node["planner_node\ndecompose & plan"]
    planner_node --> plan_approval

    plan_approval{{"⏸ plan_approval\nhuman · approve plan"}}
    plan_approval -->|approved| generator_node
    plan_approval -->|revise| planner_node

    generator_node["generator_node\ngenerate / patch code"]
    generator_node --> file_permission

    file_permission{{"⏸ file_permission\nhuman · new file or overwrite?"}}
    file_permission -->|write · new file| write_file_node
    file_permission -->|overwrite · show diff| diff_preview
    file_permission -->|skip| evaluator_node

    diff_preview{{"⏸ diff_preview\nhuman · confirm overwrite"}}
    diff_preview -->|confirmed| write_file_node
    diff_preview -->|cancel| evaluator_node

    write_file_node["write_file_node\nwrite to disk"]
    write_file_node -->|success| exec_permission
    write_file_node -->|error| evaluator_node

    exec_permission{{"⏸ exec_permission\nhuman · allow execution?"}}
    exec_permission -->|approved| execute_code_node
    exec_permission -->|denied| E(["__end__"])

    execute_code_node["execute_code_node\nrun + capture output"]
    execute_code_node -->|success| evaluator_node
    execute_code_node -->|syntax / runtime error| generator_node

    evaluator_node["evaluator_node\nset status field"]
    evaluator_node --> retry_guard

    retry_guard{{"retry_guard\ncheck retries < max"}}
    retry_guard -->|done| E(["__end__"])
    retry_guard -->|needs patch| generator_node
    retry_guard -->|needs replan| planner_node
    retry_guard -->|max retries| E(["__end__"])

    style root_node       fill:#2d3748,stroke:#68d391,color:#fff
    style summary_log     fill:#2d3748,stroke:#68d391,color:#fff
    style planner_node    fill:#322659,stroke:#9f7aea,color:#fff
    style generator_node  fill:#744210,stroke:#f6ad55,color:#fff
    style write_file_node    fill:#1a365d,stroke:#63b3ed,color:#fff
    style execute_code_node  fill:#1a365d,stroke:#63b3ed,color:#fff
    style evaluator_node  fill:#3d1a1a,stroke:#fc8181,color:#fff
    style plan_approval   fill:#1a3a2a,stroke:#48bb78,color:#9ae6b4
    style file_permission fill:#1a3a2a,stroke:#48bb78,color:#9ae6b4
    style diff_preview    fill:#1a3a2a,stroke:#48bb78,color:#9ae6b4
    style exec_permission fill:#1a3a2a,stroke:#48bb78,color:#9ae6b4
    style retry_guard     fill:#2d2a1a,stroke:#ecc94b,color:#faf089
    style S fill:#1a202c,stroke:#4a5568,color:#a0aec0
    style E fill:#1a202c,stroke:#4a5568,color:#a0aec0
```

---

### Node prompts

**`root_node`**
```
You are an intent classifier. Read the user message and classify it as one of:
- "new task"   → user wants something built from scratch
- "edit"       → user references existing code or output and wants a change
- "skip plan"  → request is trivial enough (single file, clear spec) to skip planning

Output JSON: { "intent": "new task" | "edit" | "skip plan", "summary": "<one sentence>" }
Do not generate any code.
```

**`summary_log`**
```
The planner was skipped. Write a one-paragraph rationale explaining why no formal plan
is needed for this task and what the generator will do directly.
Append this to state.plan_log before passing control forward.
This ensures the human sees a brief summary at plan_approval even without a full plan.
```

**`planner_node`**
```
You are a task planner. Given the user's request and any prior state, produce a structured plan:
- List of files to create or modify
- Step-by-step implementation approach
- Known risks or ambiguities
- Estimated number of code generation passes

Output JSON: { "steps": [...], "files": [...], "risks": [...] }
Do not write any code. Do not guess at implementation details — flag unknowns explicitly.
```

**`plan_approval`** *(human interrupt)*
```
INTERRUPT: Present the plan to the user.
Display state.plan_log in a readable format.
Ask: "Approve this plan or request revisions?"
Resume with: { "decision": "approved" | "revise", "feedback": "<optional text>" }
On revise, write feedback into state.revision_notes before returning to planner_node.
```

**`generator_node`**
```
You are a code generator. Using state.plan and state.revision_notes (if any),
generate or patch the required code.
- On first pass: generate from the plan
- On patch pass: read state.error_trace and state.evaluator_status, fix only what failed
- On replan pass: read state.revision_notes, regenerate with updated scope

Output: { "file_path": "...", "content": "...", "patch_mode": true | false }
Never modify files not listed in the plan without flagging it.
```

**`file_permission`** *(human interrupt)*
```
INTERRUPT: Check if state.file_path already exists on disk.
- If NOT exists → prompt: "Create new file at <path>?"
- If EXISTS     → prompt: "File already exists. Overwrite? (will show diff)"

Resume with: { "decision": "write" | "overwrite" | "skip" }
On "overwrite" route to diff_preview. On "skip" route to evaluator_node
with state.evaluator_status = "skipped".
```

**`diff_preview`** *(human interrupt)*
```
INTERRUPT: Generate a unified diff between the existing file and state.content.
Display the diff clearly. Ask: "Confirm overwrite?"
Resume with: { "decision": "confirmed" | "cancel" }
On cancel, set state.evaluator_status = "write_cancelled" and route to evaluator_node.
```

**`write_file_node`**
```
Write state.content to state.file_path on disk.
On success: set state.write_status = "ok", pass to exec_permission.
On failure (permissions error, disk full, path invalid):
  set state.write_status = "error"
  set state.error_trace = <OS error message>
  route to evaluator_node with state.evaluator_status = "write_error"
Do not swallow exceptions silently.
```

**`exec_permission`** *(human interrupt)*
```
INTERRUPT: Display the file path and first 20 lines of state.content.
Ask: "Allow execution of <file_path>?"
Resume with: { "decision": "approved" | "denied" }
On denied → route to __end__ with state.evaluator_status = "execution_denied".
Log denial reason to state if user provides one.
```

**`execute_code_node`**
```
Execute state.file_path in a sandboxed subprocess. Capture:
- stdout, stderr, exit_code, runtime_ms

On success (exit_code == 0):
  set state.exec_output = { stdout, runtime_ms }
  set state.evaluator_status = "executed"
On failure:
  set state.error_trace = stderr
  set state.evaluator_status = "runtime_error"
  route directly back to generator_node for auto-fix (no human needed for known error types)
Timeout after 30s → treat as runtime error.
```

**`evaluator_node`**
```
You are a result evaluator. Read state and set state.evaluator_status to exactly one of:
- "done"             → output is correct and complete
- "needs_patch"      → output ran but result is wrong; small fix needed in generator
- "needs_replan"     → scope changed or approach is fundamentally wrong
- "write_error"      → disk write failed (propagated from write_file_node)
- "write_cancelled"  → user cancelled overwrite
- "skipped"          → user skipped file write
- "execution_denied" → user denied execution

Do not route. Do not loop. Only set the status field and pass to retry_guard.
Output JSON: { "evaluator_status": "...", "rationale": "<one sentence>" }
```

**`retry_guard`**
```
Read state.evaluator_status and state.retry_count (default 0).
MAX_RETRIES = 4

If evaluator_status == "done"            → route to __end__
If evaluator_status in terminal set      → route to __end__
  terminal = { write_cancelled, skipped, execution_denied, write_error after max }
If retry_count >= MAX_RETRIES            → route to __end__ with status "max_retries"
If evaluator_status == "needs_patch"     → increment retry_count, route to generator_node
If evaluator_status == "needs_replan"    → increment retry_count, route to planner_node

Always write updated retry_count back to state before routing.
```