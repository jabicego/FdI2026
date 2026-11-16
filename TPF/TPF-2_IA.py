import csv

archivo_csv = "datos_climaticos_villa_maria.csv"

# 1. Leer el archivo y detectar dinámicamente el último año registrado
filas = []
with open(archivo_csv, mode="r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        filas.append(fila)

ultimo_año = max(int(fila["año"]) for fila in filas)

# Crear listas con los datos del último año
meses = []
precipitaciones = []

for fila in filas:
    if int(fila["año"]) == ultimo_año:
        meses.append(fila["mes"])
        precipitaciones.append(float(fila["precipitacion_mm"]))

print(f"--- Análisis de Precipitaciones en Villa María ({ultimo_año}) ---")
print("Lista de precipitaciones mensuales (mm):", precipitaciones)

# 2. Calcular precipitación promedio, máxima y mínima
promedio = sum(precipitaciones) / len(precipitaciones)
maxima = max(precipitaciones)
minima = min(precipitaciones)

print(f"\nPrecipitación promedio: {promedio:.2f} mm")
print(f"Precipitación máxima: {maxima} mm")
print(f"Precipitación mínima: {minima} mm")

# 3. Identificar meses con precipitación superior al promedio
print("\nMeses con precipitación superior al promedio:")
for mes, mm in zip(meses, precipitaciones):
    if mm > promedio:
        print(f"- {mes}: {mm} mm")

# 4. Clasificar meses según riesgo de inundación (if / elif / else)
# Umbrales definidos:
#   - Riesgo Bajo: menos de 40 mm
#   - Riesgo Medio: entre 40 mm y 80 mm (inclusive)
#   - Riesgo Alto: más de 80 mm

print("\nClasificación de riesgo de inundación por mes:")
for mes, mm in zip(meses, precipitaciones):
    if mm < 40:
        riesgo = "Bajo"
    elif mm <= 80:
        riesgo = "Medio"
    else:
        riesgo = "Alto"
        
    print(f"- {mes} ({mm} mm): Riesgo {riesgo}")
