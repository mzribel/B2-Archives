from PUtils import utils, inputs
import time
from os import system

# Crée une textBox de 3x`width` contenant du texte `content`.
# Si `title` n'est pas vide, rajoute `title` en haut à gauche de la textBox, sur la ligne haute.
class Box:
    def __init__(self, content, title="Python B2 TP n°2", width=48, height=3):
        self.title = title.strip()
        self.content = content.strip()
        self.height = height
        self.width = width

    # Dessine la textBox.
    def drawBox(self):
        # Ajoute deux espaces de padding autour de `title` pour la lisibilité.
        if len(self.title) != 0:
            self.title = f" {self.title.strip()} "
        # Ne fonctionne pas si la textBox n'a pas de `content`.
        if len(self.content) == 0:
            return


        # Print la textBox et son contenu:
        print(f"┌{self.title.ljust(self.width, '─')}┐")
        print(f"|{self.content.center(self.width)}|")
        print(f"└{'─'*self.width}┘")

# Classe permettant de lier un titre d'option `optionTitle` à une fonction `optionFunction`.
class MenuOption:
    def __init__(self, optionTitle, optionFunction:callable=None):
        self.optionTitle = optionTitle
        self.optionFunction = optionFunction

# Crée un menu et ses choix d'options.
class Menu:
    # `quitOption` permet de choisir le texte qui s'affichera pour l'option 0 (retour).
    # `layer` représente le niveau du menu: `layer`=0 signifie qu'il s'agit du premier menu,
    # le quitter suppose l'arrêt du programme.
    def __init__(self, textBox:Box=None, options:list[MenuOption]=None, quitOption="Quitter", layer:int=0):
        self.textBox = textBox
        self.options = options
        self.quitOption = quitOption
        self.layer = layer

    def drawMenu(self):
        userRetry = -1

        while userRetry != 0:
            # Dessine la textBox si elle a été renseignée.
            if bool(self.textBox):
                self.textBox.drawBox()
                utils.jump_lines()

            # Print les options du menu.
            if len(self.options) >= 1:
                for index, element in enumerate(self.options):
                    print(f"{index+1}// {element.optionTitle}")
                print()
            # Print l'option "quitter" du menu.
            print(f"0// {self.quitOption}")

            userRetry =  inputs.getNumericalInput("→ ", True, 0, len(self.options))
            utils.jump_lines()

            # Si `layer`>0, la réponse de l'utilisateur sera retournée mais le programme ne s'arrêtera pas.
            if self.layer == 0:
                if userRetry == 0:
                    print("Bonne journée !! ♪")
                    time.sleep(1)
                    continue
                else:
                    if self.options[userRetry-1].optionFunction is not None:
                        self.options[userRetry-1].optionFunction()
                    else:
                        print(f"Option n°{userRetry}: {self.options[userRetry-1].optionTitle}\n")
            else:
                return userRetry
        return 0

# Print un menu simple binaire, sans fonction associée aux options.
# `intro` représente la chaîne de caractères qui introduit le choix,
# `option` et `quitOption` permettent de personnaliser les deux options.
def drawBinaryMenu(intro:str, option:str="Oui", quitOption:str="Quitter"):
    print(intro)

    print(f"1// {option}")
    print(f"0// {quitOption}")
    return inputs.getNumericalInput("→ ", True, 0, 1)

