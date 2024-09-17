import csv
import datetime
import random

import numpy as np
import scipy as sp
import scipy.fftpack
import pandas as pd
import matplotlib.pyplot as plt
from packages.PUtils import inputs, utils
from packages.PUtils import menu_tui as menu

def generate_dates(start_year, end_year):
    start_date = datetime.datetime(start_year, 1, 1)
    end_date = datetime.datetime(end_year, 12, 31)
    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime('%Y-%m-%d')
        current_date += datetime.timedelta(days=32 - current_date.day)

# Fonction pour générer un prix aléatoire entre 0.5 et 1
def generate_price():
    return round(random.uniform(0.5, 1), 2)

def generate_data_in_file(filename="pates_generees.csv"):
    # Écrire les données dans un fichier CSV
    with open('pates_generees.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Prix'])

        avg_price = 0.7
        trend = [-0.03, -0.06, -0.1, -.05, 0, 0, 0, .04, .1, .05, 0, 0]
        for y in range(2000, 2024):
            avg_price += avg_price * 0.019
            print(y, avg_price)
            for m in range(1, 13):
                min_price = avg_price+avg_price*trend[m-1] * .95
                max_price = (avg_price + avg_price * trend[m - 1])*1.05
                writer.writerow([f"{m}/01/{y}", round(random.uniform(min_price, max_price))])

def calculate_power(df):
    try:
        date = pd.to_datetime(df["Date"])
        prix = df["Prix"]
        N = len(prix)

        prix_fft = sp.fftpack.fft(prix.values)
        prix_psd = np.abs(prix_fft) ** 2
        fftfreq = sp.fftpack.fftfreq(len(prix_psd), 1. / 12)

        i = fftfreq > 0

        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        ax.plot(fftfreq[i], 10 * np.log10(prix_psd[i]))
        ax.set_xlim(0, 5)
        ax.set_xlabel('Frequency (1/year)')
        ax.set_ylabel('PSD (dB)')
        plt.show()

        # prix_fft_bis = prix_fft.copy()
        # prix_fft_bis[np.abs(fftfreq) > 1.1] = 0
        # prix_slow = np.real(sp.fftpack.ifft(prix_fft_bis))
        # fig, ax = plt.subplots(1, 1)
        # prix.plot(ax=ax, lw=1)
        # ax.plot_date(date, prix_slow, '-')
        # # ax.set_xlim(datetime.date(1999, 1, 1), datetime.date(2000, 1, 1))
        # ax.set_ylim(0.6, 1.3)
        # ax.set_xlabel("Date")
        # ax.set_ylabel("Prix")
        # plt.show()

    except:
        print("Une erreur est survenue")
        return False

class Menu:
    @staticmethod
    def sub_menu_1(df, filename):
        # 1. Informations
        menu.Box("I N F O R M A T I O N S").drawBox()
        utils.jump_lines()
        print("Fichier utilisé : "+filename)
        print(df.head(), "\n")
        print("Total : ", df["Prix"].count(), "\n")

    @staticmethod
    def sub_menu_2(df, filename):
        # 2. Diagrammes (Insee)
        menu.Box("D I A G R A M M E S").drawBox()
        utils.jump_lines()
        print("Fichier utilisé : "+filename)
        print(
            "Affichage de la courbe \"Relevé mensuels du prix moyen du paquet de pâtes entre 1999 et 2019\"...")
        ax = df.plot(x='Date', y='Prix')
        plt.show()

        print(
            "Affichage de la courbe \"Courbe du spectre de puissance pour le prix moyen du paquet de pâtes entre 1999 et 2019\"...")
        calculate_power(df)
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
            filename_insee = "pates_insee.csv"
            filename_gen = "pates_generees.csv"

            temp_df = pd.read_csv("data/"+filename_insee, parse_dates=["Date"])
            df_insee = temp_df.groupby('Date')["Prix"].mean().dropna().reset_index()
            df_insee.reset_index()
            temp_df = pd.read_csv("data/"+filename_gen, parse_dates=["Date"])
            df_gen = temp_df.groupby('Date')["Prix"].mean().dropna().reset_index()
            df_gen.reset_index()

            options = ["Informations (données Insee)", "Diagrammes (données Insee)", "Informations (données générées)", "Diagrammes (données générées)"]
            menu.print_menu(options)

            userRetry = inputs.getNumericalInput("→ ", True, 0, 4)
            utils.jump_lines()

            match userRetry:
                case 1:
                    Menu.sub_menu_1(df_insee, filename_insee)
                case 2:
                    Menu.sub_menu_2(df_insee, filename_insee)
                case 3:
                    Menu.sub_menu_1(df_gen, filename_gen)
                case 4:
                    Menu.sub_menu_2(df_gen, filename_gen)
                case _:
                    break
            # Menu pour réessayer ou quitter

            # Menu retry (0 = quitter, 1 = réessayer).
            userRetry = menu.drawBinaryMenu("Voulez-vous continuer")
            utils.jump_lines()
