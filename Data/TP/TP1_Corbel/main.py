import warnings
from packages.PGUI.TPMenu import TPMenu

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
    TP = TPMenu(title="B2 DATA TP1 - Marianne C.")
    TP.root.mainloop()