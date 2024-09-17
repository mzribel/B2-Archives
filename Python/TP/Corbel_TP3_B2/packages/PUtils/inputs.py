import re

from packages.PUtils.format import sanitize_str_whitespace

# Demande une entrée numérique à l'utilisateur en gérant les erreurs de type ou de limite.
# Répète la demande tant que l'input ne correspond pas au format demandé.
def getNumericalInput(message:str, isInt:bool=False, minLimit:None|int|float=None, maxLimit:None|int|float=None):
    # Lève une erreur si `minLimit` est supérieur à `maxLimit`
    if minLimit is not None and maxLimit is not None and minLimit > maxLimit:
        raise ValueError("La limite minimum ne peut pas être supérieure à la limite maximum")
    while True:
        try:
            # Récupère l'entrée utilisateur et convertit au type numérique attendu
            userInput = int(input(message)) if isInt else float(input(message))
        except ValueError:
            # Lève une erreur si la conversion a échoué (valeur non numérique ou nombre décimal pour un int)
            print("ERREUR: On ne veut que des chiffres entiers!\n") if isInt \
                else print("ERREUR: Un nombre est attendu !\n")
        except KeyboardInterrupt:
            exit(1)
        else:
            # Applique les limites min et/ou max si elles ont été définies
            if (minLimit is not None and minLimit > userInput) or \
                    (maxLimit is not None and maxLimit < userInput):
                intervalStr = f"[{minLimit if minLimit is not None else str()}:{maxLimit if maxLimit is not None else str()}]"
                print(f"ERREUR: Nombre hors de l'interval autorisé ! {intervalStr}\n")
                continue
            # Retourne la valeur valide
            return userInput

def get_str_input(message:str, regex:str|None=None, accepts_empty=True,
                  regex_err:str="ERREUR: La chaîne de caractères entrée ne correspond pas au schéma attendu."):
    while True:
        try:
            userInput = sanitize_str_whitespace(input(message))
        except KeyboardInterrupt:
            exit(1)
        if userInput == "" and not accepts_empty:
            print("ERREUR: Il faut entrer une valeur non nulle !\n")
            continue
        if regex:
            regex = re.compile(regex)
            if not regex.match(userInput):
                print(regex_err, "\n")
                continue
        return userInput