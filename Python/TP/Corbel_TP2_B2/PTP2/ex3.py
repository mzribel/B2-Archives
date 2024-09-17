import statistics
from math import pow, sqrt
from PUtils import utils, inputs, menu_tui as menu
from PTP2 import ex2

class Ex3:
    """Contient les méthodes nécessaires à l'exercice TP2_3: Calcul de la variance et de l'écart-type."""
    synced_list = []
    debug = True
# Méthodes statiques:
    @staticmethod
    def get_pvariance(lst):
        """Equivalent de la fonction statistics.pvariance, renvoie la variance d'une population."""

        # Vérifie si le paramètre `lst` est valide. Lance une TypeError exception dans le cas inverse.
        utils.check_numerical_list_validity(lst)
        # Retourne 0 si la liste est vide afin d'éviter une division par 0.
        if len(lst) == 0: return 0

        # Récupère la moyenne de la population
        lstMean = statistics.mean(lst)
        squareTotal = 0
        # Pour chaque valeur de la liste, ajoute à squareTotal le carré de la valeur
        # moins la moyenne de la population.
        for value in lst:
            squareTotal += pow((value - lstMean), 2)

        return squareTotal / len(lst)

    @staticmethod
    def get_psdt_deviation(lst):
        """Equivalent de la fonction statistics.pstddev, renvoie l'écart-type  d'une population, ie
        la racine carrée de la variance de la population."""
        return sqrt(Ex3.get_pvariance(lst))

def submenu():
    userRetry = -1
    while userRetry != 0:
        synced_has_value = len(Ex3.synced_list) != 0
        # Affiche le menu et demande l'input de l'utilisateur.
        menu.Box("V A R I A N C E  & E C .  T Y P E").drawBox()
        print(f"Dernière liste utilisée: "+ (f"\n   {Ex3.synced_list}\n" if synced_has_value else "///\n"))
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
                numberLst = Ex3.synced_list
                print(f"--- LISTE ENREGISTREE ---\n   {numberLst}")
            case default:
                continue

        # Affiche les résultats.
        if len(numberLst) > 0 and numberLst is not None:
            try:
                print("\nRESULTAT:\n"
                      f"   Variance de la liste: {round(Ex3.get_pvariance(numberLst), 2)}\n"
                      f"   Ecart-type de la liste: {round(Ex3.get_psdt_deviation(numberLst), 2)}")
                if Ex3.debug:
                    print("COMPARAISON (statistics.pvariance & statistics.pstdev):\n"
                          f"   Variance de la liste: {round(statistics.pvariance(numberLst), 2)}\n"
                          f"   Ecart-type de la liste: {round(statistics.pstdev(numberLst), 2)}")
                Ex3.synced_list = ex2.Ex2.synced_list = numberLst
            except TypeError as e:
                print(f"ERREUR: {str(e)}")
        utils.jump_lines()

        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Voulez-vous continuer?")
        utils.jump_lines()