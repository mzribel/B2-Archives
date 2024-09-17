import pandas as pd
from packages.PTP3.ex1 import Ex1
from packages.PTP3.ex2 import Ex2
from packages.PTUI import menu

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    print("ATTENTION : Le fichier traité est volumineux ! Mais si vous utilisez les menus qui permettent de lire\n"
          "les fichiers avant/après, regardez les dernières lignes : beaucoup de coquilles s'y trouvent !\n")

    menu.Menu(textBox=menu.Box("M E N U  P R I N C I P A L"), options=[
        menu.MenuOption("Assainissement des données", Ex1.Menu.main_menu),
        menu.MenuOption("Traitement des valeurs aberrantes", Ex2.Menu.main_menu)
    ]).drawMenu()