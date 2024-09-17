import tkinter
from tkinter import *
from pandastable import Table
import pandas as pd
from tkinter import ttk
from packages.PUtils.files import csv_to_df

class TPMenu:
    def __init__(self, title="TP - Marianne C.", w=1000, h=600, iconfile: str | None= "icon.ico"):
        #  Base configuration
        self.root = Tk()
        self.root.geometry(f"{w}x{h}")
        if iconfile: self.root.iconbitmap(iconfile)
        self.root.title(title)
        self.root.resizable(False, False)

        self.base_data: pd.DataFrame | None = None

        header = Frame(padx=5, pady=5)
        header.pack(anchor=tkinter.NW)
        # Buttons frame
        btn_ctn = Frame(header, pady=5)
        btn_ctn.pack(anchor=tkinter.NW)
        # Buttons
        button1 = Button(btn_ctn, height=2, width=10, text="Exercice 1", command=self.exercice_1)
        button1.pack(anchor=tkinter.NW, side=tkinter.LEFT)
        button2 = Button(btn_ctn, height=2, width=10, text="Exercice 2", command=self.exercice_2)
        button2.pack(anchor=tkinter.NW, side=tkinter.LEFT)
        button3 = Button(btn_ctn, height=2, width=10, text="Exercice 3", command=self.exercice_3)
        button3.pack(anchor=tkinter.NW, side=tkinter.LEFT)
        button4 = Button(btn_ctn, height=2, width=10, text="Exercice 4", command=self.exercice_4)
        button4.pack(anchor=tkinter.NW, side=tkinter.LEFT)
        button5 = Button(btn_ctn, height=2, width=10, text="Exercice 5", command=self.exercice_5)
        button5.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        self.enonce = Label(text="Enoncé : ", font="font='Helvetica 12 bold")
        self.enonce.pack(anchor=tkinter.NW)




        self.main = Frame(padx=5, pady=5)  # first page, which would get widgets gridded into it
        self.main.pack(fill="both", expand=True)

        self.stats_ctn = ttk.Frame(self.main)

        self.mean1_ctn = Frame(self.stats_ctn)
        self.mean1_ctn.pack(anchor=NW)
        Label(self.mean1_ctn, text="Moy. valeur marchande :", font='Helvetica 10 bold').pack(side=LEFT)
        self.mean1 = Label(self.mean1_ctn, text="--€")
        self.mean1.pack(side=LEFT)
        self.mean2_ctn = Frame(self.stats_ctn)
        self.mean2_ctn.pack(anchor=NW)
        Label(self.mean2_ctn, text="Méd. valeur marchande :", font='Helvetica 10 bold').pack(side=LEFT)
        self.mean2 = Label(self.mean2_ctn, text="--€")
        self.mean2.pack(side=LEFT)

        self.table_ctn = ttk.Frame(self.main)
        self.table_ctn.pack(anchor=NW, expand=True, fill=BOTH)
        self.table = Table(self.table_ctn, dataframe=self.get_base_data(), editable=True, enable_menus=False, cols=0, rows=0)
        self.table.show()

        self.initialize()

    def initialize(self):
        self.exercice_1()

    def get_base_data(self, filename:str="timbres"):
        self.base_data = csv_to_df(filename)

    def set_enonce(self, enonce:str):
        self.enonce.config(text="Enoncé : "+enonce)

    def update_table(self, new_df:pd.DataFrame):
        self.table.model.df = new_df
        self.table.redraw()

    def exercice_1(self):
        self.set_enonce("Afficher le tableau")
        if self.base_data is None:
            self.get_base_data("timbres")
        self.update_table(self.base_data)
        self.stats_ctn.pack_forget()

    def exercice_2(self):
        self.set_enonce("Afficher les timbres venant de France")
        temp = self.base_data.loc[self.base_data["Pays d'émission"]=="France"]
        self.update_table(temp)
        self.stats_ctn.pack_forget()

    def exercice_3(self):
        self.set_enonce("Afficher la moyenne des valeurs marchandes")
        self.update_table(self.base_data)
        temp = round(pd.to_numeric(self.base_data["Valeur marchande"], errors="coerce").mean(), 2)
        self.mean1.config(text=f"{temp}€")
        temp = round(self.base_data["Valeur marchande"].median(), 2)
        self.mean2.config(text=f"{temp}€")
        self.stats_ctn.pack(before=self.table_ctn, anchor=tkinter.NW, pady=5)

    def exercice_4(self):
        self.set_enonce("Afficher les timbres dont la valeur marchande >= 100€")
        temp = self.base_data.loc[self.base_data["Valeur marchande"]>=100]
        self.update_table(temp)
        self.stats_ctn.pack_forget()

    def exercice_5(self):
        self.set_enonce("Trier les timbres par valeur marchande descendante")
        temp = self.base_data.sort_values(by=["Valeur marchande"], ascending=False)
        self.update_table(temp)
        self.stats_ctn.pack_forget()