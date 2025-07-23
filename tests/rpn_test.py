import unittest
from pycalc.app import Expression


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
