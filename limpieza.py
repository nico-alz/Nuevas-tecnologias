"""
limpieza.py - Módulo de limpieza y preparación de datos.
Proyecto: Gastos Hormiga

Funciones:
  - estandarizar_texto()   → convierte a minúsculas, quita espacios extra
  - manejar_nulos()        → rellena o elimina valores nulos
  - limpiar_gastos()       → limpieza completa del DataFrame de gastos
  - limpiar_categorias()   → limpieza completa del DataFrame de categorías
"""

import pandas as pd


# ─────────────────────────────────────────────
# 1. ESTANDARIZAR TEXTO
# ─────────────────────────────────────────────

def estandarizar_texto(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Estandariza columnas de texto: quita espacios extra y convierte a minúsculas.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        columnas (list): Lista de nombres de columnas a estandarizar.

    Returns:
        pd.DataFrame: DataFrame con las columnas estandarizadas.
    """
    for col in columnas:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
            # Revertir 'nan' (strings) a NaN real
            df[col] = df[col].replace('nan', pd.NA)
    print(f"   [estandarizar_texto] Columnas estandarizadas: {columnas}")
    return df


# ─────────────────────────────────────────────
# 2. MANEJAR VALORES NULOS
# ─────────────────────────────────────────────

def manejar_nulos(df: pd.DataFrame, rellenos: dict = None, eliminar_si_nulo: list = None) -> pd.DataFrame:
    """
    Maneja valores nulos: rellena con valores por defecto y/o elimina filas críticas.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        rellenos (dict): Diccionario {columna: valor_por_defecto} para rellenar nulos.
        eliminar_si_nulo (list): Lista de columnas; se eliminan filas con nulo en ellas.

    Returns:
        pd.DataFrame: DataFrame sin nulos problemáticos.
    """
    antes = len(df)

    if rellenos:
        for col, valor in rellenos.items():
            if col in df.columns:
                df[col] = df[col].fillna(valor)
        print(f"   [manejar_nulos] Nulos rellenados en: {list(rellenos.keys())}")

    if eliminar_si_nulo:
        df = df.dropna(subset=eliminar_si_nulo)
        eliminadas = antes - len(df)
        print(f"   [manejar_nulos] {eliminadas} fila(s) eliminadas por nulos en: {eliminar_si_nulo}")

    return df


# ─────────────────────────────────────────────
# 3. LIMPIEZA ESPECÍFICA: eliminar montos inválidos
# ─────────────────────────────────────────────

def eliminar_montos_invalidos(df: pd.DataFrame, col_monto: str = 'monto',
                               minimo: float = 0, maximo: float = 50000) -> pd.DataFrame:
    """
    Elimina filas con montos negativos o fuera del rango esperado.
    Limpieza específica del proyecto: un gasto hormiga no puede ser negativo
    ni superar los $50.000 COP.

    Args:
        df (pd.DataFrame): DataFrame de gastos.
        col_monto (str): Nombre de la columna de monto.
        minimo (float): Monto mínimo válido (exclusivo).
        maximo (float): Monto máximo válido (inclusivo).

    Returns:
        pd.DataFrame: DataFrame con montos dentro del rango.
    """
    antes = len(df)
    df = df[(df[col_monto] > minimo) & (df[col_monto] <= maximo)]
    eliminadas = antes - len(df)
    print(f"   [eliminar_montos_invalidos] {eliminadas} fila(s) con monto fuera de rango eliminadas")
    return df


# ─────────────────────────────────────────────
# 4. LIMPIEZA COMPLETA: GASTOS
# ─────────────────────────────────────────────

def limpiar_gastos(df_gastos: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica la pipeline completa de limpieza sobre el DataFrame de gastos.

    Pasos:
      1. Estandarizar texto (descripcion, metodo_pago)
      2. Manejar nulos (rellenar descripcion y metodo_pago; eliminar filas sin monto/fecha/id_categoria)
      3. Eliminar duplicados
      4. Eliminar montos inválidos
      5. Convertir fecha a datetime

    Returns:
        pd.DataFrame: DataFrame de gastos limpio.
    """
    print("\n-- Iniciando limpieza de gastos --")

    # Paso 1: estandarizar texto
    df_gastos = estandarizar_texto(df_gastos, ['descripcion', 'metodo_pago'])

    # Paso 2: manejar nulos
    df_gastos = manejar_nulos(
        df_gastos,
        rellenos={
            'descripcion': 'sin descripcion',
            'metodo_pago': 'desconocido'
        },
        eliminar_si_nulo=['monto', 'fecha', 'id_categoria']
    )

    # Paso 3: eliminar duplicados
    antes = len(df_gastos)
    df_gastos = df_gastos.drop_duplicates()
    print(f"   [drop_duplicates] {antes - len(df_gastos)} fila(s) duplicadas eliminadas")

    # Paso 4: eliminar montos inválidos (limpieza específica del proyecto)
    df_gastos = eliminar_montos_invalidos(df_gastos)

    # Paso 5: convertir fecha
    df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'])
    print("   [to_datetime] Columna 'fecha' convertida a datetime")

    print(f"-- Limpieza finalizada: {len(df_gastos)} registros válidos --\n")
    return df_gastos


# ─────────────────────────────────────────────
# 5. LIMPIEZA COMPLETA: CATEGORIAS
# ─────────────────────────────────────────────

def limpiar_categorias(df_categorias: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica la pipeline de limpieza sobre el DataFrame de categorías.

    Returns:
        pd.DataFrame: DataFrame de categorías limpio.
    """
    print("\n-- Iniciando limpieza de categorias --")

    df_categorias = estandarizar_texto(df_categorias, ['nombre_categoria', 'tipo'])
    df_categorias = manejar_nulos(df_categorias, eliminar_si_nulo=['nombre_categoria', 'tipo'])
    df_categorias = df_categorias.drop_duplicates()

    print(f"-- Limpieza finalizada: {len(df_categorias)} categorias válidas --\n")
    return df_categorias