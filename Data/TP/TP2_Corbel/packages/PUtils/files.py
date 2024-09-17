import pandas as pd

def csv_to_df(filename:str):
    return pd.read_csv("data/"+filename+".csv", encoding='latin-1')