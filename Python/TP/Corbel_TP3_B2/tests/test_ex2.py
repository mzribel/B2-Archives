import datetime
import unittest

from packages.PEx2.person import Person
from tests import customtestclass
from dateutil.relativedelta import relativedelta


class Tests_Person(customtestclass.CustomTestClass):
    """Réalise les tests relatifs à la classe Person, de l'exercice 2 du TP3."""

    # --- INITIALISATION --- #
    def test_person_init_raises_when_names_empty(self):
        """Lance une erreur si le nom ET le prénom sont vides ou nuls."""
        self.assertRaises(ValueError, Person, "", "")
    def test_person_init_raises_when_invalid_DoB(self):
        """Lance une erreur si le programme ne parvient pas à convertir la date
        dd/mm/yyyy sous format datetime."""
        self.assertRaises(ValueError, Person, "Jean", "Ducanard", "invalide")
    def test_person_init_valid_age_when_valid_DoB(self):
        """Vérifie le bon fonctionnement de la déduction de l'âge par rapport à la dob"""
        fictive_DoB = datetime.datetime(2000, 1, 1) # date de naissance dynamique pour éviter une erreur future.
        age_from_DoB = relativedelta(datetime.datetime.now(), fictive_DoB).years # calcul de l'âge
        p = Person("Jean", "Ducanard", fictive_DoB.strftime("%d/%m/%Y")) # création de la personne fictive
        self.assertEqual(age_from_DoB, p.age)
    def test_person_init_valid_when_valid_age_param(self):
        """Initialisation avec un age valide"""
        p = Person("Jean", "Ducanard", age=12) # création de la personne fictive
        self.assertEqual(12, p.age)
    def test_person_init_raises_when_invalid_age_str(self):
        """Lance une erreur si un age impossible est fourni."""
        self.assertRaises(ValueError, Person, "Jean", "Ducanard", "", -1)
    def test_person_init_raises_when_invalid_age(self):
        """Lance une erreur si une date de naissance impliquant un âge impossible
        est fournie."""
        self.assertRaises(ValueError, Person, "Jean", "Ducanard", "10/10/1800", -1)
    def test_person_init_valid_age_str(self):
        """Vérifie le bon fonctionnement de la convertion date string -> datetime"""
        person = Person("Ducanard", "Jean", "01/01/2000")
        self.assertEqual(person.dob, datetime.datetime(2000, 1, 1))
    def test_person_init_valid_params(self):
        """Initialisation avec des paramètres tous valides."""
        person = Person("Ducanard", "Jean", age=21)
        self.assertEqual(person.firstname, "Jean")
        self.assertEqual(person.lastname, "DUCANARD")
        self.assertEqual(person.age, 21)
    # ------------------- #

if __name__ == '__main__':
    unittest.main()

