from packages.PTP3.ex1 import Ex1
from packages.PTUI import menu
from packages.PUtils import utils, inputs
from packages.PUtils.utils import HiddenPrints
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest

test_file = "production.csv"
result_file = "saved_data/production_ex2.csv"

class Ex2:
    @staticmethod
    # Utilise le z-score sur la colonne "Production" pour supprimer les valeurs aberrante d'un dataframe.
    # Threshold désigne les valeurs maximale et minimale acceptées
    # Iterations désigne le nombre de boucles de suppression réalisées.
    def apply_zscore(df, threshold=3, iterations=3):
        print(f" --- NETTOYAGE DES VALEURS ABERRANTES (ZSCORE)... ---")

        for i in range(iterations):
            print(f" --- ITERATION n°{i + 1} ---")
            # Sépare le dataframe en sous-tableaux régionaux
            for region in df["Région"].unique():
                # Duplique le tableau pour ne pas ajouter de colonne au tableau réel
                region_df = df[(df["Région"] == region)].copy()
                region_df["z-score"] = stats.zscore(region_df["Production"])

                # Récupère les valeurs jugées anormales
                outliers = region_df[(region_df["z-score"] > threshold) | (region_df["z-score"] < -threshold)]
                if outliers.empty:
                    continue

                # Retire chaque valeur considérée anormale du dataframe
                for index, outlier in outliers.iterrows():
                    df.drop(index, inplace=True)
                    print(
                        f">>> Ligne {index} supprimée <<< (Le z-score `{round(outlier['z-score'], 2)}` lié à la Production dans "
                        f"\n\t\tla Région `{outlier['Région']}` rend la valeur {round(outlier['Production'], 2)} aberrante)")
        print(f" --- Terminé ! ---")
        return df

    @staticmethod
    def apply_dbscan(df, eps=50):
        print(f" --- NETTOYAGE DES VALEURS ABERRANTES (DBSCAN)... ---")
        # Sépare le dataframe en sous-tableaux régionaux

        for region in df["Région"].unique():
            # Duplique le tableau pour ne pas ajouter de colonne au tableau réel
            temp = df[(df["Région"] == region)].copy()
            # Retire la colonne "Région" pour ne pas faire planter le programme
            X = temp[["Année", "Production"]]

            # Applique l'algorithme DBSCAN aux données
            db = DBSCAN(eps=eps, min_samples=3).fit(X)
            labels = db.labels_

            # Crée le diagramme
            unique_labels = set(labels)
            core_samples_mask = np.zeros_like(labels, dtype=bool)
            core_samples_mask[db.core_sample_indices_] = True

            colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
            for k, col in zip(unique_labels, colors):
                if k == -1:
                    col = [0, 0, 0, 1]

                class_member_mask = labels == k

                xy = X[class_member_mask & core_samples_mask]
                plt.plot(xy.iloc[:, 0], xy.iloc[:, 1], "o", markerfacecolor=tuple(col), markeredgecolor="k", markersize=14)

                xy = X[class_member_mask & ~core_samples_mask]
                plt.plot(xy.iloc[:, 0], xy.iloc[:, 1], "o", markerfacecolor=tuple(col), markeredgecolor="k", markersize=6)

            plt.title(f"Clusters pour la Région {region}")
            # Affiche le diagramme
            plt.show()

            # Récupère les valeurs jugées anormales
            outliers = X[labels == -1]
            # Retire chaque valeur considérée anormale du datafram
            for index, outlier in outliers.iterrows():
                df.drop(index, inplace=True)
                print(
                    f">>> Ligne {index} supprimée <<< (la valeur de Production {round(outlier['Production'], 2)} dans la région {region} a été jugée aberrante par DBSCAN)")

        print(" --- Terminé ! ---\n")
        return df

    @staticmethod
    def apply_isolation_forest(df, n_estimators=50, contamination=float(0.05)):
        print(" --- NETTOYAGE DES VALEURS ABERRANTES (DBSCAN)... ---")
        print("ATTENTION !! Cette méthode est utilisée à titre informatif : l'inconstance des résultats ne rend pas"
              "\npertinente la sauvegarde des données, elles ne seront pas réellement supprimées.\n")

        # Sépare le dataframe en sous-tableaux régionaux
        for region in df["Région"].unique():
            # Duplique le tableau pour ne pas ajouter de colonne au tableau réel
            temp = df[(df["Région"] == region)].copy()[["Année", "Production"]]

            # Applique l'algorithme isolation forest aux données
            model = IsolationForest(n_estimators=n_estimators, max_samples='auto', contamination=float(contamination))
            model.fit(temp)
            labels = model.predict(temp)

            # Crée le diagramme
            plt.scatter(temp.iloc[:,0], temp.iloc[:,1], c=labels)
            plt.title(f"Isolation Forest pour la Région {region}")
            plt.show()

            # Récupère les valeurs jugées anormales
            outliers = temp[labels == -1]
            # Retire chaque valeur considérée anormale du dataframe
            for index, outlier in outliers.iterrows():
                # df_prod.drop(index, inplace=True)
                print(f">>> Ligne {index} supprimée <<< (la valeur de Production {round(outlier['Production'], 2)} dans la région {region} a été jugée aberrante par DBSCAN)")

        print(" --- Terminé ! ---\n")
        # return df

    class Menu:
        @staticmethod
        def sub_menu_1(df):
            menu.Box("D O N N E E S  B R U T E S").drawBox()
            utils.jump_lines()
            # Affiche le contenu du fichier de base dans la console
            print(df)
            utils.jump_lines()

        @staticmethod
        def sub_menu_2(df, write=True):
            menu.Box("Z - S C O R E").drawBox()
            utils.jump_lines()
            # Traite les données
            changed = Ex2.apply_zscore(df)
            utils.jump_lines()

            # Sauvegarde des données
            if write:
                print(" --- ECRITURE DANS LE FICHIER... ---")
                changed.to_csv("data/" + result_file, encoding='utf-8-sig', index=False)
                print(f" Les données ont été écrites dans le fichier `data/{result_file}`.")
                print(" --- Terminé ! ---\n")

        @staticmethod
        def sub_menu_3(df, write=True):
            menu.Box("D B S C A N").drawBox()
            utils.jump_lines()
            # Traite les données
            changed = Ex2.apply_dbscan(df)
            utils.jump_lines()

            # Sauvegarde des données
            if write:
                print(" --- ECRITURE DANS LE FICHIER... ---")
                changed.to_csv("data/" + result_file, encoding='utf-8-sig', index=False)
                print(f" Les données ont été écrites dans le fichier `data/{result_file}`.")
                print(" --- Terminé ! ---\n")

        @staticmethod
        def sub_menu_4(df):
            menu.Box("D B S C A N").drawBox()
            utils.jump_lines()

            # Affiche les étapes de l'isolation forest
            Ex2.apply_isolation_forest(df)

        @staticmethod
        def sub_menu_5():
            menu.Box("D O N N E E S  T R A I T E E S").drawBox()
            utils.jump_lines()

            # Affiche les données du fichier contenant les valeurs modifiées
            try:
                df = utils.read_csv(result_file)
                print(df)
            except Exception:
                print(
                    f"Le fichier {result_file} n'existe pas encore, ou est invalide !\n\nAvez vous déjà tenté de traiter les données brutes ? (options 2-4 du menu précédent)")
            utils.jump_lines()

        @staticmethod
        def main_menu():
            # charger et traiter le fichier dans un DF pandas
            try:
                base_df = utils.read_csv(test_file)
                # Traite le fichier avec les fonctions de l'exercice 1
                # de manière silencieuse
                with HiddenPrints():
                    base_df = Ex1.clear_production_data(base_df, False)
            except Exception:
                print(f"ERREUR : Un problème est survenu pendant la lecture du fichier data/{test_file}")
                return

            userRetry = -1
            # Répète tant que l'utilisateur ne choisit pas de quitter
            while userRetry != 0:
                df = base_df.copy()
                menu.Box("E X  2  : A L G O R I T H M E S").drawBox()
                utils.jump_lines()
                print(f"NOTE : Cet exercice charge au préalable les données du fichier {test_file}\n"
                      f"et les traite avec les fonctions de l'exercice 1 avant d'appliquer les algorithmes.\n")

                # Options possibles
                options = ["Lire le fichier de base", "Traiter avec z-score", "Traiter avec DBSCAN", "Traiter avec Isolation Forest", "Lire le dernier fichier traité"]
                menu.print_menu(options)

                # Menu souhaité par l'utilisateur
                userRetry = inputs.getNumericalInput("→ ", True, 0, len(options))
                utils.jump_lines()

                match userRetry:
                    case 1:
                        Ex2.Menu.sub_menu_1(df)
                    case 2:
                        Ex2.Menu.sub_menu_2(df)
                    case 3:
                        Ex2.Menu.sub_menu_3(df)
                    case 4:
                        Ex2.Menu.sub_menu_4(df)
                    case 5:
                        Ex2.Menu.sub_menu_5()
                    case _:
                        break

                # Menu de sortie
                print(f"0// Continuer")
                inputs.getNumericalInput("→ ", True, 0, 0)
                utils.jump_lines()