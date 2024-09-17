import unittest
from unittest.mock import patch

from packages.PEx4.tiger import Tiger
from packages.PEx4.turtle import Turtle
from tests.customtestclass import CustomTestClass
from packages.PEx4.animal import Animal

class Tests_Abstract_Animal(CustomTestClass):
    """Réalise les tests relatifs à la classe Animal, de l'exercice 4 du TP3."""

    # --- ATTRIBUTS --- #
    @patch.multiple(Animal, __abstractmethods__=set())
    def test_animal_attributes(self):
        """Affiche les attributs propres à la classe Animal."""
        animal = Animal("Tigrou", "tigre", 5)
        d = {k: getattr(animal, k, '') for k in animal.__dir__() if
             k[:2] != '__' and not "abc" in k and type(getattr(animal, k, '')).__name__ != 'method'}
        if d:
            print("\n   -> Attributs de la classe:")
            for k in d.keys():
                print(f"\t - {k}")

    # --- METHODES --- #
    @patch.multiple(Animal, __abstractmethods__=set())
    def test_animal_make_sound(self):
        print("\n   -> (méthode abstraite: pas implémentée!) ", end="")

    @patch.multiple(Animal, __abstractmethods__=set())
    def test_animal_sleep(self):
        animal = Animal("Tigrou", "tigre", 5)
        print("\n   -> " + animal.sleep() + " ", end="")

    @patch.multiple(Animal, __abstractmethods__=set())
    def test_animal_move(self):
        animal = Animal("Tigrou", "tigre", 5)
        print("\n   -> " + animal.move() + " ", end="")
    @patch.multiple(Animal, __abstractmethods__=set())
    def test_animal_eat(self):
        animal = Animal("Tigrou", "tigre", 5)
        print("\n   -> " + animal.eat() + " ", end="")

class Tests_Turtle(CustomTestClass):
    """Réalise les tests relatifs à la classe Turtle, de l'exercice 4 du TP4."""
    turtle = Turtle("Franklin", 10, "green")

    # --- AFFICHAGE --- #
    def test_turtle_attributes(self):
        """Affiche les attributs propres à la classe Turtle."""
        animal = Tests_Turtle.turtle
        d = {k: getattr(animal, k, '') for k in animal.__dir__() if
             k[:2] != '__' and not "abc" in k and type(getattr(animal, k, '')).__name__ != 'method'}
        if d:
            print("\n   -> Attributs d'une instance de la classe':")
            for k, v in d.items():
                print(f"\t - {k}: {v}")

    # --- METHODES --- #
    def test_turtle_sleep(self):
        print("\n   -> " + Tests_Turtle.turtle.sleep() + " ", end="")

    def test_turtle_move(self):
        print("\n   -> " + Tests_Turtle.turtle.move() + " ", end="")

    def test_turtle_eat(self):
        print("\n   -> " + Tests_Turtle.turtle.eat() + " ", end="")

    def test_turtle_make_sound(self):
        print("\n   -> " + Tests_Turtle.turtle.make_sound() + " ", end="")

    def test_turtle_lay_eggs(self):
        print("\n   -> " + Tests_Turtle.turtle.lay_eggs() + " ", end="")



class Tests_Tiger(CustomTestClass):
    """Réalise les tests relatifs à la classe Tiger, de l'exercice 4 du TP4."""
    tiger = Tiger("Sherkan", 10, "orange")

    # --- AFFICHAGE --- #
    def test_tiger_attributes(self):
        """Affiche les attributs propres à la classe Tiger."""
        animal = Tests_Tiger.tiger
        d = {k: getattr(animal, k, '') for k in animal.__dir__() if
             k[:2] != '__' and not "abc" in k and type(getattr(animal, k, '')).__name__ != 'method'}
        if d:
            print("\n   -> Attributs d'une instance de la classe':")
            for k, v in d.items():
                print(f"\t - {k}: {v}")

    # --- METHODES --- #
    def test_tiger_sleep(self):
        print("\n   -> " + Tests_Tiger.tiger.sleep() + " ", end="")

    def test_tiger_move(self):
        print("\n   -> " + Tests_Tiger.tiger.move() + " ", end="")

    def test_tiger_eat(self):
        print("\n   -> " + Tests_Tiger.tiger.eat() + " ", end="")

    def test_tiger_make_sound(self):
        print("\n   -> " + Tests_Tiger.tiger.make_sound() + " ", end="")

    def test_tiger_breastfeed(self):
        print("\n   -> " + Tests_Tiger.tiger.breastfeed() + " ", end="")
    def test_tiger_give_birth(self):
        print("\n   -> " + Tests_Tiger.tiger.give_birth() + " ", end="")
    def test_tiger_hunt(self):
        print("\n   -> " + Tests_Tiger.tiger.hunt() + " ", end="")

if __name__ == '__main__':
    unittest.main(verbosity=2)