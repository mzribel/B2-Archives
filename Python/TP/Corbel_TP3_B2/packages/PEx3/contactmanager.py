from abc import ABC
from typing import List

from packages.PEx3.contact import Contact
from packages.PUtils.format import sanitize_str_whitespace

class ContactManager:
    # --- CONSTRUCTEUR --- #
    def __init__(self):
        self._contact_list:List[Contact] = []
        self.order_by = "firstname"
    # -------------------- #

    # --- PROPRIETES --- #
    # ORDER BY
    @property
    def order_by(self):
        return self._order_by
    @order_by.setter
    def order_by(self, new_order:str):
        """Ordonne les contacts après avoir redéfini order_by"""
        self._order_by = new_order
        self.sort_contacts()

    # CONTACT_LIST
    @property
    def contact_list(self):
        return self._contact_list
    @contact_list.setter
    def contact_list(self, new_contact_list:List[Contact]):
        """Ordonne la liste de contact avant de réassigner self.contact_list"""
        self._contact_list = ContactManager.sorted_contacts(new_contact_list, self.order_by)
    # ----------------- #

    # --- METHODES --- #
    def add_contact(self, new_contact:Contact):
        self.contact_list.append(new_contact)
    def remove_contact(self, contact:Contact):
        try:
            self.contact_list.remove(contact)
        except ValueError: pass
        # Passe l'erreur not found sous silence dans la mesure où elle n'apporte rien.

    # --- METHODES DE RECHERCHE --- #
    @staticmethod
    def search_comparison_func(contact: Contact, needle: str, by: str = "name") -> bool:
        """Fonction faisant la comparaison entre un contact recherché et un contact de la liste.
        Utilisée dans find_first et find_all."""
        match by:
            # Recherche par numéro de téléphone, email ou nom/prénom.
            case "phone_number" | "email":
                if needle == getattr(contact, by).lower(): return True
            case _:
                c_firstname = contact.firstname.lower()
                c_lastname = contact.lastname.lower()
                if needle == c_firstname or needle == c_lastname or \
                        needle == f"{c_firstname} {c_lastname}" or needle == f"{c_lastname} {c_firstname}":
                    # Compare le nom donné à toutes les variations possibles du nom d'un contact:
                    # "marianne", "corbel", "marianne corbel" et "corbel marianne' par exemple..
                    return True
        return False

    def find_first(self, needle: str, by: str = "name") -> Contact | None:
        """Retourne le premier contact correspondant aux critères de recherche."""
        needle = sanitize_str_whitespace(needle).lower()
        if needle == "": return None

        for contact in self.contact_list:
            if ContactManager.search_comparison_func(contact, needle, by): return contact
        return None

    def find_all(self, needle: str, by: str = "name") -> List[Contact]:
        """Retourne tous les contacts correspondant aux critères de recherche."""
        result: List[Contact] = []
        needle = sanitize_str_whitespace(needle).lower()
        if needle == "": return result

        for contact in self.contact_list:
            if ContactManager.search_comparison_func(contact, needle, by): result.append(contact)
        return result

    # --- METHODES DE TRI --- #
    @staticmethod
    def sorted_contacts(contact_list:List[Contact], by:str|None=""):
        """Retourne une copie triée de l'array sans le remplacer."""
        return sorted(contact_list, key=lambda contact:
            ((contact.firstname, contact.lastname) if by == "firstname"
            else (contact.lastname, contact.firstname)))

    def sort_contacts(self):
        """Remplace contact_list dans l'instance de ContactManager par la liste triée."""
        self._contact_list = ContactManager.sorted_contacts(self.contact_list, self.order_by)

    # --- DISPLAY --- #
    def display_contacts(self):
        if not self._contact_list:
            print("(le répertoire est vide)")
            return
        for contact in self.contact_list:
            print(contact)
