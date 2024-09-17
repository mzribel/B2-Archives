from enum import IntEnum
from PUtils import menu, utils
import re

# Regex ciblant le format d'une string comprenant une succession d'opérations.
operationReg = re.compile(r"^(?:-?\d+(?:\.\d+)?|\(-\d+(?:\.\d+)?\))? *[+-\/*] *(?:\d+(?:\.\d+)?|\(-\d+(?:\.\d+)?\)) *(?: *[-+\/*] *(?:\d+(?:\.\d+)?|\(-\d+(?:\.\d+)?\)))*$")
# Ces deux regex pourraient être regroupées en une si la première boucle while de `makeAComplexOperation` avait une variable `ignoreIfNotPriorities`.
priorities = re.compile(r"(?P<a>-?\d+(?:\.\d+)?|\(-\d+(?:\.\d+)?\))(?P<sign>[\/\*])(?P<b>\d+(?:\.\d+)?|\(-\d+(?:\.\d+)?\))")
operations = re.compile(r"(?P<a>-?\d+(?:\.\d+)?|\(-\d+(?:\.\d+)?\))(?P<sign>[\/\*+-])(?P<b>\d+(?:\.\d+)?|\(-\d+(?:\.\d+)?\))")

class Operations(IntEnum):
    MLT = 1
    ADD = 2
    DVD = 3
    SUB = 4

operationsNames = ["Multiplication", "Addition", "Division", "Soustraction"]

# Traduit un signe en son équivalent dans l'enum Operations.
def stringToSignEnum(sign:str):
    match sign:
        case "*":
            return Operations.MLT
        case "/":
            return Operations.DVD
        case "+":
            return Operations.ADD
        case "-":
            return Operations.SUB
        case _:
            raise TypeError("Le signe de l'opération est incorrect (doit être [/+-*])")

# Traduit un élément de l'enum Operations en son signe.
def signEnumToString(sign:Operations):
    match sign:
        case 1:
            return "*"
        case 2:
            return "+"
        case 3:
            return "/"
        case 4:
            return "-"

# Réalise une opération simple à deux termes et correspondant à une addition, soustraction, multiplication ou division
# de nombres entiers ou décimaux.
def makeAnOperation(opType:Operations, num1, num2):
    if not isinstance(num1, (int, float, complex)) or not isinstance(num1, (int, float, complex)):
        raise TypeError("Seule des valeurs numériques sont autorisées en guise de terme d'une opération")

    match opType:
        case 1:
            return num1 * num2
        case 2:
            return num1 + num2
        case 3:
            return num1 / num2
        case _:
            return num1 - num2

# Todo: Refactoriser potentiellement ces fonctions pour leur donner un nom plus explicite?
# Interprète une string constituée d'une succession d'opérations simples en respectant les règles de priorité.
def makeAComplexOperation(operationStr:str):
    if not operationReg.match(operationStr):
        raise TypeError("L'équation fournie ne respecte pas le bon format")
    operationStr = operationStr.replace(" ", "")

    # Multiplications et divisions en priorité.
    nextOperations = priorities.search(operationStr)
    while nextOperations:
        operationStr = translateOperation(operationStr, nextOperations)
        nextOperations = priorities.search(operationStr)
    # Additions et soustractions ensuite.
    nextOperation = operations.search(operationStr)
    while nextOperation:
        operationStr = translateOperation(operationStr, nextOperation)
        nextOperation = operations.search(operationStr)

    return round(float(re.sub(r'[()]', '', operationStr)), 4)

# Lorsqu'une correspondance a été trouvée sur une regex d'opérations, prioritaire ou non,
# réalise l'opération et remplace l'opération dans la string par son résultat.
# Todo: Il doit exister une manière plus propre de réaliser ceci.
def translateOperation(full:str, matched:re.Match):
    offset, a, b, sign = 0, float(re.sub(r'[()]', '', matched.group("a"))), float(
            re.sub(r'[()]', '', matched.group("b"))), matched.group("sign")
    if matched.span()[0] != 0 and a < 0:
        a = abs(a)
        offset = 1
    result = makeAnOperation(stringToSignEnum(sign), a, b)
    result = str(result) if result > 0 else f"({result})"
    return full[:matched.span()[0] + offset] + result + full[matched.span()[1]:]

# Menu sous format GUI.
def menuUI():
    userRetry = -1
    while userRetry != 0:
        menu.Box("C A L C U L A T R I C E").drawBox()
        utils.jumpLines()

        # Demande à l'utilisateur son opération choisie.
        print("1// Multiplication\n2// Addition\n3// Division\n4// Soustraction\n\n0// Retour")
        userRetry = utils.getUserInput(0, 4, "→ ", "int")
        utils.jumpLines()

        # Si 0: l'utilisateur retourne au menu principal.
        if userRetry == 0:
            continue

        # Réalise l'opération choisie par l'utilisateur.
        try:
            # Opération complexe à deux termes ou plus.
            # Suite à quelques bugs, cette fonctionnalité est retirée du programme.
            if userRetry == 5:
                print("--- OPERATIONS COMPLEXES (beta) ---\n")
                print("Cette fonctionnalité permet d'interpréter et calculer une string comprenant une succession d'opérations simples.\n"
                      "Règles: prioritées respectées, espaces ignorés; parenthèses autour des négatifs seulement, signes autorisés [+-*/].\nExemple de format: -2 + 5.934 * (-2) / 7\n")
                operationsStr = input("Entrez la chaîne d'opérations: ")
                print(f"RESULTAT: {makeAComplexOperation(operationsStr)}")
            else:
            # Opération simple à deux termes.
                print(f"--- {operationsNames[userRetry-1].upper()} A DEUX TERMES ---\n")
                a = utils.getUserInputWithoutLimits("Entrez la valeur de A: ")
                b = utils.getUserInputWithoutLimits("Entrez la valeur de B: ")
                print(f"RESULTAT: {a} {signEnumToString(userRetry)} {b} = {makeAnOperation(userRetry, a, b)}")
        except ZeroDivisionError:
            print(f"ERREUR: Division par 0 !")
        except TypeError as te:
            print(f"ERREUR: {te}.")
        finally:
            utils.jumpLines()

        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Réaliser un autre calcul ?")
        utils.jumpLines()