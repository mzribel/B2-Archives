import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
        menu.Box("M A T R I C E S").drawBox()
        utils.jump_lines()

        print("Affichage de la matrice \"Répartition des paquets de pâtes en fonction du type et de la marque \"...")
        crossed = pd.crosstab(df["Marque"], df["Type"])
        ax = sns.heatmap(crossed, annot=True, cmap=sns.cubehelix_palette(as_cmap=True, reverse=True))
        plt.tight_layout()
        plt.show()

        print(
            "Affichage de la matrice \"Moyennes du prix au kilo des paquets de pâtes en fonction de la marque et du poids\"...")
        df_heatmap = df.pivot_table(values='Prix au kilo', index='Marque', columns="Poids", aggfunc="mean")
        ax = sns.heatmap(df_heatmap, annot=True, cmap=sns.cubehelix_palette(as_cmap=True))
        plt.tight_layout()
        plt.show()

        print(
            "Affichage de la matrice \"Moyennes du prix au kilo des paquets de pâtes en fonction du type et du poids\"...")
        df_heatmap = df.pivot_table(values='Prix au kilo', index='Type', columns="Poids", aggfunc="mean")
        ax = sns.heatmap(df_heatmap, annot=True, cmap=sns.cubehelix_palette(as_cmap=True))
        plt.tight_layout()
        plt.show()
        utils.jump_lines()

    @staticmethod
    def sub_menu_3(df):
        # 3. Covariance / Corrélation
        menu.Box("C O V A R  /  C O R R").drawBox()
        utils.jump_lines()

        # Covariance et corrélation poids/prix
        print("Poids / Prix du paquet")
        cov_weight = df['Poids'].cov(df['Prix'])
        print("   - Covariance : ", round(cov_weight, 2))
        corr_weight = df['Poids'].corr(df['Prix'])
        print("   - Coeff. de corrélation : ", round(corr_weight, 2))
        utils.jump_lines()

        # Covariance et corrélation poids/prix au kilo
        print("Poids / Prix au kilo")
        cov_weight = df['Poids'].cov(df['Prix au kilo'])
        print("   - Covariance : ", round(cov_weight, 2))
        corr_weight = df['Poids'].corr(df['Prix au kilo'])
        print("   - Coeff. de corrélation : ", round(corr_weight, 2))
        utils.jump_lines()

    @staticmethod
    def sub_menu_4(df):
        # 4. Nuages de points
        menu.Box("N U A G E S  D E  P T S").drawBox()
        utils.jump_lines()

        print(
            "Affichage du nuage de points \"Répartition des prix au kilo des paquets de pâtes en fonction du poids\"...")
        ax = df.plot.scatter(x="Poids", y="Prix au kilo")
        plt.tight_layout()
        plt.show()

        print(
            "Affichage du nuage de points \"Répartition des prix unitaires des paquets de pâtes en fonction du poids\"...")
        ax = df.plot.scatter(x="Poids", y="Prix")
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

            options = ["Informations", "Matrices", "Covariance et corrélation", "Nuages de points"]
            menu.print_menu(options)

            userRetry = inputs.getNumericalInput("→ ", True, 0, 4)
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
                case _:
                    break
            # Menu pour réessayer ou quitter

            # Menu retry (0 = quitter, 1 = réessayer).
            userRetry = menu.drawBinaryMenu("Voulez-vous continuer")
            utils.jump_lines()
