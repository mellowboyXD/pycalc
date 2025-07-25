import unittest
from pycalc.app import Expression, InvalidExpressionToken, MissingMatchingBracket


class RPNTest(unittest.TestCase):
    def test_simple(self):
        exp = "12+24"
        expected = ["12", "24", "+"]
        actual = Expression(exp).postfix
        self.assertListEqual(expected, actual, "Simple test")

    def test_1(self):
        exp = "12+24-2"
        expected = ["12", "24", "+", "2", "-"]
        actual = Expression(exp).postfix
        self.assertListEqual(expected, actual, "Simple test")

    def test_decimal(self):
        exp = "2+5.1"
        expected = ["2", "5.1", "+"]
        actual = Expression(exp).postfix
        self.assertListEqual(expected, actual, "Test decimals")

    def test_brac(self):
        exp = "(24-5)*8"
        expected = ["24", "5", "-", "8", "*"]
        actual = Expression(exp).postfix
        self.assertListEqual(expected, actual, "Simple brackets")

    def test_2(self):
        exp = "(24-5)*8/2"
        expected = ["24", "5", "-", "8", "*", "2", "/"]
        actual = Expression(exp).postfix
        self.assertListEqual(expected, actual, "Simple test")

    def test_empty(self):
        exp = ""
        self.assertRaises(InvalidExpressionToken, Expression, exp)

    def test_incomplete(self):
        exp = "2-"  # handle these in evaluate()
        expected = ["2", "-"]
        actual = Expression(exp).postfix
        self.assertListEqual(expected, actual, "Test Incomplete input")

    def test_negative_at_beginning(self):
        exp = "-2+4"
        expected = ["2", "-", "4", "+"]
        actual = Expression(exp).postfix
        self.assertListEqual(expected, actual, "Test negative at beginning")

    def test_mul_at_beginning(self):
        exp = "*3-2"
        expected = ["3", "*", "2", "-"]
        actual = Expression(exp).postfix
        self.assertListEqual(expected, actual, "Multiplication at beginning")

    def test_alphabet(self):
        exp = "s+i" 
        self.assertRaises(InvalidExpressionToken, 
                          Expression, exp)

    def test_only_operators(self):
        exp = "-+/*"
        self.assertRaises(InvalidExpressionToken, 
                          Expression, exp) 

    def test_no_open_brac(self):
        exp = "4-5)/2"
        self.assertRaises(MissingMatchingBracket,
                          Expression, exp)

def suite():
    suite = unittest.TestSuite()
    test_cases = [
        func
        for func in dir(RPNTest)
        if callable(getattr(RPNTest, func)) and func.startswith("test")
    ]
    for test in test_cases:
        suite.addTest(RPNTest(test))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
