import statistics
from functools import reduce
from PUtils import utils, inputs, menu_tui as menu
from PTP2 import ex3

class Ex2:
    """Contient les méthodes nécessaires à l'exercice TP2_2: Calcul de la moyenne et de la médiane"""
    # Permetafficher les résultats de statistics.mean.median après les résultats des fonctions customisées.
    debug = True
    synced_list = []

    @staticmethod
    def get_mean(lst):
        """Equivalent de la fonction statistics.mean, renvoie la moyenne d'un ensemble de nombres."""

        # Vérifie la validité du type du paramètre.
        utils.check_numerical_list_validity(lst)

        return reduce(lambda a, b: a + b, lst) / len(lst) if len(lst) > 0 else None

    @staticmethod
    def getMedian(lst):
        """Equivalent de la fonction statistics.median, renvoie la médiane d'un ensemble de nombres."""
        utils.check_numerical_list_validity(lst)

        # Retourne 0 si la liste ne comprend aucune valeur.
        if len(lst) == 0: return None

        # Trie la liste et récupère la valeur du milieu arrondie à l'entier inférieur.
        lst = sorted(lst)
        midValue = (len(lst) - 1) // 2

        if len(lst) % 2 == 1:
            return lst[midValue]
        return (lst[midValue] + lst[midValue + 1]) / 2

def submenu():
    userRetry = -1
    while userRetry != 0:
        synced_has_value = len(Ex2.synced_list) != 0
        # Affiche le menu et demande l'input de l'utilisateur.
        menu.Box("M O Y E N N E  &  M E D I A N E").drawBox()
        print(f"Dernière liste utilisée: "+ (f"\n   {Ex2.synced_list}\n" if synced_has_value else "///\n"))
        print("1// Nouvelle liste\n"+("2// Utiliser la dernière liste enregistrée\n" if synced_has_value else "")+"\n0// Retour")
        userRetry = inputs.getNumericalInput("→ ", True, 0, 2 if synced_has_value else 1)
        utils.jump_lines()
        numberLst = []

        # Récupère la liste de la manière choisie par l'utilisateur.
        match userRetry:
            case 1:
                print("--- NOUVELLE LISTE ---\n")
                numberLst = inputs.getNumericalListInput("Entrez une liste de nombres (décimaux/négatifs supportés):\n   → ")
            case 2:
                numberLst = Ex2.synced_list
                print(f"--- LISTE ENREGISTREE ---\n   {numberLst}")
            case default:
                continue

        # Affiche les résultats.
        if len(numberLst) > 0 and numberLst is not None:
            try:
                print("\nRESULTAT:\n"
                      f"   Moyenne de la liste: {round(Ex2.get_mean(numberLst), 2)}\n"
                      f"   Médiane de la liste: {round(Ex2.getMedian(numberLst), 2)}")
                if Ex2.debug:
                    print("COMPARAISON (statistics.mean & statistics.median):\n"
                          f"   Moyenne de la liste: {round(statistics.mean(numberLst), 2)}\n"
                          f"   Médiane de la liste: {round(statistics.median(numberLst), 2)}")
                Ex2.synced_list = ex3.Ex3.synced_list = numberLst
            except TypeError as e:
                print(f"ERREUR: {str(e)}")
        utils.jump_lines()

        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Voulez-vous réessayer?")
        utils.jump_lines()