from typing import List

from packages.PEx1.clientaccount import ClientAccount
from packages.PEx1.client import Client

class BankManager:
    """Classe "tiroir" destinée à afficher les éléments plus facilement."""

    # --- CONSTRUCTEUR --- #
    def __init__(self):
        self.client_list:List[Client] = []
        self.account_list:List[ClientAccount] = []

    # -------------------- #

    # --- METHODES --- #
    def print_accounts(self):
        for account in self.account_list:
            print(account)
    def print_clients(self):
        for client in self.client_list:
            print(client)

    # --------------- #