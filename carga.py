import pandas as pd

def cargar_gastos():
    df_gastos = pd.read_csv('data/row/gastos.csv')
    print(">> Carga de gastos exitosa")
    df_gastos.info()
    return df_gastos

def cargar_categorias():
    df_categorias = pd.read_csv('data/row/categorias.csv')
    print(">> Carga de categorias exitosa")
    df_categorias.info()
    return df_categorias