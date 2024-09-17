import datetime
import unittest

from packages.PEx3.contact import Contact
from packages.PEx3.contactmanager import ContactManager
from tests import customtestclass


class Tests_Contact(customtestclass.CustomTestClass):
    """Réalise les tests relatifs à la classe Contact, de l'exercice 2 du TP3."""
    # --- AFFICHAGE --- #
    def test_contact_affichage(self):
        print()
        print(Contact("Ducanard", "Richard", "0504030201", "richardducanard@gmail.com"))

class Tests_ContactManager(customtestclass.CustomTestClass):
    """Réalise les tests relatifs à la classe ContactManager, de l'exercice 2 du TP3."""

    # --- RETRAIT D'UN CONTACT --- #
    def test_contact_remove_from_list_valid(self):
        """Vérifie le bon fonctionnement du retrait d'un contact."""
        # Setup
        contact_manager = ContactManager()
        contact = Contact("Ducanard", "Jean")
        contact_manager.contact_list = [contact,
            Contact("Dujambon", "Tony", "0102030405"),
            Contact("Ducanard", "Richard", "0504030201", "richardducanard@gmail.com")]
        # Fonction et test
        contact_manager.remove_contact(contact)
        self.assertNotIn(contact, contact_manager.contact_list)
    def test_remove_from_list_not_in_list(self):
        """Passe sous silence l'erreur lancée si le contact n'est pas ou plus dans la liste."""
        # Setup
        contact_manager = ContactManager()
        contact = Contact("Ducanard", "Jean")
        contact_manager.contact_list = [Contact("Dujambon", "Tony", "0102030405"),
                                        Contact("Ducanard", "Richard", "0504030201", "richardducanard@gmail.com")]
        # Fonction et test
        contact_manager.remove_contact(contact)
        self.assertEqual(len(contact_manager.contact_list), 2)
    # -------------- #

    # --- AJOUT D'UN CONTACT --- #
    def test_contact_add_to_list_valid(self):
        """Vérifie le bon fonctionnement d'un ajout valide de contact."""
        # Setup
        contact_manager = ContactManager()
        contact = Contact("Ducanard", "Jean")
        # Exécution et test
        contact_manager.add_contact(contact)
        self.assertIn(contact, contact_manager.contact_list)

    # --- TRI DES CONTACTS --- #
    def test_sort_list_when_contact_list_changed(self):
        # Vérifie que la liste est bien triée lorsque son setter est utilisé.
        # Setup
        contact_manager = ContactManager()
        # Setup et exécution dans le setter
        contact_manager.contact_list = [Contact("Ducanard", "Jean"),Contact("Dujambon", "Tony", "0102030405"),
                                        Contact("Ducanard", "Richard", "0504030201", "richardducanard@gmail.com")]
        # Test
        self.assertEqual(contact_manager.contact_list[0].firstname, "Jean")

    def test_sort_list_when_order_by_changed(self):
        # Vérifie que la liste se trie automatiquement lorsque l'ordre est changé.
        contact_manager = ContactManager()
        # Setup et exécution dans le setter
        contact_manager.contact_list = [Contact("Ducanard", "Valentine"), Contact("Dujambon", "Antoine", "0102030405"),
                                        Contact("Ducanard", "Richard", "0504030201", "richardducanard@gmail.com")]
        contact_manager.order_by = "firstname"
        self.assertEqual(contact_manager.contact_list[0].firstname, "Antoine")

    def test_sorted_list_returns_copy(self):
        """Vérifie que la fonction retourne une copie de la liste de contact triée,
        sans impacter la liste réelle."""
        contact_manager = ContactManager()
        # Setup et exécution dans le setter
        # Liste organisée par prénom
        contact_manager.contact_list = [Contact("Ducanard", "Valentine"), Contact("Dujambon", "Antoine", "0102030405"),
                                        Contact("Ducanard", "Richard", "0504030201", "richardducanard@gmail.com")]
        # Récupère une copie de la liste organisé par nom de famille
        sorted_contact_list = ContactManager.sorted_contacts(contact_manager.contact_list, "lastname")
        # Vérifie que les deux éléments en tête de liste sont les premiers dans leurs ordres respectifs.
        self.assertEqual(contact_manager.contact_list[0].firstname, "Antoine")
        self.assertEqual(sorted_contact_list[0].firstname, "Richard")

    # --- RECHERCHE D'UN CONTACT --- #
    def test_find_first_empty_param(self):
        """Vérifie que le programme ne cherche rien lorsque le paramètre de recherche est vide."""
        contact_manager = ContactManager()
        # Setup et exécution dans le setter
        contact_manager.contact_list = [Contact("Ducanard", "Valentine"), Contact("Dujambon", "Antoine", "0102030405"),
                                        Contact("Ducanard", "Richard", "0504030201", "richardducanard@gmail.com")]
        self.assertIsNone(contact_manager.find_first(""))
    def test_find_all_empty_param(self):
        """Vérifie que le programme ne cherche rien lorsque le paramètre de recherche est vide."""
        contact_manager = ContactManager()
        # Setup et exécution dans le setter
        contact_manager.contact_list = [Contact("Ducanard", "Valentine"), Contact("Dujambon", "Antoine", "0102030405"),
                                        Contact("Ducanard", "Richard", "0504030201", "richardducanard@gmail.com")]
        self.assertEqual(contact_manager.find_all(""), [])

    def test_find_first_by_names(self):
        """Vérifie le bon fonctionnement de la fonction qui retourne le premier résultat correspondant,
        lorsque le nom est le paramètre de recherche utilisé."""
        contact_manager = ContactManager()
        # Setup et exécution dans le setter
        contact_manager.contact_list = [Contact("Ducanard", "Valentine"), Contact("Dujambon", "Valentine"),
                                        Contact("Ducanard", "Richard")]
        self.assertEqual(contact_manager.find_first("ducanard").firstname, "Richard")
        self.assertEqual(contact_manager.find_first("dujambon").firstname, "Valentine")
        self.assertEqual(contact_manager.find_first("ducanard valentine").firstname, "Valentine")
        self.assertEqual(contact_manager.find_first("valentine ducanard").firstname, "Valentine")
    def test_find_all_by_names(self):
        """Vérifie le bon fonctionnement de la fonction qui retourne la liste des contacts correspondant,
        lorsque le nom est le paramètre de recherche utilisé."""
        contact_manager = ContactManager()
        # Setup et exécution dans le setter
        contact_manager.contact_list = [Contact("Ducanard", "Valentine"), Contact("Dujambon", "Valentine"),
                                        Contact("Ducanard", "Richard")]
        self.assertEqual(len(contact_manager.find_all("ducanard")), 2)
        self.assertEqual(len(contact_manager.find_all("valentine")), 2)
        self.assertEqual(len(contact_manager.find_all("ducanard valentine")), 1)
        self.assertEqual(len(contact_manager.find_all("valentine ducanard")), 1)
        self.assertEqual(len(contact_manager.find_all("marianne corbel")), 0)

    def test_find_first_by_phone_number(self):
        """Vérifie le bon fonctionnement de la fonction qui retourne le premier résultat correspondant,
        lorsque le téléphone est le paramètre de recherche utilisé."""
        contact_manager = ContactManager()
        contact_manager.contact_list = [Contact("", "Petit Canard", "0102030405"), Contact("", "Grand Canard", "0102030405"),
                                        Contact("", "Madame Ours", email="ours@gmail.com")]
        self.assertEqual(contact_manager.find_first("0102030405", "phone_number").firstname, "Grand Canard")
        self.assertEqual(contact_manager.find_first("0504030201", "phone_number"), None)

    def test_find_all_by_phone_number(self):
        """Vérifie le bon fonctionnement de la fonction qui retourne les contacts correspondant,
        lorsque le nom est le paramètre de recherche utilisé."""
        contact_manager = ContactManager()
        contact_manager.contact_list = [Contact("", "Petit Canard", "0102030405"),
                                        Contact("", "Grand Canard", "0102030405"),
                                        Contact("", "Madame Ours", email="ours@gmail.com")]
        self.assertEqual(len(contact_manager.find_all("0102030405", "phone_number")), 2)
        self.assertEqual(len(contact_manager.find_all("0504030201", "phone_number")), 0)

    def test_find_first_by_email(self):
        """Vérifie le bon fonctionnement de la fonction qui retourne le premier résultat correspondant,
        lorsque l'adresse mail est le paramètre de recherche utilisé."""
        contact_manager = ContactManager()
        contact_manager.contact_list = [Contact("", "Petit Canard", "0102030405"), Contact("", "Grand Canard", "0102030405"),
                                        Contact("", "Madame Ours", email="ours@gmail.com")]
        self.assertEqual(contact_manager.find_first("OURS@gmail.com", "email").firstname, "Madame Ours")
        self.assertEqual(contact_manager.find_first("0504030201", "email"), None)

    def test_find_all_by_email(self):
        """Vérifie le bon fonctionnement de la fonction qui retourne les contacts correspondant,
        lorsque le nom est le paramètre de recherche utilisé."""
        contact_manager = ContactManager()
        contact_manager.contact_list = [Contact("", "Petit Canard", "0102030405", "petitcanard@outlook.com"),
                                        Contact("", "Grand Canard", "0102030405"),
                                        Contact("", "Madame Ours", email="ours@gmail.com")]
        self.assertEqual(len(contact_manager.find_all("OURS@gmail.com", "email")), 1)
        self.assertEqual(len(contact_manager.find_all("0504030201", "email")), 0)

    # --- AFFICHAGE --- #
    def test_affichage_contacts(self):
        print()
        contact_manager = ContactManager()
        contact_manager.contact_list = [Contact("", "Petit Canard", "0102030405", "petitcanard@outlook.com"),
                                        Contact("", "Grand Canard", "0102030405"),
                                        Contact("", "Madame Ours", email="ours@gmail.com")]
        contact_manager.display_contacts()