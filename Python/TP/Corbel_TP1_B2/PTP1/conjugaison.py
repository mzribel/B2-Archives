import json
from PUtils import menu, utils, tables

# Récupère le verbe à l'infinitif fourni en paramètre dans le json des verbes conjugués.
# Retourne None si aucune correspondance n'est trouvée.
def getVerbFromJSON(verbName:str):
    with open('data/verbes_lowercase.json', encoding="utf-8") as f:
        data = json.load(f)
        return next((verb for verb in data if verbName in verb['infinitif']["présent"]), None)

# Affiche les verbes conjugués sous les trois temps de l'indicatif les plus communs.
def printVerbs(verbData, verbName):
    nums = [ 'je', 'tu', 'il/elle', 'nous', 'vous', 'ils/elles']
    print(f"   --- Conjugaison de {verbName.upper()} à l'indicatif ---")
    verbData = verbData["indicatif"]
    print(tables.Table(
        tables.Column('', nums),
        tables.Column('PRESENT', verbData["présent"]),
        tables.Column('IMPARFAIT', verbData["imparfait"]),
        tables.Column('PASSE SIMPLE', verbData["passé simple"]),
        ))

def menuUI():
    userRetry = -1
    while userRetry != 0:
        menu.Box("C O N J U G U E U R").drawBox()
        utils.jumpLines()

        # Demande à l'utilisateur de rentrer un verbe.
        chosenVerb = input("Entrez un verbe à l'infinitif → ")
        result = (getVerbFromJSON(chosenVerb))
        # En fonction du résultat, print ou non les tableaux des conjugaisons.
        if result is None:
            print("Aucun verbe correspondant n'a été trouvé.")
        else:
            utils.jumpLines()
            printVerbs(result, chosenVerb)
        utils.jumpLines()

        # Menu retry (0 = quitter, 1 = réessayer).
        userRetry = menu.drawBinaryMenu("Voulez vous conjuguer un autre verbe ?")
        utils.jumpLines()


