import re
from PUtils import menu


# Demande un chiffre à l'utilisateur et traite les erreurs.
# `inputType` ["int" ou "float"] permet de renseigner le type du nombre voulu.
# `intro` est la phrase qui précède la demande d'une nouvelle valeur à l'utilisateur.
# `minValue` et `maxValue` représente les limites minimale et maximale pour le nombre.
def getUserInput(minValue, maxValue, intro, inputType:str="int"):
    global userinput
    while True:
        try:
            userinput = input(intro)
            if inputType == "int":
                userinput = int(userinput)
            else:
                userinput = float(userinput)
        except ValueError:
            print("/!\\ On ne veut que des chiffres entiers !!\n") if bool(re.search("^ *[+-]?(\\d+\\.\\d*) *$", userinput)) else print("/!\\ Il faudrait peut-être essayer avec un chiffre...\n")
        except KeyboardInterrupt:
            exit(1)
        else:
            if minValue > userinput or maxValue < userinput:
                print(f"/!\\ Ce nombre est un poil petit, ou grand..? [{minValue}:{maxValue}]\n")
                continue
            return userinput

def getUserInputWithoutLimits(intro:str):
    global userinput
    while True:
        try:
            userinput = float(input(intro))
        except ValueError:
            print("/!\\ Il faudrait peut-être essayer avec un chiffre...\n")
        except KeyboardInterrupt:
            exit(1)
        else:
            return userinput

# Fonction "raccourcie" pour sauter les lignes (plus esthétiques que des `print` vides).
# `number` représente le nombre de lignes à sauter.
def jumpLines(number=1):
    # Check la validité du nombre fourni.
    if number < 0:
        return
    print("\n"*number, sep='', end='', flush=True)

# Oui.
def drawMeSomething():
    menu.Box("L E  C A N A R D  ( T I M I D E )").drawBox()
    jumpLines()
    print(
"              ⢀⣀⡼⠚⠉⠉⠉⠙⢯⣢ ",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢺⠊⠀⠀⣀⠀⠀⠀⠀⢱⣧⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣮⠃⠀⠀⠘⠛⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀  Bonjour...",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⢀⣼⠒⣺⣻⠀⠀⠀⠀⠀  On est bien ici non..?",
"⠀⠀⠀⠀⠀⠀⠀⣀⡤⠖⠒⠛⠃⠀⠀⠀⠀⠀⠀⢞⠁⠈⠉⡿⡿⡄⠀⠀⠀⠀",
"⠀⠀⠀⢀⣴⡴⠊⠁⠀⠀⠀⡴⠁⠀⠀⠀⠀⠀⠀⠈⠛⠦⣄⡀⣹⣖⠀⠀⠀⠀",
"⠀⠀⢀⣾⡏⠀⠀⠀⠀⠀⠜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣧⠀⠀⠀",
"⠀⠀⣎⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀",
"⣠⣠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠈⠳⡅",
"⢳⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⠤⠒⠈⢞⣁⣀⣀⡀⢀⡀⣀⡀⠓⠉⠒⠦⡀⠀⢱",
"⡾⠀⠀⠀⠀⠀⠀⠀⢰⠛⠉⠀⠀⠀⢰⠛⠛⠛⠁⠈⠙⠛⠛⡇⠀⠀⠀⠈⠛⡄",
"⢻⠀⠀⠀⠀⠀⠀⠀⠸⣄⣀⣀⡀⢀⡎⠀⠀⠀⠀⠀⠀⠀⠀⢳⡀⠀⣀⣀⣠⠃",
"⢸⡄⠀⠀⠀⠀⠀⠀⠀⠈⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠈⠁⢠",
"⠸⡽⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡼",
"⠀⠙⠹⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⡞⠀",
"⠀⠀⠀⠀⠙⢲⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⡶⠛⠉⠀⠀",
"⠀⠀⠀⠀⠀⠘⢿⣿⣿⣶⡦⠶⠶⣾⠏⠉⠉⠉⠉⠉⠉⢉⢿⣿⣷⠃⠀⠀",
"⠀⠀⠀⠀⠀⠀⢸⠁⡸⠷⣶⣴⣶⣦⡀⠀⠀⢀⣤⣤⣴⣵⡿⢞⠿⡶⣄⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠻⠤⠿⠧⠶⠶⠤⢧⠃⠀⠀⠙⠾⢟⣛⣁⣒⣻⣅⣙⡾⠀⠀⠀", sep="\n")
    jumpLines()

    getUserInput(0, 0, "0// Quitter\n→ ")
    jumpLines()
