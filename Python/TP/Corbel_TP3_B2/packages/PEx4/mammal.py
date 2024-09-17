from packages.PEx4.animal import Animal

class Mammal(Animal):
    """Classe Mammal, dérivée de la classe Animal."""

    # --- CONSTRUCTEUR --- #
    def __init__(self, name: str, species: str, age: int, avg_litter_count, fur_color, alimentation=""):
        super().__init__(name, species, age, alimentation=alimentation)

        # Attributs propres aux mammifères.
        self.avg_litter_size = avg_litter_count
        self.fur_color = fur_color
    # -------------------- #

    # --- METHODES --- #
    def make_sound(self):
        """Surcharge la méthode make_sound de Animal."""
        return f"{self.name} is making noise !"

    def breastfeed(self):
        """Méthode propre à Mammal.
        Représente l'allaitement, propre aux mammifères."""
        return f"{self.name} is breastfeeding..."

    def give_birth(self):
        """Méthode propre à Mammal.
        Représente la mise bas pour un animal vivipare.."""
        return f"{self.name} is giving birth..."