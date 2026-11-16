import csv                                                             
import os                                                              
                                                                       
                                                                       
archivo_csv = "datos_climaticos_villa_maria.csv"                   
print(os.path.exists(archivo_csv))                                     
data = open(archivo_csv, mode="r", encoding="utf-8")                   
                                                                       
                                                                       
                                                                       
                                                                       
# 1. Leer el archivo y detectar dinámicamente el último año registrado 
filas = []                                                             
with data as archivo:                                                  
    lector = csv.reader(archivo)                                       
    encabezados = next(lector)  # Leer la primera fila como encabezados
                                                          
    for fila in lector:                                                
        filas.append(fila)                                            
                                                                       
                                                                       
                                                                       
                                                                       
                                                                       
ultimo_año = max(int(fila[1]) for fila in filas)                       
                                                                       
                                                                       
# Crear listas con los datos del último año                            
                                                                       
                                                                       
meses = []
precipitaciones = []

for fila in filas:
    if int(fila[1]) == ultimo_año:
        meses.append(fila[0])
        precipitaciones.append(float(fila[2]))

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
for i in range(len(precipitaciones)):
    if precipitaciones[i] > promedio:
        print(f"{meses[i]}: {precipitaciones[i]} mm")

# 4. Clasificar meses según riesgo de inundación (if / elif / else)
# Umbrales definidos:
#   - Riesgo Bajo: menos de 40 mm
#   - Riesgo Medio: entre 40 mm y 80 mm (inclusive)
#   - Riesgo Alto: más de 80 mm

print("\nClasificación de riesgo de inundación por mes:")
for i in range(len(precipitaciones)):
    if precipitaciones[i] < 40:
        riesgo = "Bajo"
    elif precipitaciones[i] <= 80:
        riesgo = "Medio"
    else:
        riesgo = "Alto"
    print(f"{meses[i]}: {precipitaciones[i]} mm - Riesgo: {riesgo}")