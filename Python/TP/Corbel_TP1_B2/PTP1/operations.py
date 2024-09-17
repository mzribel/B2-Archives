import math
from PUtils import utils, menu
import re

# Calcule la somme et la factorielle d'un nombre `number`
def getSumAndFactorial(number:int):
    if number <= 0: return [0, 0]
    if number == 1: return [1, 1]

    result = [0, 1]

    for i in range(1, number + 1):
        result[0] += i
        result[1] *= i
    return result

# Print le résultat sous la forme fournie par la consigne,
# En éludant une partie des chiffres avec "..." s'ils sont trop nombreux.
def prettyPrint(base:int, sum:int, fact:int):
    if base and sum and fact == 1:
        print("La somme et la factorielle de 1 sont égales à... 1 !\n")
        return
    utils.jumpLines()
    print(prettyPrintLine(base, sum, "+") +
    prettyPrintLine(base, sum, "+", False) + "\n" +
    prettyPrintLine(base, fact, "*") +
    prettyPrintLine(base, fact, "*", False))

def prettyPrintLine(base:int, result:int, sign:str, resultIsFirst=True, total:int=9):
    resultStr:str = f"{result} = " if resultIsFirst else ""
    for i in range(1, base + 1):
        if base > total and math.floor(total / 2) < i < base-(math.floor(total/2)-2):
            if i == math.floor(total/2 + 1):
                resultStr += f"{sign} ..."
            continue
        resultStr += f"{i} " if i == 1 else f"{sign} {i} "


    resultStr += f"= {result}\n" if not resultIsFirst else "\n"
    return resultStr

def menuUI():
    userRetry = -1
    while userRetry != 0:
        menu.Box("S O M M E  /  F A C T O R I E L L E").drawBox()
        utils.jumpLines()

        # Demande à l'utilisateur d'entrer son entier de base.
        # Pour éviter de devoir arrondir et convertir des nombres bien trop grands
        # en notation scientifique, 20 est défini comme la valeur maximum.
        baseNumber = utils.getUserInput(1, 20, "Entrez un nombre positif → ")
        sum, facto = getSumAndFactorial(baseNumber)[0], getSumAndFactorial(baseNumber)[1]
        prettyPrint(baseNumber, sum, facto)

        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Voulez-vous réessayer avec d'autres valeurs ?")
        utils.jumpLines()

