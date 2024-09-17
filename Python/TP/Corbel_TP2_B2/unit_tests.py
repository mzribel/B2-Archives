import unittest
from PTP2 import ex5, ex4
from PTP2.ex1 import Ex1
from PTP2.ex2 import Ex2
from PTP2.ex3 import Ex3
from PUtils import utils
from statistics import median, mean, pvariance, pstdev
from collections import Counter

class TestsTP2_1(unittest.TestCase):
    """Réalise les tests relatifs à la classe PTP2.Ex1: Tests de nombres premiers."""

# Surcharge des méthodes de classe:
    @classmethod
    def setUpClass(cls):
        print('\n---> STARTING TESTS ON TP2_1: "Tests de nombres premiers"')
    @classmethod
    def tearDownClass(cls):
        print('---> ENDED TESTS ON TP2_1.')

# Tests sur la fonction is_prime:
    def test_isprime_exception_parameter_type(self):
        self.assertRaises(TypeError, Ex1.is_prime, "a")
    def test_isprime_negative_number(self):
        self.assertEqual(Ex1.is_prime(-1), False)
    def test_isprime_two(self):
        self.assertEqual(Ex1.is_prime(2), True)
    def test_isprime_small_prime_number(self):
        self.assertEqual(Ex1.is_prime(1999), True)
    def test_isprime_big_prime_number(self):
        self.assertEqual(Ex1.is_prime(9737333), True)
    def test_isprime_big_not_prime(self):
        self.assertEqual(Ex1.is_prime(8762325), False)

class TestsTP2_2(unittest.TestCase):
    """Réalise les tests relatifs à la classe PTP2.Ex2: Calcul de la moyenne et de la médiane."""
# Surcharge des méthodes de classe:
    @classmethod
    def setUpClass(cls):
        print('\n---> STARTING TESTS ON TP2_2: "Calcul de la moyenne et de la médiane"')
    @classmethod
    def tearDownClass(cls):
        print('---> ENDED TESTS ON TP2_2.')

    # Tests on getMean:
    def test_mean_exception_parameter_type(self):
        self.assertRaises(TypeError, Ex2.get_mean, "canard")
    def test_mean_exception_parameter_value(self):
        self.assertRaises(TypeError, Ex2.get_mean, [1, 2, 3, 4.3, "canard"])
    def test_mean_empty_parameter(self):
        self.assertIsNone(Ex2.get_mean([]))
    def test_mean_valid(self):
        success = 0
        for i in range(3):
            lst = utils.generate_random_numberList(0, 100, 20)
            if Ex2.get_mean(lst) == mean(lst): success += 1
        self.assertEqual(success, 3)

    # Tests on getMedian:
    def test_median_exception_parameter_type(self):
        self.assertRaises(TypeError, Ex2.getMedian, "canard")
    def test_median_exception_parameter_value(self):
        self.assertRaises(TypeError, Ex2.getMedian, [1, 2, 3, 4.3, "canard"])
    def test_median_empty_parameter(self):
        self.assertIsNone(Ex2.getMedian([]))
    def test_median_valid(self):
        success = 0
        for i in range(3):
            lst = utils.generate_random_numberList(0, 100, 20)
            if Ex2.getMedian(lst) == median(lst): success += 1
        self.assertEqual(success, 3)

class TestsTP2_3(unittest.TestCase):
    """Réalise les tests relatifs à la classe PTP2.Ex3: Calcul de la variance et de l'écart-type."""

# Surcharges des méthodes de classe:
    @classmethod
    def setUpClass(cls):
        print('\n---> STARTING TESTS ON TP2_3: "Calcul de la variance et de l\'écart-type"')
    @classmethod
    def tearDownClass(cls):
        print('---> ENDED TESTS ON TP2_3.')

    # Tests on get_variance:
    def test_variance_exception_parameter_type(self):
        self.assertRaises(TypeError, Ex3.get_pvariance, "canard")
    def test_variance_exception_parameter_value(self):
        self.assertRaises(TypeError, Ex3.get_pvariance, [1, 2, 3, 4.3, "canard"])
    def test_variance_empty_parameter(self):
        self.assertIsNone(Ex2.get_mean([]))
    def test_variance_valid(self):
        success = 0
        for i in range(3):
            lst = utils.generate_random_numberList(0, 100, 20)
            if round(Ex3.get_pvariance(lst), 2) == round(pvariance(lst), 2): success += 1
        self.assertEqual(success, 3)

    # Tests on get_psdt_deviation
    def test_stddev_valid(self):
        success = 0
        for i in range(3):
            lst = utils.generate_random_numberList(0, 100, 20)
            if round(Ex3.get_psdt_deviation(lst), 2) == round(pstdev(lst), 2): success += 1
        self.assertEqual(success, 3)

class TestsTP2_4(unittest.TestCase):
    # Surcharge des méthodes de classe:
    @classmethod
    def setUpClass(cls):
        print('\n---> STARTING TESTS ON TP2_4: "Analyse de données d\'âge"')

    @classmethod
    def tearDownClass(cls):
        print('---> ENDED TESTS ON TP2_4.')

    def test_dfromgroups_none(self):
        self.assertIsNone(ex4.Ex4.get_df_from_groups([]))
    def test_dfromgroups_none_wrong_labels(self):
        self.assertIsNone(ex4.Ex4.get_df_from_groups([-1]))
    def test_dfromgroups_invalid_labels(self):
        self.assertRaises(TypeError, ex4.Ex4.get_df_from_groups, [1, 2, 3], ["canards"])
    def test_dffromgroups_valid(self):
        self.assertEqual(len(ex4.Ex4.get_df_from_groups([1, 20, 30])), 6)

class TestsTP2_5(unittest.TestCase):
# Surcharge des méthodes de classe:
    @classmethod
    def setUpClass(cls):
        print('\n---> STARTING TESTS ON TP2_5: "Simulation de lancers de dés"')
    @classmethod
    def tearDownClass(cls):
        print('---> ENDED TESTS ON TP2_5.')

    # Default dice roll function
    def test_rolldice_wrong_parameters(self):
        self.assertIsNone(ex5.Ex5.rollDice(0, 100))
    def test_rolldice_wrong_parameters_2(self):
        self.assertIsNone(ex5.Ex5.rollDice(6, -1))
    def test_rolldice(self):
        self.assertEqual(len(ex5.Ex5.rollDice(6, 100)), 100)

    # Frequency function
    def test_frequency_exception_parameter_type(self):
        self.assertRaises(TypeError, ex5.Ex5.getFrequency, 2)
    def test_frequency_empty_parameter(self):
        self.assertEqual(ex5.Ex5.getFrequency([]), {})
    def test_valid_numerical_frequency(self):
        lst = ex5.Ex5.rollDice(6, 1000)
        self.assertEqual(ex5.Ex5.getFrequency(lst), dict(sorted(Counter(lst).items())))
    def test_valid_non_numerical_frequency(self):
        lst = ex5.Ex5.customRollDice(["canard", 1, 9.0, [2, 43]], 1000)
        self.assertEqual(ex5.Ex5.getFrequency(lst, False), dict(sorted(Counter(lst).items())))

if __name__ == '__main__':
    unittest.main(verbosity=2)