import pandas as pd

def merge():
    df_gastos = pd.read_csv('data/procesados/gastos_limpio.csv')
    df_categorias = pd.read_csv('data/procesados/categorias_limpio.csv')

    # left join: solo los gastos que tengan categoria registrada
    df_gastos_categorias = df_gastos.merge(df_categorias, on='id_categoria', how='left')

    print(">> Merge realizado exitosamente")
    print(df_gastos_categorias.head())
    return df_gastos_categorias