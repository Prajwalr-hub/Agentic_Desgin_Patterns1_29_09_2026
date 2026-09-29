from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    route: str
    expression: str
    result: str