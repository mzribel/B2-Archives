import math
from PUtils import menu, utils
import re

# Vérifie si la chaîne de caractères fournie en paramètre est un palindrome ou non.
# La fonction ignore tous les caractères qui ne sont pas des lettres présentes dans la table ascii.
# Fonctionne si la chaîne de caractères est une phrase (voir les tests unitaires).
def isPalindrome(word:str):
    # Convertit la phrase en minuscule et retire tous les caractères
    # qui ne sont pas des lettres.
    word = re.sub("[^a-z]", '', word.lower())
    if len(word) < 3:
        return False

    # Itère sur les caractères et retourne false si les caractères opposés
    # ne sont pas les mêmes.
    for i in range(0, math.floor(len(word)/2)):
        if word[i] != word[-1 - i]:
            return False
    return True

def menuUI():
    userRetry = -1
    while userRetry != 0:
        menu.Box("P A L I N D R O M E S").drawBox()
        utils.jumpLines()

        print("Règles: Cette fonctionnalité vérifie si le mot ou la phrase proposé est un palindrome."
              "\nElle ignore tous les caractères non-alphabétiques et lettres accentuées !\n")

        # Demande à l'utilisateur la phrase ou le mot à vérifier.
        sentence = input("Entrez un mot ou une phrase → ")
        print("RESULTAT: ", end="")
        print("C'est un palindrome !") if isPalindrome(sentence) else print("Raté !")
        utils.jumpLines()

        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Voulez vous essayer avec une autre phrase ?")
        utils.jumpLines()

