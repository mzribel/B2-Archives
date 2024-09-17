import os
import unittest

from packages.PMenu.menu import Menu
from packages.PMenu.titlebox import TitleBox
from packages.PUtils import inputs
from tests import test_ex1, test_ex2, test_ex4, test_ex3
from tests.customtestclass import CustomTestClass


def main():
    """Définit le menu pour l'exercice TP2.1: Nombres premiers
        :return: None"""

    os.system('cls' if os.name == 'nt' else 'clear')
    userRetry = -1
    # Répète tant que l'utilisateur ne choisit pas de quitter
    while userRetry != 0:
        TitleBox("Menu Principal").draw()
        print("NOTE: Ce TP ne nécessite pas de réaliser les tests à la main puisqu'il s'agit \n"
              "d'une suite de tests unitaires ! L'accent a été mis sur une meilleure\nstructure et utilisation de la POO. Bonne journée !\n")
        # Demande à l'utilisateur d'entrer un nombre entier positif.
        print("1// Simulateur de compte bancaire\n2// Création d'une classe Personne\n3// Gestionnaire de contacts\n4// Création d'un zoo\n\n0// Retour")
        userRetry = inputs.getNumericalInput("→ ", True, 0, 4)
        match userRetry:
            case 1:
                TitleBox("Tests exercice 1").draw(sep="")
                suite = unittest.TestLoader().loadTestsFromModule(test_ex1)
                unittest.TextTestRunner(verbosity=2).run(suite)
            case 2:
                TitleBox("Tests exercice 2").draw()
                suite = unittest.TestLoader().loadTestsFromModule(test_ex2)
                unittest.TextTestRunner(verbosity=2).run(suite)
            case 3:
                TitleBox("Tests exercice 3").draw()
                suite = unittest.TestLoader().loadTestsFromModule(test_ex3)
                unittest.TextTestRunner(verbosity=2).run(suite)
            case 4:
                suite = unittest.TestLoader().loadTestsFromModule(test_ex4)
                unittest.TextTestRunner(verbosity=2).run(suite)
            case _:
                exit()
        Menu.jump_lines()
        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = Menu.draw_binary_menu("Voulez-vous continuer?")
        Menu.jump_lines()

