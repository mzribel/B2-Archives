# Crée une textBox de 3x`width` contenant du texte `content`.
# Si `title` n'est pas vide, rajoute `title` en haut à gauche de la textBox, sur la ligne haute.

from packages.PUtils.format import sanitize_str_whitespace
class TitleBox:
    def __init__(self, content, title="", width=48, height=3):
        self.title = title.strip()
        self.content = " ".join([*sanitize_str_whitespace(content).upper()])
        self.height = height
        self.width = width

    # Dessine la textBox.
    def draw(self, sep="\n"):
        # Ajoute deux espaces de padding autour de `title` pour la lisibilité.
        if len(self.title) != 0:
            self.title = f" {self.title} "
        # Ne fonctionne pas si la textBox n'a pas de `content`.
        if len(self.content) == 0:
            return

        # Print la textBox et son contenu:
        print(f"┌{self.title.ljust(self.width, '─')}┐")
        print(f"|{self.content.center(self.width)}|")
        print(f"└{'─'*self.width}┘"+sep)