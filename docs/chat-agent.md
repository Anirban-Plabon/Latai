# LangGraph Simple Agent Specification (Gemini LLM Node)

## Overview
This is a minimal LangGraph agent consisting of a single LLM node powered by the Gemini API.

Flow:

START → Gemini LLM Node → END

The agent takes a user input, sends it to Gemini, and returns the model response directly without additional tools, memory, or branching.

---

## Graph Structure

### Nodes

#### 1. `gemini_llm_node`
- Type: LLM Node
- Purpose: Sends input prompt to Gemini API and returns response.
- Input:
  - `state["messages"]`: List of chat messages (LangChain-style format)
- Output:
  - Appends Gemini response to `state["messages"]`

---

## State Schema

```python
from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    messages: List[Dict[str, Any]]