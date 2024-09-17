import json
import statistics
# PIP INSTALL numpy, pandas
import numpy as np
import pandas as pd
from PUtils import utils, inputs, menu_tui as menu

class Ex4:
    """Contient les méthodes nécessaires à l'exercice TP2_4: Analyse de données d'âge."""

# Proprietés statiques
    default_grps = [-1, 13, 25, 35, 45, 55, np.inf]

# Méthodes statiques
    @staticmethod
    def get_df_from_groups(lst, groups=None)->pd.DataFrame|None:
        """Divise une liste de valeur numériques par les délimiteurs de groupes données en paramètres. Si aucun n'est donné,
        prend par défaut celle de Ex3.default_grps.
        :return: pd.Dataframe|None"""
        if groups is None:
            groups = Ex4.default_grps
        groups = [np.inf if x == "inf" else x for x in groups]
        lst = utils.sanitize_age_list(lst, groups[0] + 1, None if groups[-1] == 100 else groups[-1])
        if len(lst) == 0:
            return None
        # Lance une erreur si `lst` n'est pas un itérable composé de nb_personness.
        utils.check_numerical_list_validity(lst)

        # Formate les groupes et les étiquettes à utiliser dans le tableau.
        labels = utils.bins_to_labels(groups)

        # Crée le DataFrame utilisé pour séparer les valeurs en groupes.
        df = pd.DataFrame({"age": lst})
        df["groupe"] = pd.cut(df["age"], bins=groups, labels=utils.bins_to_labels(groups))

        # Regroupe les données par groupe d'âges, ajoute le compte et la moyenne de chaque groupe.
        df = df.groupby("groupe", observed=True) \
            .agg(nb_personnes=("groupe", "size"), age_moyen=("age", "mean")) \
            .reset_index().round(1)

        # Ajoute les champs manquants (n'ayant aucune valeur correspondant au groupe):
        for i in range(len(labels)):
            if not any(df["groupe"].isin([labels[i]])):
                df.loc[len(df)] = [labels[i],0, 0]

        # Réorganise les valeurs et renvoie le tableau
        df = df.sort_values(by="groupe").reset_index(drop=True)
        return df

    @staticmethod
    def get_group_frequency(lst, groups=None)->list:
        """Renvoie un array des fréquences de chaque groupe.
        :return: list"""
        return Ex4.get_df_from_groups(lst, groups)["nb_personnes"] if not None else []

def get_weighted_avg(lst:dict, weight_lst:list=None)-> int|float:
    """Renvoie la moyenne pondérée d'un groupe de nombres.
    :return:int|float"""
    if len(lst) == 0: return 0
    if weight_lst is None or len(weight_lst) != len(lst):
        raise ValueError("Le paramètre `weight_lst` doit comprendre le même nombre d'élément que le paramètre `lst`.")

    weightedMean = 0
    total_weight = 0
    i = 0
    for key, value in lst.items():
        weight = value["nb_personnes"] * (weight_lst[i])
        weightedMean += value["age_moyen"] * weight
        total_weight += weight
        i += 1

    return weightedMean / total_weight

# Todo: Refactoriser correctement cette fonction, très répétitive et maladroite)
def submenu():
    """Définit le menu pour l'exercice TP2.1: Nombres premiers
    :return: None"""

    userRetry = -1
    # Répète tant que l'utilisateur ne choisit pas de quitter.
    while userRetry != 0:
        menu.Box("M O Y E N N E  P O N D E R E E").drawBox()
        utils.jump_lines()

        print("1// Afficher l'exemple\n2// Etudiants par âges en France\n3// Âges et poids aléatoires\n\n0// Retour")
        userRetry = inputs.getNumericalInput("→ ", True, 0, 4)
        utils.jump_lines()

        match userRetry:
            case 1:
                menu.Box("E X E M P L E", title="TP2.4: Moyenne Pondérée").drawBox()
                utils.jump_lines()
                with open("data/ages.json") as f:
                    # Récupère les données dans le JSON
                    data = json.load(f)
                    lst, bins =  utils.sanitize_age_list(data["example"]["list"],data["example"]["bins"][0]-1, data["example"]["bins"][-1]), data["example"]["bins"]
                    # Crée la base des deux dataframes
                    df1 = df2 = Ex4.get_df_from_groups(lst, bins)
                    if df1 is None or df2 is None:
                        print("Aucune valeur dans le tableau !!")
                        break
                    values = df1.set_index("groupe")[["age_moyen","nb_personnes"]].to_dict(orient="index")

                    # Complète et affiche le dataframe sans coefficient
                    no_weight = [1] * len(values)
                    df1["poids"] = no_weight
                    print(f"   -> Exemple 1 (aucun poids) <-\n{df1.to_string(index=False)}\n----\n"
                          f"Moyenne: {round(statistics.mean(lst), 1)}\nMoyenne pondérée: {round(get_weighted_avg(values, no_weight), 1)}\n")

                    # Complète et affiche le dataframe avec coefficients.
                    weighted = list(range(1, len(values) + 1))
                    df2["poids"] = weighted
                    print(f"   -> Exemple 2 (pondéré) <-\n{df1.to_string(index=False)}\n---\n"
                          f"Moyenne: {round(statistics.mean(lst), 1)}\nMoyenne pondérée: {round(get_weighted_avg(values, weighted), 1)}")
                    print("\nNOTE: Il y a deux tableaux au-dessus! Pensez à agrandir le terminal :)")
            case 2:
                menu.Box("A G E  D E S  E T U D I A N T S", title="TP2.4: Moyenne Pondérée").drawBox()
                utils.jump_lines()
                with open("data/ages.json") as f:
                    # Récupère les données dans le JSON
                    data = json.load(f)
                    lst, bins = utils.sanitize_age_list(data["students"]["list"],data["students"]["bins"][0]-1, data["students"]["bins"][-1]), data["students"]["bins"]
                    # Crée la base du dataframe
                    df = Ex4.get_df_from_groups(lst, bins)
                    if df is None:
                        print("Aucune valeur dans le tableau !!")
                        break
                    # Récupère les valeurs et les ajoute au dataframe
                    values = df.set_index("groupe")[["age_moyen", "nb_personnes"]].to_dict(orient="index")
                    weighted = list(range(1, len(values)))+[10]
                    df["poids"] = weighted
                    # Affiche le dataframe
                    print(f"{df.to_string(index=False)}\n----\n"
                          f"Moyenne: {round(statistics.mean(lst), 1)}\nMoyenne pondérée: {round(get_weighted_avg(values, weighted), 1)}")
            case 3:
                menu.Box("V A L E U R S  A L E A T O I R E S", title="TP2.4: Moyenne Pondérée").drawBox()
                utils.jump_lines()
                # Génère les valeurs et crée la base du dataframe
                arr = utils.generate_random_numberList(0, 100, 1000)
                df = Ex4.get_df_from_groups(arr)
                if df is None:
                    print("Aucune valeur dans le tableau !!")
                    break
                # Récupère les valeurs et les poids et les ajoute au dataframe
                values = df.set_index("groupe")[["age_moyen", "nb_personnes"]].to_dict(orient="index")
                weighted = utils.generate_random_numberList(1, (len(values)+1*2), len(values))
                df["poids"] = weighted
                # Affiche le dataframe
                print(f"{df.to_string(index=False)}\n----\n"
                      f"Moyenne: {round(statistics.mean(arr), 1)}\nMoyenne pondérée: {round(get_weighted_avg(values, weighted), 1)}")
            case _:
                break
        # Menu pour réessayer ou quitter
        utils.jump_lines()
        userRetry = menu.drawBinaryMenu("Voulez-vous continuer?")
        utils.jump_lines()
