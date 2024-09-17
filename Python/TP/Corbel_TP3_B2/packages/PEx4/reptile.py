from packages.PEx4.animal import Animal

class Reptile(Animal):
    """Classe Reptile, héritée d'Animal."""

    # --- CONSTRUCTEUR --- #
    def __init__(self, name: str, species: str, age: int, avg_egg_count, scale_color):
        super().__init__(name, species, age, is_cold_blooded=True)

        # Attributs propres aux reptiles.
        self.avg_egg_size = avg_egg_count
        self.scale_color = scale_color
    # -------------------- #

    # --- METHODES --- #

    def make_sound(self):
        """Surcharge la méthode make_sound de Animal.
        Le sifflement est un trait relativement commun chez les reptiles."""
        return f"{self.name} is hissing !"

    def move(self):
        """Surcharge la méthode move de Animal.
        Le fait de ramper est un point propre aux reptiles."""
        return f"{self.name} is crawling..."

    def lay_eggs(self):
        """Méthode propre de Reptile.
        Représente le fait de pondre des oeufs."""
        return f"{self.name} is laying eggs..."