import unittest

from PTP1 import calculator, conjugaison, currency, operations, palindrome

# Teste les fonctions de PTP1/calculator.py
class TestCalculator(unittest.TestCase):
    # Complex operations:
    def test_valid_complex_operations(self):
        result = calculator.makeAComplexOperation("2.4355 + 3 * (-2) -10 / 7 * 3 * (-1.847) - 12 * 9 / 9 * 3")
        self.assertEqual(result, -31.6488)
    def test_wrong_format_complex_operations(self):
        self.assertRaises(TypeError, calculator.makeAComplexOperation, "2.4355qskj ° ?")
    def test_illegal_division_complex_operations(self):
        self.assertRaises(ZeroDivisionError, calculator.makeAComplexOperation, "3*8/0")
    # Two-term operations:
    def test_valid_multiplication(self):
        self.assertEqual(calculator.makeAnOperation(1, 3, 7), 21)
    def test_valid_addition(self):
        self.assertEqual(calculator.makeAnOperation(2, -19, 25), 6)
    def test_valid_division(self):
        self.assertEqual(calculator.makeAnOperation(3, -7.5, -10), .75)
    def test_illegal_division(self):
        self.assertRaises(ZeroDivisionError, calculator.makeAnOperation, 3, -7.5, 0)
    def test_illegal_substraction(self):
        self.assertEqual(calculator.makeAnOperation(4, 15, -3.734893), 18.734893)

# Teste les fonctions de PTP1/conjugaison.py
class TestConjugaison(unittest.TestCase):
    def test_get_verb(self):
        self.assertIsNotNone(conjugaison.getVerbFromJSON("manger"))
    def test_verb_doesnt_exist(self):
        self.assertIsNone(conjugaison.getVerbFromJSON("canard"))

# Teste les éléments de PTP1/currency.py
class TestCurrency(unittest.TestCase):
    # Simple exchange rate application function
    def test_valid_applyexchangerate(self):
        self.assertEqual(currency.applyExchangeRate(1234, 1.10), 1357.4)
    def test_sub0_quantity_applyexchangerate(self):
        self.assertEqual(currency.applyExchangeRate(-1, 1.10), 0)
    def test_sub0_exchangeRate_applyexchangerate(self):
        self.assertEqual(currency.applyExchangeRate(10, -1), 0)
    # GetExchangeRate
    def test_valid_getexchangerate(self):
        self.assertEqual(currency.getExchangeRate(3, 4), 1.12)
    def test_valid_getexchangerate2(self):
        self.assertEqual(currency.getExchangeRate(currency.Currency.JPY, currency.Currency.CHF), 0.0061)
    def test_invalid_getexchangerate(self):
        self.assertEqual(currency.getExchangeRate(10, 12), -1)
    # UpdateCurrency
    def test_updatecurrency(self):
        currency.updateCurrency(1.99, 1, 2)
        self.assertEqual(currency.exchangeRates[1][2], 1.99)
        self.assertEqual(currency.exchangeRates[2][1], round(1/1.99, 2))

# Teste les éléments de PTP1/operations.py
class TestOperations(unittest.TestCase):
    def test_valid_getsumfacto(self):
        self.assertEqual(operations.getSumAndFactorial(5), [15, 120])
    def test_zero_getsumfacto(self):
        self.assertEqual(operations.getSumAndFactorial(0), [0,0])
    def test_one_getsumfacto(self):
        self.assertEqual(operations.getSumAndFactorial(1), [1, 1])

# Teste les éléments de PTP1/palindrome.py
class TestPalindrome(unittest.TestCase):
    def test_true_ispalindrome(self):
        self.assertEqual(palindrome.isPalindrome("A man, a plan, a canal: Panama"), True)
    def test_false_ispalindrome(self):
        self.assertEqual(palindrome.isPalindrome("Un très joli canard"), False)
    def test_short_ispalindrome(self):
        self.assertEqual(palindrome.isPalindrome("*$aa"), False)


if __name__ == "__main__":
    unittest.main()