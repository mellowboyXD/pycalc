import unittest
from pycalc.app import Expression, InvalidExpressionToken

def evaluate(exp: str) -> str:
    e = Expression(exp)
    return e.evaluate()

class EvaluateTest(unittest.TestCase):
    def test_simple(self):
        exp = "12+24"
        expected = "36.0"
        actual = evaluate(exp)
        self.assertEqual(expected, actual, "Simple test")

    def test_empty(self):
        self.assertRaises(InvalidExpressionToken, lambda: Expression("").evaluate())

    def test_brackets(self):
        exp = "(2+5)*2"
        expected = "14.0"
        actual = evaluate(exp)
        self.assertEqual(expected, actual, "Test Brackets")

    def test_incomplete(self):
        exp = "2-"
        self.assertRaises(InvalidExpressionToken, lambda: Expression(exp).evaluate())

    def test_negative(self):
        exp = "-2+1"
        expected = "-1.0"
        actual = evaluate(exp)
        self.assertEqual(expected, actual, "Test Negative")


def suite():
    suite = unittest.TestSuite()
    test_cases = [
        func
        for func in dir(EvaluateTest)
        if callable(getattr(EvaluateTest, func)) and func.startswith("test")
    ]
    for test in test_cases:
        suite.addTest(EvaluateTest(test))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())