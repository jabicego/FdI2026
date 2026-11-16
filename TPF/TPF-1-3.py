import csv                                                             
import os                                                              
                                                                       
                                                                       
archivo_csv = "calles_pavimentacion.csv"                   
print(os.path.exists(archivo_csv))                                     
data = open(archivo_csv, mode="r", encoding="utf-8")      

filas = []                                                             
with data as archivo:                                                  
    lector = csv.reader(archivo)                                       
    encabezados = next(lector)  # Leer la primera fila como encabezados
                                                          
    for fila in lector:                                                
        filas.append(fila)    

dicc_calles={}

for fila in filas:
    calle = fila[0]
    pavimentacion = fila[1]
    dicc_calles[calle] = pavimentacion

print(dicc_calles)


superficie_total = 0

for fila in filas:
    longitud = fila[1]
    ancho = fila[2]
    superficie = float(longitud) * float(ancho)
    superficie_total += superficie

print("La superficie total de pavimentación es:", superficie_total) 

ESPESOR_M = 0.05  # 5 cm en metros

volumen_asfalto = superficie_total * ESPESOR_M

print("La superficie total de pavimentación es:", superficie_total, "m²")
print("El asfalto necesario es:", round(volumen_asfalto, 2), "m³")