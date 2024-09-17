from PUtils import menu_tui as menu
from PTP2 import ex1, ex2, ex3, ex4, ex5

if __name__ == '__main__':
    menu.Menu(textBox=menu.Box("M E N U  P R I N C I P A L"), options=[
        menu.MenuOption("Test de nombre premier", ex1.submenu),
        menu.MenuOption("Calcul de la moyenne et de la médiane", ex2.submenu),
        menu.MenuOption("Calcul de la variance et de l'écart-type", ex3.submenu),
        menu.MenuOption("Analyse de données d'âge", ex4.submenu),
        menu.MenuOption("Simulation de lancers de dés", ex5.submenu),
    ]).drawMenu()

