import matplotlib.pyplot as plt

from packages.PTP2 import ex1, ex2
from sklearn import linear_model
from packages.PUtils import files, inputs, utils
from packages.PUtils import menu_tui as menu

class Menu:
    @staticmethod
    def sub_menu_1(df):
        # 1. Informations
        menu.Box("I N F O R M A T I O N S").drawBox()
        utils.jump_lines()
        print(df.head(), "\n")
        print("Total : ", df["Prix"].count(), "\n")

    @staticmethod
    def sub_menu_2(df):
        # 2. Matrices
        ex2.Menu.sub_menu_2(df)

    @staticmethod
    def sub_menu_3(df):
        # 3. Moyennes
        ex1.Menu.sub_menu_3(df)

    @staticmethod
    def sub_menu_4(df):
        # 4. Médianes
        ex1.Menu.sub_menu_4(df)

    @staticmethod
    def sub_menu_5(df):
        # 5. Variances
        ex1.Menu.sub_menu_5(df)

    @staticmethod
    def sub_menu_6(df):
        # 6. Droites de régression
        menu.Box("D R O I T E S  D E  R E G R .").drawBox()
        utils.jump_lines()

        print(
            "Affichage de la droite de régression linéaire \"Répartition des prix au kilo des paquets de pâtes en fonction du poids\"...")
        length = df["Poids"].count()
        x = df["Poids"].values.reshape(length, 1)
        y = df["Prix au kilo"].values.reshape(length, 1)
        regr = linear_model.LinearRegression()
        regr.fit(x, y)
        plt.scatter(x, y)
        plt.plot(x, regr.predict(x), color='violet', linewidth=3)
        plt.xlabel('Poids')
        plt.ylabel('Prix au kilo')
        plt.tight_layout()
        plt.show()

        print(
            "Affichage de la droite de régression linéaire \"Répartition des prix unitaires des paquets de pâtes en fonction du poids\"...")
        y = df["Prix"].values.reshape(length, 1)
        regr = linear_model.LinearRegression()
        regr.fit(x, y)
        plt.scatter(x, y)
        plt.plot(x, regr.predict(x), color='violet', linewidth=3)
        plt.xlabel('Poids')
        plt.ylabel('Prix du paquet')
        plt.tight_layout()
        plt.show()
        utils.jump_lines()

    @staticmethod
    def main_menu():
        """Définit le menu pour l'exercice TP2.1: Nombres premiers
                :return: None"""

        userRetry = -1
        # Répète tant que l'utilisateur ne choisit pas de quitter
        while userRetry != 0:
            menu.Box("E X E R C I C E  2").drawBox()
            utils.jump_lines()

            # charger le fichier dans un DF pandas
            df = files.csv_to_df("pates_carrefour")
            df["Prix au kilo"] = df["Prix"] / df["Poids"]

            options = ["Informations", "Matrices", "Moyennes", "Médianes", "Variances", "Droites de régression linéaire"]
            menu.print_menu(options)

            userRetry = inputs.getNumericalInput("→ ", True, 0, 6)
            utils.jump_lines()

            match userRetry:
                case 1:
                    Menu.sub_menu_1(df)
                case 2:
                    Menu.sub_menu_2(df)
                case 3:
                    Menu.sub_menu_3(df)
                case 4:
                    Menu.sub_menu_4(df)
                case 5:
                    Menu.sub_menu_5(df)
                case 6:
                    Menu.sub_menu_6(df)
                case _:
                    break
            # Menu pour réessayer ou quitter

            # Menu retry (0 = quitter, 1 = réessayer).
            userRetry = menu.drawBinaryMenu("Voulez-vous continuer")
            utils.jump_lines()
