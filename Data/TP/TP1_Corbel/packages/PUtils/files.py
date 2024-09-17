import pandas as pd

def csv_to_df(filename:str="timbres"):
    file = pd.read_csv("data/"+filename+".csv", encoding='latin-1')
    file[["Valeur faciale", "Valeur marchande"]] = file[["Valeur faciale", "Valeur marchande"]].apply(pd.to_numeric, errors="coerce")
    return file