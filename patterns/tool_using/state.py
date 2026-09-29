from typing import TypedDict

class AgentState(TypedDict):
    question: str
    expression: str
    result: str