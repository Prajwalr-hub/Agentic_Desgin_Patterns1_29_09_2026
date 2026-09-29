import unittest
from types import SimpleNamespace
from unittest.mock import patch

from patterns.tool_using.graph import build_graph
from tools.calculator import calculator


class StubLLM:
    def __init__(self, responses):
        self.responses = iter(responses)

    def invoke(self, prompt):
        return SimpleNamespace(content=next(self.responses))


class ToolUsingWorkflowTests(unittest.TestCase):
    def test_arithmetic_question_uses_calculator(self):
        with patch(
            "patterns.tool_using.nodes.llm",
            StubLLM(["MATH: ((10 + 5) / 2) ** 2"]),
        ):
            result = build_graph().invoke({"question": "Square the average of 10 and 5."})

        self.assertEqual(result["route"], "math")
        self.assertEqual(result["result"], "56.25")

    def test_general_question_uses_fallback(self):
        with patch(
            "patterns.tool_using.nodes.llm",
            StubLLM(
                [
                    "GENERAL",
                    "Artificial intelligence is the study of systems that perform tasks requiring human-like intelligence.",
                ]
            ),
        ):
            result = build_graph().invoke({"question": "Define AI."})

        self.assertEqual(result["route"], "general")
        self.assertIn("Artificial intelligence", result["result"])

    def test_unsupported_math_expression_falls_back(self):
        with patch(
            "patterns.tool_using.nodes.llm",
            StubLLM(["MATH: math.sqrt(9)", "The square root of 9 is 3."]),
        ):
            result = build_graph().invoke({"question": "What is the square root of 9?"})

        self.assertEqual(result["route"], "general")
        self.assertEqual(result["result"], "The square root of 9 is 3.")

    def test_calculator_rejects_non_arithmetic_code(self):
        result = calculator("__import__('os').system('whoami')")

        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()