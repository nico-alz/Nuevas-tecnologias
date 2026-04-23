def guardar_gastos_limpios(df_gastos):
    df_gastos.to_csv('data/procesados/gastos_limpio.csv', index=False)
    print(">> Gastos limpios guardados en data/procesados/gastos_limpio.csv")

def guardar_categorias_limpias(df_categorias):
    df_categorias.to_csv('data/procesados/categorias_limpio.csv', index=False)
    print(">> Categorias limpias guardadas en data/procesados/categorias_limpio.csv")