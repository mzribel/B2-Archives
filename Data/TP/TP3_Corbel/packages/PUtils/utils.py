from difflib import SequenceMatcher

import pandas as pd
import os, sys

# Fonction "raccourcie" pour sauter les lignes (plus esthétiques que des `print` vides).
# `number` représente le nombre de lignes à sauter.
def jump_lines(number=1):
    """Saute un nombre de lignes donné en paramètre."""
    # Check la validité du nombre fourni.
    if number < 0:
        return
    print("\n"*number, sep='', end='', flush=True)

def get_correct_name_in_list(name:str, list_names:[], minimum_ratio=0.85):
    correct_name = None
    ratio = -1
    if len(name) == 0:
        return None

    if len(list_names) == 0 or name in list_names:
        return name

    for n in list_names:
        r = SequenceMatcher(None, n.lower() ,name.lower()).ratio()
        if r < minimum_ratio or r < ratio:
            continue
        correct_name = n
        ratio = r

    return correct_name if correct_name is not None else None

def read_csv(filename:str):
    return pd.read_csv("data/" + filename, encoding='utf-8-sig')


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout