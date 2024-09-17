import re
from datetime import datetime

def sanitize_str_whitespace(string:str)->str:
    """Retire les espaces au début et à la fin de la string,
    ainsi que les doublons d'espaces au milieu de la string."""
    return re.sub("\s+", " ", string.strip())

def date_to_string(date:datetime|None):
    if date is None: return ""
    return date.strftime("%d/%m/%Y")