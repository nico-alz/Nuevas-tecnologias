import carga
import limpieza
import persistencia
import merge
import analisis

print("========== INICIO DEL PIPELINE ==========\n")

# 1. CARGA
df_gastos = carga.cargar_gastos()
df_categorias = carga.cargar_categorias()

# 2. LIMPIEZA
df_gastos_limpio = limpieza.limpiar_gastos(df_gastos)
df_categorias_limpia = limpieza.limpiar_categorias(df_categorias)

# 3. PERSISTENCIA
persistencia.guardar_gastos_limpios(df_gastos_limpio)
persistencia.guardar_categorias_limpias(df_categorias_limpia)

# 4. MERGE
df_final = merge.merge()

# 5. ANALISIS
analisis.analizar(df_final)

print("========== FIN DEL PIPELINE ==========")