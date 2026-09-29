from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import reasoning_agent, tool_executor

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("reasoning_agent", reasoning_agent)
    graph.add_node("math_agent", tool_executor)

    graph.set_entry_point("reasoning_agent")
    graph.add_edge("reasoning_agent", "math_agent")
    graph.add_edge("math_agent", END)

    return graph.compile()