import datetime

from packages.PEx2.person import Person
from packages.PEx1.anonymousaccount import AnonymousAccount
import itertools
from typing import List

class Client(Person):
    iter_counter = itertools.count()
    name_re = r"[A-Za-zÀ-ÖØ-öø-ÿ'-\ ]{1,30}"

    # --- CONSTRUCTEUR --- #
    def __init__(self, lastname:str, firstname:str, DoB:str):
        # Champs obligatoires
        if lastname == "" or firstname == "" or DoB == "":
            raise ValueError("Les champs `firstname`, `lastname` et `DoB` sont obligatoires et doivent être non nuls.")

        # Crée la base du Client en partant de sa classe parente Person
        super().__init__(lastname, firstname, DoB)
        # Attributs propres à Client
        self.id = next(Client.iter_counter)
        self.account_list:List[AnonymousAccount] = []

    # ------------------- #

    # --- PROPRIETES --- #

    # FIRSTNAME
    @Person.firstname.setter
    def firstname(self, new_firstname:str):
        """Précise le setter original: le prénom ne doit pas être vide."""
        super(Client, type(self)).firstname.fset(self, new_firstname)
        if not self.firstname:
            raise ValueError("Les paramètres `firstname` et `lastname` ne peuvent pas être vides.")

    # LASTNAME
    @Person.lastname.setter
    def lastname(self, new_lastname:str):
        """Précise le setter original: le nom de famille ne doit pas être vide."""
        super(Client, type(self)).lastname.fset(self, new_lastname)
        if not self.lastname:
            raise ValueError("Les paramètres `firstname` et `lastname` ne peuvent pas être vides.")

    # AGE
    @Person.age.setter
    def age(self, new_age):
        """Retire le setter original: un compte en banque à besoin de l'âge précis du client, basé sur sa date de naissance."""
        raise AttributeError("Impossible de modifier la propriété âge: seule la date de naissance peut être manuellement modifiée.")

    # DATE OF BIRTH
    @Person.dob.setter
    def dob(self, new_dob):
        """Précise le setter de la classe de base: la date de naissance ne doit pas être supprimée du client."""
        super(Client, type(self)).dob.fset(self, new_dob)
        if not new_dob:
            raise ValueError("La date de naissance ne peut pas être vide ou non-spécifiée..")

    # ----------------- #

    # --- METHODES --- #
    def __str__(self):
        result = f"Client n°{self.id} - {self.get_full_name()} - {self.get_str_dob()} ({self.age} ans)"
        for account in self.account_list:
            result += "\n   " + AnonymousAccount.__str__(account)
        return result

    @staticmethod
    def sanitize_name(string:str, re=None) ->str:
        sanitized_str = super().sanitize_name(string)
        regex = re.compile(Client.name_re)
        if not regex.match(sanitized_str):
            raise ValueError("Le nom et le prénom ne peuvent contenir que des caractères alphabétiques, ainsi que ' et -.")
        return sanitized_str