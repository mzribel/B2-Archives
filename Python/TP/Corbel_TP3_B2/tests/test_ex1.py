import itertools
import unittest

from packages.PEx1.client import Client
from packages.PEx1.clientaccount import ClientAccount
from tests import customtestclass

class Tests_Client(customtestclass.CustomTestClass):
    """Réalise les tests relatifs à la classe Client, de l'exercice 1 du TP3."""

    # --- INITIALISATION --- #
    def test_client_init_increments_id(self):
        """Vérifie que l'id s'incrémente bien avec la création de nouveaux clients."""
        Client.iter_counter = itertools.count(0)
        client = Client("Ducanard", "Jean", "01/01/2000")
        client = Client("Ducanard", "Antoine", "01/01/2000")
        client = Client("Ducanard", "Tony", "01/01/2000")
        self.assertEqual(client.id, 2)
    def test_client_init_valid(self):
        """Initialisation valide de la classe."""
        self.assertEqual(Client("Ducanard", "Jean", "01/01/2000").lastname, "DUCANARD")
    def test_client_init_raises_when_dob_empty(self):
        """Un client de banque ne peut pas ne pas renseigner sa date de naissance.
        Si elle n'est pas renseignée, le programme lance une erreur."""
        self.assertRaises(TypeError, Client, "Ducanard", "")
    def test_client_init_raises_when_lastname_empty(self):
        """Lance une erreur si le client n'a pas de nom de famille donné."""
        self.assertRaises(ValueError, Client, "Ducanard", "", "01/01/2000")
    def test_client_init_raises_when_firstname_empty(self):
        """Lance une erreur si le client n'a pas de prénom donné."""
        self.assertRaises(ValueError, Client, "", "Jean", "01/01/2000")
    # ------------------ #

    # --- PROPRIETES --- #
    def test_client_firstname_setter_raises_when_empty(self):
        """Lance une erreur si le nouveau prénom est vide."""
        client = Client("Ducanard", "Jean", "01/01/2000")
        with self.assertRaises(ValueError):
            client.firstname = ""
    def test_client_lastname_setter_raises_when_empty(self):
        """Lance une erreur si le nouveau nom de famille est vide."""
        client = Client("Ducanard", "Jean", "01/01/2000")
        with self.assertRaises(ValueError):
            client.lastname = ""
    def test_client_age_setter_raises_accessed(self):
        """L'âge d'un client doit être calculé par sa date de naissance.
        L'accès au setter initial de Person.age est bloqué pour Client."""
        client = Client("Ducanard", "Jean", "01/01/2000")
        with self.assertRaises(AttributeError):
            client.age = 25
    def test_client_dob_setter_raises_when_None(self):
        """Vérifie que la nouvelle date de naissance n'est pas nulle."""
        client = Client("Ducanard", "Jean", "01/01/2000")
        with self.assertRaises(ValueError):
            client.dob = ""
    # ------------------ #

    # --- AFFICHAGE --- #
    def test_client_affichage(self):
        """Affiche la fonction display de la classe dans le terminal."""
        print("\n\t", end="")
        client = Client("Ducanard", "Jean", "01/01/2000").display()


class Tests_BankAccount(customtestclass.CustomTestClass):
    """Réalise les tests relatifs à la classe BankAccount, de l'exercice 1 du TP3."""

    client = Client("Ducanard", "Jean", "01/01/2000")

    # --- AFFICHAGE --- #
    def test_clientaccount_affichage(self):
        print("\n\t", end="")
        Tests_BankAccount.client.display()
    # ----------------- #

    # --- INITIALISATION --- #
    def test_clientaccount_init_raises_when_owner_underage(self):
        """Lance une erreur si le propriétaire du compte a moins de 18 ans."""
        underage_client = Client("Ducanard", "Timmy", "12/10/2020")
        self.assertRaises(ValueError, ClientAccount, underage_client)
    def test_clientaccount_init_raises_when_balance_under_overdraft(self):
        """Lance une erreur si l'utilisateur entre un solde initial inférieur au découvert."""
        self.assertRaises(ValueError, ClientAccount, Tests_BankAccount.client, -700, 0)
    def test_clientaccount_init_raises_when_negative_overdraft(self):
        """Lance une erreur si l'utilisateur entre un découvert négatif (le nombre
        est généralement donné sous forme positive par les banques."""
        self.assertRaises(ValueError, ClientAccount, Tests_BankAccount.client, 0, -700)
    # ---------------- #

    # --- METHODES --- #
    def test_clientaccount_deposit_valid_param(self):
        """Vérifie la fonction de dépôt d'argent avec des paramètres valides."""
        account1 = ClientAccount(Tests_BankAccount.client)
        account1.deposit(600)
        self.assertEqual(account1.balance, 600)
    def test_clientaccount_deposit_raises_when_null_or_negative_param(self):
        """Lance une erreur si le montant à retirer est nul ou négatif."""
        account1 = ClientAccount(Tests_BankAccount.client)
        self.assertRaises(ValueError, account1.deposit, 0)

    def test_clientaccount_withdrawal_raises_insufficient_funds(self):
        """Lance une erreur si le solde après retrait est inférieur au découvert maximum autorisé."""
        account1 = ClientAccount(Tests_BankAccount.client, 500)
        self.assertRaises(ClientAccount.InsufficientFundsException, account1.withdrawal, 600)
    def test_clientaccount_withdrawal_valid_param_with_overdraft(self):
        """Vérifie le bon fonctionnement du découvert lors des retraits."""
        account1 = ClientAccount(Tests_BankAccount.client, 0, max_overdraft=400)
        account1.withdrawal(200)
        self.assertEqual(account1.balance, -200)
    def test_clientaccount_withdrawal_valid_param(self):
        """Vérifie le bon fonctionnement de la méthode de retrait avec des paramètres valides."""
        account1 = ClientAccount(Tests_BankAccount.client, 100, max_overdraft=100)
        account1.withdrawal(200)
        self.assertEqual(account1.balance, -100)
    def test_clientaccount_transfer_ownership_valid(self):
        """Le transfert de client implique de retirer le compte des comptes de l'ancien
        propriétaire et de l'ajouter à ceux du nouveau."""
        client1 = Client("Ducanard", "Jean", "01/01/2000")
        client2 = Client("Ducoincoin", "Denis", "01/01/1976")
        account1 = ClientAccount(client1, 200)
        account1.owner = client2
        with self.subTest():
            self.assertEqual(len(client1.account_list), 0)
        with self.subTest():
            self.assertEqual(len(client2.account_list), 1)
    def test_clientaccount_transfer_ownership_raises_wrong_param_type(self):
        """Lance une erreur si le propriétaire du compte est set à null."""
        account1 = ClientAccount(Client("Ducanard", "Jean", "01/01/2000"), 200)
        with self.assertRaises(ValueError):
            account1.owner = None

if __name__ == '__main__':
    unittest.main(verbosity=2)

