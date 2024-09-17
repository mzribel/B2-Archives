# TP 2.5: SIMULATION DE LANCERS DE DES
from random import randrange
from PUtils import utils, inputs, menu_tui as menu
# PIP INSTALL PANDAS
import pandas as pd

pd.set_option("display.max_rows", None)

class Ex5:
    @staticmethod
    def getFrequency(itemList, isNumerical: bool = True)->dict:
        """Récupère la fréquence pour chaque face du dé."""
        try:
            _ = iter(itemList)
        except TypeError:
            raise TypeError("Le paramètre `itemList` doit être itérable.")

        result = {}
        # Itère sur la liste des lancers et trie les chiffres
        for item in itemList:
            if not str(item) in result:
                result[(str(item) if not isNumerical else item)] = itemList.count(item)

        return dict(sorted(result.items()))

    @staticmethod
    def rollDice(faceCount: int, rollCount: int = 1000):
        """Lance un dé de `faceCount` faces `rollCount` fois."""
        if faceCount <= 0 or rollCount <= 0:
            return None
        return [randrange(1, faceCount + 1, 1) for _ in range(rollCount)]

    @staticmethod
    def customRollDice(faces: list, rollCount: int = 1000):
        if len(faces) == 0 or rollCount <= 0:
            return None
        return [str(faces[randrange(0, len(faces), 1)]) for _ in range(rollCount)]

def submenu():
    userRetry = -1
    while userRetry != 0:
        menu.Box("L A N C E R S  D E  D E S").drawBox()
        utils.jump_lines()
        # Récupère le nombre de faces et le nombre de lancers à l'utilisateur.
        # 120 est la limite haute du nombre de face puisqu'il s'agit pour l'instant de la limite théorique pour
        # le nombre de faces maximal d'un dé!
        faces_nb = inputs.getNumericalInput("Nombre de faces du dés → ", True, 3, 120)
        rolls_nb = inputs.getNumericalInput("Nombre de lancers du dés → ", True, 1, 10000)
        utils.jump_lines()

        # Calcule la fréquence
        result = Ex5.getFrequency(Ex5.rollDice(faces_nb, rolls_nb))
        frequency = map(lambda x: x / rolls_nb * 100, result.values())
        # Crée et affiche un dataframe comprenant les données
        print(pd.DataFrame.from_dict({"Face": result.keys(), "Total": result.values(), "Fréquence (%)": frequency}).to_string(index=False))

        utils.jump_lines()

        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Voulez-vous réessayer?")
        utils.jump_lines()