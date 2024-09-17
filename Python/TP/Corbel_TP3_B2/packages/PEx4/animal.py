from abc import ABC, abstractmethod

class Animal(ABC):
    """Classe abstraite Animal."""

    # --- CONSTRUCTEUR --- #
    def __init__(self, name: str, species: str, age: int, has_vertebrae:bool=True, is_cold_blooded:bool=False, alimentation:str=""):
        self.alimentation = alimentation
        self.name: str = name.title()
        self.species: str = species.title()
        self.age: int = age
        self.has_vertebrae = has_vertebrae
        self.is_cold_blooded = is_cold_blooded
        self.alimentation = alimentation
    # -------------------- #

    # --- METHODES --- #
    @abstractmethod
    def make_sound(self):
        """Méthode abstraite: la classe est trop vague pour savoir le type de bruit
        que peut faire l'animal."""
        pass

    def sleep(self)->str:
        return f"{self.name} is sleeping..."

    def move(self):
        return f"{self.name} is moving..."

    def eat(self):
        return f"{self.name} is eating" + ("..." if self.alimentation == "" else f" {self.alimentation}...")