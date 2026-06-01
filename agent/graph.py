import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes.root_node import root_node
from agent.nodes.planner_node import planner_node
from agent.nodes.generator_node import generator_node
from agent.nodes.write_file_node import write_file_node
from agent.nodes.chat_node import chat_node


def route_start(state: AgentState) -> str:
    return state.get("route", "skip_plan")


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("root_node", root_node)
    graph.add_node("planner_node", planner_node)
    graph.add_node("generator_node", generator_node)
    graph.add_node("write_file_node", write_file_node)
    graph.add_node("chat_node", chat_node)

    graph.set_entry_point("root_node")

    graph.add_conditional_edges(
        "root_node",
        route_start,
        {
            "new_task": "planner_node",
            "edit_request": "planner_node",
            "skip_plan": "chat_node",
            "simple_coding": "generator_node",
        },
    )

    graph.add_edge("planner_node", "generator_node")
    graph.add_edge("generator_node", "write_file_node")
    graph.add_edge("write_file_node", END)
    graph.add_edge("chat_node", END)

    return graph


graph = build_graph()
phase1_graph = graph.compile()
