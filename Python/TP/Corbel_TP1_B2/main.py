from PUtils import menu
from PTP1 import calculator, operations, conjugaison, palindrome, currency

if __name__ == '__main__':
    menu.Menu(textBox=menu.Box("M E N U  P R I N C I P A L"), options=[
        menu.MenuOption("Calculatrice", calculator.menuUI),
        menu.MenuOption("Somme et factorielle", operations.menuUI),
        menu.MenuOption("Conjugueur de verbes", conjugaison.menuUI),
        menu.MenuOption("Convertisseur de devises", currency.menuUI),
        menu.MenuOption("Vérificateur de palindrome", palindrome.menuUI),
    ]).drawMenu()
