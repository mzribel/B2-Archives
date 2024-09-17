import sys
import unittest
from abc import ABC

class CustomTestClass(ABC, unittest.TestCase):
    """Récupère automatiquement le nom de la classe et définit les méthodes
    `setUpClass et tearDownClass pour l'affichage des tests unitaires."""

    classname:str = ""
    # Surcharge des méthodes de classe:
    @classmethod
    def setUpClass(cls):
        CustomTestClass.classname = cls.__name__.replace("Tests_", "")
        print(f'\n---> STARTING TESTS ON CLASS `{CustomTestClass.classname}`..."')
    @classmethod
    def tearDownClass(cls):
        print(f'---> ENDED TESTS ON CLASS `{CustomTestClass.classname}`.')

    @staticmethod
    def record_test(module, out=sys.stderr, verbosity: int = 2):
        suite = unittest.TestLoader().loadTestsFromModule(module)
        unittest.TextTestRunner(out, verbosity=verbosity).run(suite)