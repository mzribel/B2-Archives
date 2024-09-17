from abc import ABC
from enum import Enum

import numpy as np
import re

import pandas as pd

from packages.PUtils.utils import get_correct_name_in_list


class DataType(Enum):
    STRING = 0
    INTEGER = 1
    FLOAT = 2

class DataColumn(ABC):
    def __init__(self, name: str, name_in_file: str, dtype: DataType, null_or_empty: bool):
        if name is None or name == "":
            raise ValueError("Le nom de la colonne `name` ne peut pas être vide")
        self.name = name
        self.name_in_file = name_in_file if name_in_file is None or name_in_file == "" else self.name
        self.dtype = dtype
        self.null_or_empty = null_or_empty

    def normalize(self, value):
        pass

    def print(self):
        pass

class DataColumnString(DataColumn):
    def __init__(self, name: str, name_in_file: str, null_or_empty: bool = True, spell_check=None):
        super().__init__(name, name_in_file, DataType.STRING, null_or_empty)
        self.spell_check = [] if spell_check is None else spell_check

    def get_corrected_value(self, value, minimum_ratio):
        return get_correct_name_in_list(value, self.spell_check, minimum_ratio)

    def normalize(self, value, minimum_ratio=.85):
        if self.null_or_empty and (value == np.NaN or value == ""):
            return np.Nan
        if len(self.spell_check) == 0 or value in self.spell_check: return value
        try:
            return self.get_corrected_value(value, minimum_ratio)
        except ValueError:
            return None

    def print(self, print_list: bool = True):
        print(f"--- COLONNE ---")
        print(f"Nom: {self.name} ({self.name_in_file} dans le csv)")
        print(f"Type: {self.dtype}")
        print(f"Nullable: {self.null_or_empty}")
        if not print_list:
            print(f"Spell check list: {len(self.spell_check)} elements")
        else:
            print(f"Spell check list ({len(self.spell_check)} elements):")
            for element in self.spell_check:
                print(f"   - {element}")

class DataColumnNumber(DataColumn):
    def __init__(self, name: str, name_in_file: str, is_int: bool = False, null_or_empty: bool = True,
                 min_value: float | int | None = None, max_value: float | int | None = None,
                 limit_to_extremes: bool = False):
        dtype = DataType.INTEGER if is_int else DataType.FLOAT
        super().__init__(name, name_in_file, dtype, null_or_empty)
        self.min_value = min_value
        self.max_value = max_value
        self.limit_to_extremes = limit_to_extremes

    def normalize(self, value):

        if self.null_or_empty and str(value) == "nan":
            return np.NaN
        try:
            normalized = re.sub(r',', '.', str(value))
            normalized = re.sub(r'[^\d\.\-]|', '', normalized)

            normalized = float(normalized) if self.dtype == DataType.FLOAT else int(float(normalized))
            if self.min_value is not None and normalized < self.min_value:
                if self.limit_to_extremes:
                    return int(self.min_value) if DataType.INTEGER else float(self.min_value)
                return None
            if self.max_value is not None and normalized > self.max_value:
                if self.limit_to_extremes:
                    return int(self.max_value) if DataType.INTEGER else float(self.max_value)
                return None
        except ValueError:
            return None if not self.null_or_empty else np.NaN

        return normalized

    def print(self):
        print(f"--- COLONNE ---")
        print(f"Nom: {self.name} ({self.name_in_file} dans le csv)")
        print(f"Type: {self.dtype}")
        print(f"Nullable: {self.null_or_empty}")
        if self.min_value is not None or self.max_value is not None:
            print(f"Range: [{self.min_value} - {self.max_value}]")