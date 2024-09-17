import itertools
from datetime import datetime
from abc import ABC

# Tentative (certainement très maladroite) d'inversion des dépendances:
# La relation trop forte entre Client (contenant une liste de BankAccount)
# et BankAccount (possédant un owner Client) créait une dépendance circulaire.

class AnonymousAccount(ABC):
    """Classe permettant de créer un compte bancaire sans compte client associé.
    Abstraite dans la mesure où l'existence d'un compte sans propriétaire est inutile."""
    iter_counter = itertools.count()
    class InsufficientFundsException(Exception):
        """Exception levée quand le compte n'a pas assez de fonds pour la transaction."""

    # --- CONSTRUCTEUR --- #
    def __init__(self, initial_balance: float = 0, max_overdraft: int = 0):
        initial_balance = round(initial_balance, 2)
        if initial_balance < 0 - max_overdraft:
            raise ValueError("La balance initiale ne peut pas être inférieure au découvert autorisé.")
        self.id = next(AnonymousAccount.iter_counter)
        self.creation_date = datetime.now()
        self._balance: float = round(initial_balance, 2)
        self.max_overdraft: int = max_overdraft
        self.currency = "EUR"
    # ------------------- #

    # --- PROPRIETES --- #

    # BALANCE
    @property
    def balance(self)->float:
        return self._balance
        # NOTE: Aucun setter n'est

    @balance.setter
    def balance(self, new_balance:float):
        # Lance une erreur si le nouveau solde est inférieur au découvert max. autorisé.
        if new_balance < 0 - self.max_overdraft:
            raise AnonymousAccount.InsufficientFundsException(
                "Les fonds actuels et le découvert autorisé de ce compte ne permettent"
                " pas cette transaction.")

        self._balance = new_balance

    # MAX_OVERDRAFT (= DECOUVERT MAXIMUM AUTORISE)
    @property
    def max_overdraft(self)->int:
        return self._max_overdraft

    @max_overdraft.setter
    def max_overdraft(self, new_overdraft):
        # Lance une erreur si le nouveau découvert autorisé est négatif.
        if new_overdraft < 0:
            raise ValueError("Le découvert maximum autorisé doit être écrit sous forme positive, ou égal à 0.")

        self._max_overdraft = new_overdraft

    # ----------------------- #

    # --- METHODES --- #
    def deposit(self, amount: float):
        amount = round(amount, 2)
        if amount <= 0:
            raise ValueError("On ne peut pas déposer une somme nulle ou négative sur un compte.")
        self.balance += amount

    def withdrawal(self, amount: float):
        amount = round(amount, 2)
        if amount <= 0:
            raise ValueError("On ne peut pas retirer une somme nulle négative d'un compte.")
        self.balance -= amount
    def __str__(self):
        """Retourne une version lisible de l'objet sous forme string."""
        return f"Compte n°{self.id} - Solde: {self.balance}{self.currency} - Découvert max: {self.max_overdraft}{self.currency}"

    def display(self, verbose=True):
        """Print l'objet dans la console à partir de sa méthode __str__."""
        print(self.__str__())



