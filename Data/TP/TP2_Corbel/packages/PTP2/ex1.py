import matplotlib.pyplot as plt
from packages.PUtils import files, inputs, utils
from packages.PUtils import menu_tui as menu

def calculate_grouped_stats(df, groupby=None, col="Prix au kilo", func="mean", round=2):
    if groupby is None:
        groupby = []
    if len(groupby) == 0 or len(col) == 0:
        return

    match func:
        case "mean":
            temp = df.groupby(groupby)[col].mean().dropna().reset_index()
            temp[col] = temp[col].round(round)
            return temp
        case "median":
            temp = df.groupby(groupby)[col].median().dropna().reset_index()
            temp[col] = temp[col].round(round)
            return temp
        case "var":
            temp = df.groupby(groupby)[col].var().dropna().reset_index()
            temp[col] = temp[col].round(round)
            return temp
        case "std":
            temp = df.groupby(groupby)[col].std().dropna().reset_index()
            temp[col] = temp[col].round(round)
            return temp
        case _:
            return

def print_grouped_values(df, col1="", col2="Prix au kilo", intro="", suffix="€", prefix="   - "):
    print(intro)
    for i in range(df[col2].count()):
        index = df.iloc[i][col1]
        value = df.iloc[i][col2]
        print(prefix+ str(index) + " : " + str(value) + suffix)

def get_value_proportions(df, col, rounded=2):
   try:
       return round(df[col].value_counts(normalize=True) * 100, rounded)
   except:
       return False

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
        # 2. Statistiques globales
        menu.Box("S T A T S  D E S  P R I X").drawBox()
        utils.jump_lines()
        print("Statistiques des prix par paquet :\n", df["Prix"].describe().round(2), "\n")
        print("Statistiques des prix au kilo :\n", df["Prix au kilo"].describe().round(2), "\n")

    @staticmethod
    def sub_menu_3(df):
        # 3. Moyennes
        menu.Box("M O Y E N N E S").drawBox()
        utils.jump_lines()

        avg_price = round(df["Prix"].mean(), 2)
        print("Moyenne du prix d'un paquet : " + str(avg_price) + "€")
        avg_kg_price = round(df["Prix au kilo"].mean(), 2)
        print("Moyenne du prix au kilo : " + str(avg_kg_price) + "€")
        utils.jump_lines()

        brand_gp = calculate_grouped_stats(df, ["Marque"])
        print_grouped_values(brand_gp, "Marque", intro="Moyenne des prix au kilo par marque :")
        utils.jump_lines()

        weight_gp = calculate_grouped_stats(df, ["Poids"])
        print_grouped_values(weight_gp, "Poids", intro="Moyenne des prix au kilo par poids de paquet :")
        utils.jump_lines()

    @staticmethod
    def sub_menu_4(df):
        # 4. Médianes
        menu.Box("M E D I A N E S").drawBox()
        utils.jump_lines()

        med_price = round(df["Prix"].median(), 2)
        print("Médiane du prix d'un paquet : " + str(med_price) + "€")
        med_price = round(df["Prix au kilo"].median(), 2)
        print("Médiane du prix au kilo : " + str(med_price) + "€")
        utils.jump_lines()

        brand_gp = calculate_grouped_stats(df, ["Marque"], func="median")
        print_grouped_values(brand_gp, "Marque", intro="Médiane des prix au kilo par marque ---")
        utils.jump_lines()

        weight_gp = calculate_grouped_stats(df, ["Poids"], func="median")
        print_grouped_values(weight_gp, "Poids", intro="Médiane des prix au kilo par poids du paquet ---")
        utils.jump_lines()

    @staticmethod
    def sub_menu_5(df):
        # 5. Variances
        menu.Box("V A R I A N C E S").drawBox()
        utils.jump_lines()

        var_price = round(df["Prix"].var(), 2)
        print("Variance du prix d'un paquet : " + str(var_price) + "€")
        var_price = round(df["Prix au kilo"].var(), 2)
        print("Variance du prix au kilo : " + str(var_price) + "€")
        utils.jump_lines()

        brand_gp = calculate_grouped_stats(df, ["Marque"], func="var")
        print_grouped_values(brand_gp, "Marque", intro="Variance des prix au kilo par marque ---")
        utils.jump_lines()

        weight_gp = calculate_grouped_stats(df, ["Poids"], func="var")
        print_grouped_values(weight_gp, "Poids", intro="Variance des prix au kilo par poids du paquet ---")
        utils.jump_lines()

    @staticmethod
    def sub_menu_6(df):
        # 6. Ecarts-Type
        menu.Box("E C A R T S  T Y P E").drawBox()
        utils.jump_lines()

        std_price = round(df["Prix"].std(), 2)
        print("Ecart-type du prix d'un paquet : " + str(std_price) + "€")
        std_price = round(df["Prix au kilo"].std(), 2)
        print("Ecart-type du prix au kilo : " + str(std_price) + "€")
        utils.jump_lines()

        brand_gp = calculate_grouped_stats(df, ["Marque"], func="std")
        print_grouped_values(brand_gp, "Marque", intro="Ecart-type des prix au kilo par marque ---")
        utils.jump_lines()

        weight_gp = calculate_grouped_stats(df, ["Poids"], func="std")
        print_grouped_values(weight_gp, "Poids", intro="Ecart-type des prix au kilo par poids du paquet ---")
        utils.jump_lines()

    @staticmethod
    def sub_menu_7(df):
        # 7. Diagrammeq
        menu.Box("D I A G R A M M E S").drawBox()
        utils.jump_lines()

        print("Affichage de l'histogramme \"Prix des pâtes au kilo\"...")
        ax = df.hist(column="Prix au kilo", sharex=True, color='#86bf91', zorder=2, rwidth=0.9, bins=25)
        plt.tight_layout()
        plt.show()

        print("Affichage du diagramme en boîte \"Prix du paquet en fonction du type de pâtes\"...")
        ax = df.plot.box(column="Prix", by="Type")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
        utils.jump_lines()

    @staticmethod
    def sub_menu_8(df):
        # 8. Probabilités
        menu.Box("P R O B A B I L I T E S").drawBox()
        utils.jump_lines()

        print("Réparition des paquets de pâtes en fonction de leur type (%) :")
        print(get_value_proportions(df, "Type"))
        utils.jump_lines()

        print("Réparition des paquets de pâtes en fonction de leur marque (%) :")
        print(get_value_proportions(df, "Marque"))
        utils.jump_lines()

        print("Réparition des paquets de pâtes en fonction de leur poids (%) :")
        print(get_value_proportions(df, "Poids"))
        utils.jump_lines()

    @staticmethod
    def main_menu():
        """Définit le menu pour l'exercice TP2.1: Nombres premiers
                :return: None"""

        userRetry = -1
        # Répète tant que l'utilisateur ne choisit pas de quitter
        while userRetry != 0:
            menu.Box("E X E R C I C E  1").drawBox()
            utils.jump_lines()

            # charger le fichier dans un DF pandas
            df = files.csv_to_df("pates_carrefour")
            df["Prix au kilo"] = df["Prix"] / df["Poids"]

            options = ["Informations", "Statistiques des prix", "Moyennes", "Médianes", "Variances", "Ecarts-type", "Diagrammes", "Probabilités"]
            menu.print_menu(options)

            userRetry = inputs.getNumericalInput("→ ", True, 0, 8)
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
                case 7:
                    Menu.sub_menu_7(df)
                case 8:
                    Menu.sub_menu_8(df)
                case _:
                    break
            # Menu pour réessayer ou quitter

            # Menu retry (0 = quitter, 1 = réessayer).
            userRetry = menu.drawBinaryMenu("Voulez-vous continuer")
            utils.jump_lines()












