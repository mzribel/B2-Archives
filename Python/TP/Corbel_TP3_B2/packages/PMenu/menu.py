from packages.PMenu.titlebox import TitleBox
from packages.PUtils import inputs
import time

class Menu:
    # Classe permettant de lier un titre d'option `optionTitle` à une fonction `optionFunction`.
    class Option:
        def __init__(self, optionTitle, module, out, optionFunction: callable = None):
            self.optionTitle = optionTitle
            self.optionFunction = optionFunction
            self.module = module
            self.out = out

    # `quitOption` permet de choisir le texte qui s'affichera pour l'option 0 (retour).
    # `layer` représente le niveau du menu: `layer`=0 signifie qu'il s'agit du premier menu,
    # le quitter suppose l'arrêt du programme.
    def __init__(self, menu_title="Menu Principal", app_title:str="", options:list[Option]=None, quitOption="Quitter", layer:int=0):
        self.textBox = TitleBox(menu_title, app_title)
        self.options = options
        self.quitOption = quitOption
        self.layer = layer

    def draw(self):
        userRetry = -1

        while userRetry != 0:
            # Dessine la textBox si elle a été renseignée.
            if bool(self.textBox): self.textBox.draw()

            # Print les options du menu.
            if self.options and len(self.options) >= 1:
                for index, element in enumerate(self.options):
                    print(f"{index+1}// {element.optionTitle}")
                print()
            # Print l'option "quitter" du menu.
            print(f"0// {self.quitOption}")

            userRetry =  inputs.getNumericalInput("→ ", True, 0, len(self.options) if self.options else 0)
            self.jump_lines()

            # Si `layer`>0, la réponse de l'utilisateur sera retournée mais le programme ne s'arrêtera pas.
            if self.layer == 0:
                if userRetry == 0:
                    print("Bonne journée !! ♪")
                    time.sleep(1)
                    return
                else:
                    if self.options[userRetry - 1].optionFunction is not None:
                        self.options[userRetry - 1].optionFunction(self.module, self.out)
                    else:
                        print(f"Option n°{userRetry}: {self.options[userRetry - 1].optionTitle}\n")
            else:
                return userRetry

    @staticmethod
    # Print un menu simple binaire, sans fonction associée aux options.
    # `intro` représente la chaîne de caractères qui introduit le choix,
    # `option` et `quitOption` permettent de personnaliser les deux options.
    def draw_binary_menu(intro: str, option: str = "Oui", quitOption: str = "Quitter"):
        print(intro)

        print(f"1// {option}")
        print(f"0// {quitOption}")
        return inputs.getNumericalInput("→ ", True, 0, 1)

    @staticmethod
    def jump_lines(number=1):
        """Saute un nombre de lignes donné en paramètre."""
        # Check la validité du nombre fourni.
        if number < 0:
            return
        print("\n" * number, sep='', end='', flush=True)

    @staticmethod
    def generate(menu_title="Menu Principal", app_title:str="", options:list[Option]=None, quitOption="Quitter", layer:int=0):
        Menu(menu_title, app_title, options, quitOption, layer).draw()