def analizar(df):
    print("\n========== ANALISIS DE GASTOS HORMIGA ==========\n")

    print("1. ANALISIS DE FRECUENCIA")
    print("   ¿Cuál es el gasto que más se repite en los registros?")
    frecuencia = df['descripcion'].value_counts()
    gasto_frecuente = frecuencia.idxmax()
    veces = frecuencia.max()
    print(frecuencia.head(5).to_string())
    print(f"\n   >> El gasto más frecuente es: '{gasto_frecuente}' con {veces} registros.\n")

    print("2. ANALISIS DE AGREGACION")
    print("   ¿Cuánto se gastó en total por cada categoría?")
    gasto_por_categoria = (
        df.groupby('nombre_categoria')['monto']
        .sum()
        .sort_values(ascending=False)
    )
    print(gasto_por_categoria.to_string())
    categoria_mayor = gasto_por_categoria.idxmax()
    total_mayor = gasto_por_categoria.max()
    print(f"\n   >> La categoría con mayor gasto es: '{categoria_mayor}' con ${total_mayor:,.0f} COP.\n")

    print("3. FILTRADO Y CONTEO")
    print("   ¿Cuántos gastos se realizaron en efectivo?")
    gastos_efectivo = df[df['metodo_pago'] == 'efectivo']
    conteo = len(gastos_efectivo)
    total_efectivo = gastos_efectivo['monto'].sum()
    print(f"\n   >> Total de gastos en efectivo: {conteo} registros.")
    print(f"   >> Monto acumulado en efectivo: ${total_efectivo:,.0f} COP.\n")

    print("4. EXTRAS")
    df = df.copy()
    df['mes'] = df['fecha'].astype(str).str[:7]
    gasto_por_mes = df.groupby('mes')['monto'].sum().sort_values(ascending=False)
    print(f"   >> Mes con mayor gasto: {gasto_por_mes.idxmax()} (${gasto_por_mes.max():,.0f} COP)")
    metodo_top = df['metodo_pago'].value_counts().idxmax()
    print(f"   >> Método de pago más usado: {metodo_top}")
    total = df['monto'].sum()
    print(f"   >> Gasto total registrado: ${total:,.0f} COP")

    print("\n=================================================\n")