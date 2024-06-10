import unittest
from interpreter import Lexer, Parser, Interpreter

class TestInterpreter(unittest.TestCase):
    def evaluate_expression(self, expression):
        lexer = Lexer(expression)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        return result

    def test_addition(self):
        self.assertEqual(self.evaluate_expression("3 + 5"), 8)

    def test_subtraction(self):
        self.assertEqual(self.evaluate_expression("10 - 2"), 8)

    def test_multiplication(self):
        self.assertEqual(self.evaluate_expression("4 * 2"), 8)

    def test_division(self):
        self.assertEqual(self.evaluate_expression("8 / 4"), 2.0)

    def test_parentheses_simple(self):
        self.assertEqual(self.evaluate_expression("(3 + 5) * 2"), 16)

    def test_nested_parentheses(self):
        self.assertEqual(self.evaluate_expression("((3 + 5) * 2) / 4"), 4.0)

    def test_complex_expression(self):
        self.assertAlmostEqual(self.evaluate_expression("3 + 5 * (2 - 1) / 4"), 4.25, places=2)

    def test_complex_nested_expression(self):
        self.assertAlmostEqual(self.evaluate_expression("(10 - (2 + 3)) * (4 / 2)"), 10.0, places=2)

if __name__ == "__main__":
    unittest.main()
