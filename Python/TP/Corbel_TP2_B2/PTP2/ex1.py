from math import isqrt
from PUtils import utils, inputs, menu_tui as menu

class Ex1:
    """Contient les méthodes nécessaires à l'exercice TP2_1: Test de nombres premiers."""

# Méthodes statiques:
    @staticmethod
    def is_prime(number:int):
        """Vérifie si l'entier `number` passé en paramètre est un nombre premier."""

        # Vérifications pour les très petits chiffres
        if number <= 1: return False
        if number <= 3: return True

        # Vérifie directement si `number` est divisible par 2 et 3
        # afin de gagner du temps sur la boucle suivante.
        if number % 2 == 0 or number % 3 == 0:
            return False

        # Vérifie la primarité du nombre en utilisant la formule `number`%(6k +- 1)
        for i in range(5, isqrt(number)+1, 6):
            if number % i == 0 or number % (i+2) == 0:
                return False
        return True

def submenu():
    """Définit le menu pour l'exercice TP2.1: Nombres premiers
    :return: None"""

    userRetry = -1
    # Répète tant que l'utilisateur ne choisit pas de quitter
    while userRetry != 0:
        menu.Box("N O M B R E S  P R E M I E R S").drawBox()
        utils.jump_lines()

        # Demande à l'utilisateur d'entrer un nombre entier positif.
        number = inputs.getNumericalInput("Entrez un entier positif → ", True, 0)
        try:
            result = Ex1.is_prime(number)
            print(f"RESULTAT: {number} est un nombre premier!" if result else \
                      f"RESULTAT: {number} n'est pas un nombre premier!")
        except Exception:
            print("ERREUR: Une erreur est survenue ! Êtes-vous sûr d'avoir entré un nombre?")
        finally:
            utils.jump_lines()

        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Voulez-vous réessayer?")
        utils.jump_lines()