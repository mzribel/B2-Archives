import itertools

from dateutil.relativedelta import relativedelta

from packages.PEx1.anonymousaccount import AnonymousAccount
from packages.PEx1.client import Client
from datetime import datetime

class ClientAccount(AnonymousAccount):
    """Classe permettant de créer un compte bancaire associé à un compte client.
    Implémentation concrète de AnonymousAccount."""

    # --- CONSTRUCTEUR --- #
    def __init__(self, owner: Client, initial_balance: float = 0, max_overdraft: int = 0):
        super().__init__(initial_balance, max_overdraft)
        self.owner: Client = owner
    # ------------------- #

    # --- PROPRIETES --- #
    # OWNER
    @property
    def owner(self)->Client:
        return self._owner
    @owner.setter
    def owner(self, new_owner:Client):
        """Change le propriétaire du compte.
                Implique de retirer le compte de la liste de ceux possédés par l'ancien propriétaire,
                et d'ajouter le nouveau compte à la liste de ceux possédés par le nouveau."""

        if type(new_owner) is not Client:
            raise ValueError("Le propriétaire du compte doit être un client (classe Client).")

        # Vérifie si l'âge du nouveau propriétaire est valide.
        age_from_DoB = relativedelta(datetime.now(), new_owner.dob).years  # calcul de l'âge
        if age_from_DoB < 18:
            raise ValueError("Le propriétaire du compte doit être une personne majeure.")

        if hasattr(self, "_owner"):
            self._owner.account_list.remove(self)
        new_owner.account_list.append(self)

        self._owner = new_owner
    # ------------------ #

    def __str__(self):
        return (f"Compte n°{self.id} - Solde: {self.balance}{self.currency} - Découvert max: {self.max_overdraft}{self.currency}" +
                f"\n   Appartient à: n°{self.owner.id} {self.owner.get_full_name()} - {self.owner.get_str_dob()} ({self.owner.age} ans)")