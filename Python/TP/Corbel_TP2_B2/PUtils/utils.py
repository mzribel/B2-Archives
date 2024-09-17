# Fonction "raccourcie" pour sauter les lignes (plus esthétiques que des `print` vides).
# `number` représente le nombre de lignes à sauter.
from random import randrange
from decimal import Decimal
from typing import List

import numpy
import numpy as np
import re

def jump_lines(number=1):
    """Saute un nombre de lignes donné en paramètre."""
    # Check la validité du nombre fourni.
    if number < 0:
        return
    print("\n"*number, sep='', end='', flush=True)

