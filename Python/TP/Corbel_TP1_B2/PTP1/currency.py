from enum import IntEnum
from PUtils import menu, utils, tables

class Currency(IntEnum):
    USD = 0
    EUR = 1
    JPY = 2
    GBP = 3
    CHF = 4
currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CHF']
exchangeRates = [
    [1, 0.95, 149.20, 0.82, 0.92],
    [1.06, 1, 157.48, 0.86, 0.97],
    [0.0067, 0.0064, 1, 0.0055, 0.0061],
    [1.22, 1.16, 182.01, 1, 1.12],
    [1.09, 1.03, 162.75, 0.89, 1]]

# Ce tableau est une sauvegarde des valeurs de base de celui ci-dessus.
# Il vaut mieux éviter d'en changer les valeurs manuellement.
defaultExchangeRates = [
    [1, 0.95, 149.20, 0.82, 0.92],
    [1.06, 1, 157.48, 0.86, 0.97],
    [0.0067, 0.0064, 1, 0.0055, 0.0061],
    [1.22, 1.16, 182.01, 1, 1.12],
    [1.09, 1.03, 162.75, 0.89, 1]]

# Applique un taux de change `exchangeRate` à un montant `quantity`.
def applyExchangeRate(quantity:float,exchangeRate:float):
    if quantity <= 0 or exchangeRate <= 0: return 0
    return quantity * exchangeRate

# Retourne un taux de change du tableau exchangeRates en utilisant
# sa position grâce à l'enum Currency.
def getExchangeRate(sourceCurr:int, targetCurr:int):
    try:
        return exchangeRates[sourceCurr][targetCurr]
    # Retourne une valeur négative (qui ne peut pas être utilisée en tant que
    # taux de change) si aucune valeur n'existe pour les indexes donnés.
    except IndexError:
        return -1

# Applique le taux de change effectif entre la devise de base `sourceCurr` et la devise
# cible `targetCurr`, à un montant `quantity` donné.
def convertToCurrency(quantity:float, sourceCurr:int, targetCurr:int):
    exchangeRate = exchangeRates[sourceCurr][targetCurr]
    if quantity <= 0 or exchangeRate <= 0 : return -1

    return applyExchangeRate(quantity, exchangeRate)

# Met à jour la valeur du tableau `exchangeRates` correspondant à [`sourceCurr`][`targetCurr`]
# avec la nouveau valeur `exchangeRate` donnée. Met également à jour l'index inverse en calculant la
# valeur automatiquement.
def updateCurrency(exchangeRate:float, sourceCurr:int, targetCurr:int):
    if getExchangeRate(sourceCurr, targetCurr) < 0 or exchangeRate < 0: return
    exchangeRates[sourceCurr][targetCurr] = round(exchangeRate, 2)
    exchangeRates[targetCurr][sourceCurr] = round(1/exchangeRate, 2)

def printAllExchangeRates():
    print(tables.Table(
        tables.Column('', currencies),
        tables.Column('USD', list(map(str,exchangeRates[0]))),
        tables.Column('EUR', list(map(str, exchangeRates[1]))),
        tables.Column('JPY', list(map(str, exchangeRates[2]))),
        tables.Column('GBP', list(map(str, exchangeRates[3]))),
        tables.Column('CHF', list(map(str, exchangeRates[4])))
    ))
    print("\nNote: la lecture se fait dans le sens Y:X, \npar exemple le taux EUR->USD est de 1.06 et non 0.95.")

def menuUI():
    userRetry = -1
    while userRetry != 0:
        menu.Box("T A U X  D E  C H A N G E").drawBox()
        print("Devises supportées: USD - EUR - JPY - GBP - CHF\n")
        # Demande à l'utilisateur son opération choisie.
        print("1// Afficher tous les taux de change\n2// Convertir un montant en utilisant les devises supportées\n3// Convertir un montant en utilisant un taux libre\n4// Editer les taux de change\n\n0// Retour")
        userRetry = utils.getUserInput(0, 4, "→ ", "int")
        utils.jumpLines()

        match userRetry:
            case 0:
                continue
            case 1:
                print("--- TAUX DE CHANGE ACTUELS ---\n")
                printAllExchangeRates()
            case 2:
                print("--- CONVERTIR UN MONTANT ---\n")
                source = utils.getUserInput(1, 5, "Choisir la devise source: (1)USD (2)EUR (3)JPY (4)GBP (5)CHF → ", "int")
                target = -1
                while target < 1 or target == source:
                    target = utils.getUserInput(1, 5, "Choisir la devise cible: (1)USD (2)EUR (3)JPY (4)GBP (5)CHF → ", "int")
                    if target == source:
                        print("Inutile de choisir la même devise cible !")
                    utils.jumpLines()
                quantity = utils.getUserInputWithoutLimits("Entrer le montant à convertir → ")
                print(f"RESULTAT: {round(quantity, 2)}({currencies[source-1]}) → "
                      f"{round(convertToCurrency(quantity, source-1, target-1), 2)}({currencies[target-1]}) à taux {exchangeRates[source-1][target-1]}.")
            case 3:
                print("--- CONVERTIR UN MONTANT (taux libre) ---\n")
                source = utils.getUserInput(0.0001, 1000, "Entrez le taux de change → ", "float")
                utils.jumpLines()
                quantity = utils.getUserInputWithoutLimits("Entrer le montant à convertir → ")
                print(f"RESULTAT: {round(quantity, 2)} → {round(applyExchangeRate(quantity, source), 2)} à taux {source}.")
            case 4:
                print("--- EDITER LES TAUX DE CHANGE ---\n")
                print("Note: Si la taux de change mis à jour est par ex. USD-JPY, le taux\ninverse, ici JPY-USD, sera également automatiquement mis à jour.\n")
                source = utils.getUserInput(1, 5, "Choisir la devise source: (1)USD (2)EUR (3)JPY (4)GBP (5)CHF → ", "int")
                target = -1
                while target < 1 or target == source:
                    target = utils.getUserInput(1, 5, "Choisir la devise cible: (1)USD (2)EUR (3)JPY (4)GBP (5)CHF → ", "int")
                    if target == source:
                        print("Inutile de choisir la même devise cible !")
                    utils.jumpLines()
                rate = utils.getUserInput(0.0001, 1000, "Entrez le nouveau taux de change → ", "float")
                updateCurrency(rate, source-1, target-1)
                print("Les taux ont été modifiés avec succès !")

        utils.jumpLines()
        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Continuer ?")
        utils.jumpLines()