# TP 3.2: CREATION D'UNE CLASSE PERSONNE
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from packages.PUtils import format

class Person:
    """Définit la classe Person et ses propriétés de base."""

    # --- CONSTRUCTEUR --- #
    def __init__(self, lastname:str|None="", firstname:str|None="", dob:str|None="", age:int|None=None):
        # Assigne les valeur de base aux attributs "privées": passer par le setter lancerait une exception.
        self._firstname: str = Person.sanitize_name(firstname).title() if firstname is not None else ""
        self._lastname:str = Person.sanitize_name(lastname).upper() if lastname is not None else ""
        if self.lastname == "" and self.firstname == "":
            raise ValueError("Il faut remplir au minimum un des deux champs parmi `firstname` et `lastname`.")

        if dob:
            self.dob = dob
        else:
            self.age = age

    # ------------------- #

    # --- PROPRIETES --- #
        # NOTE: Puisque tous les attributs doivent être sanitized ou dépendent d'autres attributs,
        # tous sont déclarés en tant que propriétés et ont un setter spécifique.

    # LASTNAME
    @property
    def lastname(self):
        return self._lastname
    @lastname.setter
    def lastname(self, new_lastname:None|str):
        # Sanitize le nouveau nom.
        new_lastname = Person.sanitize_name(new_lastname) \
            if type(new_lastname) is str else ""
        # Lance une exception si les deux noms, après modification théorique, seraient vides.
        if new_lastname == "" and self.firstname == "":
            raise ValueError("Il faut remplir au minimum un des deux champs parmi `firstname` et `lastname`.")

        self._lastname = new_lastname.upper()

    # FIRSTNAME
    @property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, new_firstname:None|str):
        # Satintize le nouveau nom.
        new_firstname = Person.sanitize_name(new_firstname) \
            if type(new_firstname) is str else ""
        # Lance une exception si les deux noms, après modification théorique, seraient vides.
        if new_firstname == "" and self.lastname == "":
            raise ValueError("Il faut remplir au minimum un des deux champs parmi `firstname` et `lastname`.")

        self._firstname = new_firstname.title()

    # DATE OF BIRTH
    @property
    def dob(self):
        return self._dob
    def get_str_dob(self):
        """Renvoie une string de la date de naissance au format dd/mm/yyyy."""
        return format.date_to_string(self.dob)
    @dob.setter
    def dob(self, new_dob:str|None):
        """Ce setter est dépendant du setter de @age.
        Lorsqu'une des deux propriétés est modifiée, la deuxième l'est également."""
        if new_dob == "" or new_dob is None:
            # Reset l'âge et la date de naissance.
            self._dob = self._age = None
            return
        try:
            # Traduit la string en objet datetime.
            self._dob = datetime.strptime(new_dob, "%d/%m/%Y")
            self._age = relativedelta(datetime.now(), self._dob).years
        except ValueError as e:
            raise ValueError(f"Le format de la date de naissance est incorrect (dd/mm/yyyy).")
        if self._age < 0 or self._age > 125:
            raise ValueError("L'âge doit être compris entre 0 et 125 ans.")

    # AGE
    @property
    def age(self):
        # Recalcule l'âge à partir de la date de naissance si elle existe (dans le cas où la mise à jour n'est pas
        # automatique, accéder à la valeur la met automatiquement à jour).
        if type(self.dob) is datetime:
            self._age = relativedelta(datetime.now(), self._dob).years

        return self._age
    @age.setter
    def age(self, new_age:int|None):
        # Reset l'âge et la date de naissance.
        if new_age is None:
            self._dob = self._age = None
            return
        # Vérifie la validité de l'âge.
        if new_age < 0 or new_age > 125:
            raise ValueError("L'âge doit être compris entre 0 et 125 ans.")

        self._dob = None
        self._age = new_age

    # ------------------ #

    @staticmethod
    # Cette méthode retourne le résultat d'une fonction, ce qui peut paraître inutile.
    # Elle existe pour être potentiellement override par une classe qui nécessiterait
    # une sanitization plus stricte des noms.
    def sanitize_name(string:str)->str:
        return format.sanitize_str_whitespace(string)

    # Retourne une string contenant les deux noms, dans l'ordre où ils sont demandés.
    def get_full_name(self, firstname_first:bool=False):
        if firstname_first:
            return self.firstname.title() + (" " if self.firstname != "" else "") + self.lastname.upper()
        return self.lastname.upper() + (", " if self.lastname != "" else "") + self.firstname.title()

    # Retourne une version lisible de l'objet.
    def __str__(self):
        result = f"{self.get_full_name()}"
        if self.age:
            result += f" - {self.age} an(s)"
        if self.dob:
            result += f" [{self.get_str_dob()}]"
        return result

    # Print l'objet dans la console à partir de sa méthode __str__.
    def display(self):
        print(self.__str__())


