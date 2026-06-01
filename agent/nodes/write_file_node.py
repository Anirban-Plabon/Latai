from agent.state import AgentState


async def write_file_node(state: AgentState) -> dict:
    """Pass-through node representing the file writing phase."""
    return {}
