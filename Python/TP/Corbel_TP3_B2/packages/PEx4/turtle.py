from packages.PEx4.reptile import Reptile

class Turtle(Reptile):
    """Classe tortue, héritée d'Animal et de Reptile."""

    # --- CONSTRUCTEUR --- #
    def __init__(self, name: str, age: int, color:str="green"):
        super().__init__(name, "tortue", age, 5, color)
        self.alimentation = "fruits and vegetables"
    # -------------------- #