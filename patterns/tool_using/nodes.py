from config.llm import get_llm
from tools.calculator import calculator
from .state import AgentState

llm = get_llm()

def reasoning_agent(state: AgentState):
    prompt = f"""
                Decide whether the question can be answered by evaluating a
                basic arithmetic expression. For arithmetic, reply exactly:
                MATH: <expression>
                For every other question, reply exactly: GENERAL

                Supported arithmetic operators are +, -, *, /, //, %, **,
                parentheses, and unary + or -.

                Question: {state['question']}
                """
    response = llm.invoke(prompt).content.strip()

    if response.upper() == "GENERAL":
        return {"route": "general"}

    if response[:5].upper() == "MATH:":
        expression = response[5:].strip()
        if expression:
            return {"route": "math", "expression": expression}

    return {"route": "general"}

def tool_executor(state: AgentState):
    result = calculator(state["expression"])
    return {"result": result}

def fallback_agent(state: AgentState):
    prompt = f"""
                Answer the user's question clearly and accurately.
                If it is a math question, solve it directly and show brief
                working. Do not mention internal tools or errors.

                Question: {state['question']}
                """
    answer = llm.invoke(prompt).content.strip()
    return {"route": "general", "result": answer}