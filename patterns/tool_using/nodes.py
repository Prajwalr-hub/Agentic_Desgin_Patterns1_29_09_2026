from config.llm import get_llm
from tools.calculator import calculator
from .state import AgentState

llm = get_llm()

def reasoning_agent(state: AgentState):
    prompt = f"""
                You are a math reasoning agent.

                Convert the question into a valid Python math expression.
                Return ONLY the expression.

                Examples:
                Question: What is the sum of 5 and 3?
                Expression: 5 + 3

                Question: What is the average of 100 and 200?
                Expression: (100 + 200) / 2

                Question: What is the square of the average of 100 and 200?
                Expression: ((100 + 200) / 2) ** 2

                Question: {state['question']}
                Expression:
                """
    expression = llm.invoke(prompt).content.strip()

    return {"expression": expression}

def tool_executor(state: AgentState):
    result = calculator(state["expression"])
    return {"result": result}