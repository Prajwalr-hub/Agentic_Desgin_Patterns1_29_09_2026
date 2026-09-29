import ast
import operator


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
_MAX_EXPRESSION_LENGTH = 256
_MAX_EXPONENT = 1000


def _evaluate(node: ast.AST):
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Only basic arithmetic operators are supported.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > _MAX_EXPONENT:
            raise ValueError(f"Exponents must be between -{_MAX_EXPONENT} and {_MAX_EXPONENT}.")

        result = operation(left, right)
        if isinstance(result, complex):
            raise ValueError("Complex results are not supported.")
        return result

    if isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATORS.get(type(node.op))
        if operation is not None:
            return operation(_evaluate(node.operand))

    raise ValueError("Only numeric arithmetic expressions are supported.")


def calculator(expression: str) -> str:
    try:
        if len(expression) > _MAX_EXPRESSION_LENGTH:
            raise ValueError("The expression is too long.")
        parsed_expression = ast.parse(expression, mode="eval")
        return str(_evaluate(parsed_expression))
    except (ArithmeticError, SyntaxError, TypeError, ValueError) as error:
        return f"Error: {error}"