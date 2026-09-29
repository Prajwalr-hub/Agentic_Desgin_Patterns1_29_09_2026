from langgraph.graph import END, StateGraph

from .state import AgentState
from .nodes import fallback_agent, reasoning_agent, tool_executor


def route_after_reasoning(state: AgentState) -> str:
    if state.get("route") == "math" and state.get("expression"):
        return "math"
    return "fallback"


def route_after_math(state: AgentState) -> str:
    if state.get("result", "").startswith("Error:"):
        return "fallback"
    return "done"

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("reasoning_agent", reasoning_agent)
    graph.add_node("math_agent", tool_executor)
    graph.add_node("fallback_agent", fallback_agent)

    graph.set_entry_point("reasoning_agent")
    graph.add_conditional_edges(
        "reasoning_agent",
        route_after_reasoning,
        {"math": "math_agent", "fallback": "fallback_agent"},
    )
    graph.add_conditional_edges(
        "math_agent",
        route_after_math,
        {"fallback": "fallback_agent", "done": END},
    )
    graph.add_edge("fallback_agent", END)

    return graph.compile()