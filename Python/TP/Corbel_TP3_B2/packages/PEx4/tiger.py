from packages.PEx4.mammal import Mammal

class Tiger(Mammal):
    """Classe Tigre, dérivée d'Animal et de Mammal."""

    # --- CONSTRUCTEUR --- #
    def __init__(self, name: str, age: int, fur:str="orange"):
        super().__init__(name, "tiger", age, 3, fur)
        self.alimentation = "meat"
    # -------------------- #

    # --- METHODES --- #
    def move(self):
        """Surcharge la méthode move de Animal."""
        return f"{self.name} is moving on its legs..."

    def make_sound(self):
        """Surcharge la méthode make_sound de Animal."""
        return f"{self.name} is roaring !"

    def hunt(self):
        """Méthode propre à la classe Tiger."""
        return f"{self.name} is looking for something to eat !"