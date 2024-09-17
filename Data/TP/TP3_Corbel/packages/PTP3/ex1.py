from statistics import mean

import pandas as pd
from pandas import DataFrame

from packages.PTP3.data import DataColumnString, DataColumnNumber
from packages.PUtils import inputs, utils
from packages.PTUI import menu as menu

test_file = "production.csv"
result_file = "saved_data/production_ex1.csv"
region_file = "regions.csv"

class Ex1:
    @staticmethod
    # Récupère les deux lignes du tableau `df` dont les valeurs de la colonne
    # `col` sont immédiatement supérieures et inférieures à `x`
    def find_nearest(df, x, col="Année"):
        _min, _max = None, None
        d = (df[col] - x)

        # Ligne dont la valeur `col` est immédiatement inférieure à `x`
        condition = d[d == d[d > 0].min()]
        if len(condition) != 0:
            _max = df.loc[[d[d == d[d > 0].min()].index[0]]]

        # Ligne dont la valeur `col` est immédiatement supérieure à `x`
        condition = d[d == d[d < 0].max()]
        if len(condition) != 0:
            _min = df.loc[[d[d == d[d < 0].max()].index[0]]]

        return [_min, _max]

    @staticmethod
    # Retourne `true` si le tableau `df` contient toutes les valeurs du tableau `mandatory_col`.
    def has_mandatory_columns(df: DataFrame, mandatory_cols=None):
        if mandatory_cols is None:
            mandatory_cols = ["Année", "Production", "Région"]

        df_cols = df.columns.values.tolist()
        for i in mandatory_cols:
            name = i
            if name not in df_cols: return False
        return True

    @staticmethod
    # Vérifie la présence des colonnes `mandatory_cols` dans le tableau `df` et retire les colonnes
    # non-nécessaires au bon fonctionnement du programme.
    def sanitize_columns(df: DataFrame, mandatory_cols=None):
        if mandatory_cols is None:
            mandatory_cols = ["Année", "Production", "Région"]
        if not Ex1.has_mandatory_columns(df, mandatory_cols):
            raise ValueError(f">>> FATAL : Une ou plusieurs colonnes obligatoires sont manquantes [{mandatory_cols}]")
        df_cols = df.columns.values.tolist()
        i = 0
        for col in df_cols:
            i += 1
            if col not in mandatory_cols:
                df = df.drop(columns=[col])
                print(f">>> Colonne {i} supprimée <<< (Colonne `{col}` non-indispensable)")
        return df

    @staticmethod
    # Gigantesque fonction encapsulant la totalité des opérations d'assainissement.
    # Le choix a été fait de la garder complète car les opérations, individuellement, n'ont pas
    # vraiment de raison d'exister.
    def clear_production_data(df_prod, write=True):
        # 1. Récupération des données valides des régions
        print(" --- LECTURE DU FICHIER REGIONS... ---")
        try:
            df_reg = utils.read_csv(region_file)
            regions = df_reg["Région"].tolist()
        except Exception:
            print(f"ERREUR : Un problème est survenu pendant la lecture du fichier data/{region_file}")
            return
        print(" --- Terminé ! ---\n")

        # 2. Définition des colonnes et leurs attributs
        print(" --- RECUPERATION DES METADONNEES... ---")
        columns = [
            DataColumnString("Région", "Région", False, regions),
            DataColumnNumber("Année", "Année", True, False, 1960, 2021, False),
            DataColumnNumber("Production", "Production (en millions de tonnes)", False, True, 0, None, True)
        ]
        print(" --- Terminé ! ---\n")

        # 3. Tri des colonnes
        print(" --- TRI DES COLONNES... ---")
        df_prod = Ex1.sanitize_columns(df_prod)
        print(" --- Terminé ! ---\n")

        # 4. Nettoyage des données
        print(" --- NETTOYAGE DES DONNEES... ---")

        for index, row in df_prod.iterrows():

            # COLONNE REGION
            region = row["Région"]
            # Vérifie si la valeur de Région est identitique à l'une de celles de la liste autorisée
            # Si pas le cas:
            if region not in regions:
                # Tente de corriger la région avec l'une des régions valides
                c_region = columns[0].normalize(row["Région"])
                # Supprime la ligne si la région est invalide
                if c_region is None:
                    print(f">>> Ligne {index} supprimée <<< (Région `{region}` invalide)")
                    df_prod.drop(index, inplace=True)
                    continue
                # Remplace la région par la région corrigée
                df_prod.loc[index, 'Région'] = c_region
                print(f">>> Ligne {index} modifiée <<< (Région `{region}` remplacée par `{c_region}`)")

            # COLONNES ANNEE ET PRODUCTION

            invalid = False         # Sert à ne pas vérifier la colonne si elle a déjà été supprimée
            i = 0                   # Sert à utiliser le bon DataColumn
            for col in ["Année", "Production"]:
                if invalid: break
                i += 1

                # Conversion simple (sert à vérifier après si la variable a été modifiée)
                try:
                    base_value = float(row[col])
                except ValueError:
                    base_value = None

                # Tente de normaliser la valeur selon les critère du DataColumn utilisé
                c_value = columns[i].normalize(row[col])
                # Supprime la ligne si la normalisation retourne None
                if c_value is None:
                    print(f">>> Ligne {index} supprimée <<< ({col} `{row[col]}` invalide)")
                    df_prod.drop(index, inplace=True)
                    invalid = True
                    continue
                # Modifie la ligne si la normalisation a fonctionné
                if base_value != c_value and str(base_value) != str(c_value):
                    df_prod.loc[index, col] = c_value
                    print(f">>> Ligne {index} modifiée <<< ({col} `{row[col]}` remplacée par `{c_value}`)")
                    continue

        # Convertit le type de la colonne en numérique
        df_prod["Année"] = pd.to_numeric(df_prod["Année"])
        df_prod["Production"] = pd.to_numeric(df_prod["Production"])

        print(" --- Terminé ! ---\n")

        # 5. Traitement des doublons dans la production
        print(" --- TRAITEMENT DES DOUBLONS... ---")
        # Itère sur les lignes doublons sur les colonnes Région et Année
        for index, row in df_prod.loc[df_prod.duplicated(subset=["Région", "Année"])].iterrows():
            # Récupère l'index de la ligne originale
            initial_index = df_prod[(df_prod["Année"] == row["Année"]) & (df_prod["Région"] == row["Région"])]\
                .first_valid_index()

            # Supprime le doublon
            df_prod.drop(index, inplace=True)
            print(f">>> Ligne {index} supprimée <<< (Duplication de la ligne "
                  f"{initial_index} sur les colonnes `Région` et `Année`)")
        print(" --- Terminé ! ---\n")

        # 7. Traitement des valeurs NaN dans la Production
        print(" --- TRAITEMENT DES VALEURS VIDES... ---")
        # Itère sur toutes les lignes dont la production est NaN
        for index, row in df_prod[df_prod["Production"].isnull()].iterrows():
            # Récupère les deux valeurs (supérieures et inférieures) dont l'année est la plus proche
            nearest = Ex1.find_nearest(df_prod[(df_prod["Région"] == row["Région"])], row["Année"])

            try:
                # Tente de calculer la moyenne entre les deux
                c_mean = columns[2].normalize(
                    mean([nearest[0]["Production"].values[0], nearest[1]["Production"].values[0]]))
                df_prod.loc[index, 'Production'] = c_mean
                # Si la moyenne est NaN, c'est que l'une des deux valeurs proches était NaN également
                if str(c_mean) == "nan": raise ValueError()

                print(
                    f">>> Ligne {index} modifiée <<< (Production nulle remplacée par la moyenne des productions les plus proches)")
            # Si l'une des deux valeurs autour n'a pas été trouvée ou était NaN, supprime la ligne
            except Exception:
                df_prod.drop(index, inplace=True)
                print(
                    f">>> Ligne {index} supprimée <<< (Production nulle n'a pas pu être remplacée [manque de valeurs ou valeurs autour également nulles])")
        print(" --- Terminé ! ---\n")

        # Sauvegarde dans le fichier
        if write:
            print(" --- ECRITURE DANS LE FICHIER... ---")
            df_prod.to_csv("data/" + result_file, encoding='utf-8-sig', index=False)
            print(f" Les données ont été écrites dans le fichier `data/{result_file}`.")
            print(" --- Terminé ! ---\n")

        print(f"Opération terminée.")
        return df_prod

    # Classe Menu pour le TUI
    class Menu:
        @staticmethod
        def sub_menu_1(df):
            menu.Box("D O N N E E S  B R U T E S").drawBox()
            utils.jump_lines()
            # Affiche le contenu du fichier de base dans la console
            print(df)
            utils.jump_lines()

        @staticmethod
        def sub_menu_2(df_prod):
            menu.Box("T R A I T E M E N T  D U  F I C H I E R").drawBox()
            utils.jump_lines()
            # Traite les données
            Ex1.clear_production_data(df_prod)
            utils.jump_lines()

        @staticmethod
        def sub_menu_3():
            menu.Box("D O N N E E S  T R A I T E E S").drawBox()
            utils.jump_lines()
            # Affiche les données du fichier contenant les valeurs modifiées
            try:
                df = utils.read_csv(result_file)
                print(df)
            except Exception:
                print(f"Le fichier n'existe pas encore, ou est invalide !\n\nAvez vous déjà tenté de traiter les données brutes ? (option 1 du menu précédent)")
            utils.jump_lines()

        @staticmethod
        def main_menu():
            # charger le fichier dans un DF pandas
            try:
                df = utils.read_csv(test_file)
            except Exception:
                print(f"ERREUR : Un problème est survenu pendant la lecture du fichier data/{test_file}")
                return

            userRetry = -1
            # Répète tant que l'utilisateur ne choisit pas de quitter
            while userRetry != 0:
                menu.Box("E X 1  :  A S S A I N I S S E M E N T").drawBox()
                utils.jump_lines()

                # Options possibles
                options = ["Lire le fichier de base", "Traiter les données", "Lire le fichier modifié"]
                menu.print_menu(options)

                # Menu souhaité par l'utilisateur
                userRetry = inputs.getNumericalInput("→ ", True, 0, len(options))
                utils.jump_lines()

                match userRetry:
                    case 1:
                        Ex1.Menu.sub_menu_1(df)
                    case 2:
                        Ex1. Menu.sub_menu_2(df)
                    case 3:
                        Ex1.Menu.sub_menu_3()
                    case _:
                        break

                # Menu de sortie
                print(f"0// Continuer")
                inputs.getNumericalInput("→ ", True, 0, 0)
                utils.jump_lines()