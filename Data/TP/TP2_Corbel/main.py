from packages.PUtils import menu_tui as menu
from packages.PTP2 import ex1, ex2, ex3, ex4

if __name__ == '__main__':
    menu.Menu(textBox=menu.Box("M E N U  P R I N C I P A L"), options=[
        menu.MenuOption("Exercice 1", ex1.Menu.main_menu),
        menu.MenuOption("Exercice 2", ex2.Menu.main_menu),
        menu.MenuOption("Exercice 3", ex3.Menu.main_menu),
        menu.MenuOption("Exercice 4", ex4.Menu.main_menu),
        menu.MenuOption("Miam !", menu.bonus)
    ]).drawMenu()

