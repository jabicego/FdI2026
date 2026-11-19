import pandas as pd

# =====================================================
# PARTE 1: CÁLCULOS BÁSICOS DE INGENIERÍA
# =====================================================

# ---------- 1. Cálculo de materiales del puente ----------
print("--- 1. Cálculo de materiales del puente ---")

# Se piden las dimensiones al usuario con input
largo = float(input("Ingrese el largo del puente (m): "))
ancho = float(input("Ingrese el ancho del puente (m): "))
espesor_losa = float(input("Ingrese el espesor de la losa (m): "))
cant_pilares = int(input("Ingrese la cantidad de pilares: "))
largo_pilar = float(input("Ingrese el largo de la sección del pilar (m): "))
ancho_pilar = float(input("Ingrese el ancho de la sección del pilar (m): "))
alto_pilar = float(input("Ingrese la altura del pilar (m): "))

# Volumen de hormigón (losa + pilares)
vol_losa = largo * ancho * espesor_losa
vol_pilares = largo_pilar * ancho_pilar * alto_pilar * cant_pilares
vol_total = vol_losa + vol_pilares

# Acero de refuerzo: 150 kg por m3 de hormigón
kg_acero = vol_total * 150

# Costo estimado: hormigón $85.000/m3, acero $1.200/kg
costo_hormigon = vol_total * 85000
costo_acero = kg_acero * 1200
costo_total = costo_hormigon + costo_acero

print(f"Volumen de hormigón: {vol_total:.2f} m3")
print(f"Acero de refuerzo: {kg_acero:.2f} kg")
print(f"Costo hormigón: ${costo_hormigon:,.2f}")
print(f"Costo acero: ${costo_acero:,.2f}")
print(f"Costo total estimado: ${costo_total:,.2f}")


# ---------- 2. Análisis de precipitaciones ----------
print("\n--- 2. Análisis de precipitaciones ---")


df_clima = pd.read_csv(r"C:\Users\Usuario\Downloads\datos_climaticos_villa_maria.csv")

# Último año = últimos 12 meses del archivo
ultimos_12 = df_clima.tail(12)

# Lista con la precipitación mensual del último año
lista_precip = list(ultimos_12["precipitacion_mm"])
lista_meses = list(ultimos_12["mes"])

# Promedio, máxima y mínima
promedio = sum(lista_precip) / len(lista_precip)
maxima = max(lista_precip)
minima = min(lista_precip)

print(f"Precipitación promedio: {promedio:.2f} mm")
print(f"Precipitación máxima: {maxima} mm")
print(f"Precipitación mínima: {minima} mm")

# Meses con precipitación superior al promedio
print("\nMeses con precipitación superior al promedio:")
for i in range(len(lista_meses)):
    if lista_precip[i] > promedio:
        print(f" - {lista_meses[i]}: {lista_precip[i]} mm")

# Clasificación según riesgo de inundación (umbrales: 50 y 100 mm)
print("\nRiesgo de inundación por mes:")
for i in range(len(lista_meses)):
    p = lista_precip[i]
    if p > 100:
        riesgo = "ALTO"
    elif p >= 50:
        riesgo = "MEDIO"
    else:
        riesgo = "BAJO"
    print(f" - {lista_meses[i]}: {p} mm -> Riesgo {riesgo}")


# ---------- 3. Planificación de pavimentación ----------
print("\n--- 3. Planificación de pavimentación ---")

df_calles = pd.read_csv(r"C:\Users\Usuario\Downloads\calles_pavimentacion.csv")

# Diccionario con calles y sus longitudes
dic_calles = dict(zip(df_calles["nombre_calle"], df_calles["longitud_metros"]))
print("Calles a pavimentar:", dic_calles)

# Superficie total = suma de (longitud x ancho) de cada calle
superficie_total = (df_calles["longitud_metros"] * df_calles["ancho_metros"]).sum()

# Asfalto necesario con espesor de 5 cm (0.05 m)
volumen_asfalto = superficie_total * 0.05

print(f"Superficie total a pavimentar: {superficie_total:,.2f} m2")
print(f"Asfalto necesario: {volumen_asfalto:,.2f} m3")


# =====================================================
# PARTE 2: SISTEMA DE GESTIÓN DE PROYECTOS
# =====================================================

# ---------- 1. Función de cálculo estructural ----------
print("\n--- 1. Dimensionado de zapata ---")

df_suelos = pd.read_csv(r"C:\Users\Usuario\Downloads\ensayos_suelo.csv")


def dimensionar_zapata(carga_columna, punto_muestreo, profundidad_deseada, forma, relacion_lados):
    # Buscar el ensayo del punto y profundidad indicados
    fila = df_suelos[(df_suelos["punto_muestreo"] == punto_muestreo) &
                     (df_suelos["profundidad_m"] == profundidad_deseada)]
    tipo_suelo = fila["tipo_suelo"].values[0]
    resistencia = fila["resistencia_kpa"].values[0]

    # Tensión admisible con factor de seguridad 3
    tension_adm = resistencia / 3

    # Área necesaria = carga / tensión admisible  (kN / kPa = m2)
    area = carga_columna / tension_adm

    # Lados de la zapata: L = relacion * B  ->  A = relacion * B^2
    if forma == "cuadrada":
        relacion_lados = 1.0
    ancho_b = (area / relacion_lados) ** 0.5
    largo_l = relacion_lados * ancho_b

    print(f"Punto {punto_muestreo} a {profundidad_deseada} m - Suelo: {tipo_suelo}")
    print(f"Resistencia: {resistencia} kPa | Tensión admisible: {tension_adm:.2f} kPa")
    print(f"Área necesaria: {area:.2f} m2")
    print(f"Zapata {forma}: {ancho_b:.2f} m x {largo_l:.2f} m")
    return area, ancho_b, largo_l


# Ejemplos de uso
dimensionar_zapata(450, "P1", 3.0, "cuadrada", 1.0)
dimensionar_zapata(450, "P1", 3.0, "rectangular", 1.5)


# ---------- 2. Gestión de archivos de proyecto ----------
print("\n--- 2. Gestión de archivos de proyecto ---")

# Ingresar punto y resistencia -> profundidad mínima para alcanzarla
punto = input("Ingrese el punto de muestreo (P1 a P7): ")
resistencia_buscada = float(input("Ingrese la resistencia requerida (kPa): "))

ensayos_punto = df_suelos[df_suelos["punto_muestreo"] == punto]
cumplen = ensayos_punto[ensayos_punto["resistencia_kpa"] >= resistencia_buscada]
prof_minima = cumplen["profundidad_m"].min()
print(f"Profundidad mínima en {punto} para {resistencia_buscada} kPa: {prof_minima} m")

# Humedad promedio por punto de muestreo
humedad_prom = df_suelos.groupby("punto_muestreo")["humedad_porcentaje"].mean()
print("\nHumedad promedio por punto:")
print(humedad_prom)

# Guardar resultados en archivo de texto con formato de informe
with open("informe_suelos.txt", "w", encoding="utf-8") as archivo:
    archivo.write("========== INFORME DE ENSAYOS DE SUELO ==========\n\n")
    archivo.write("Profundidad mínima para la resistencia requerida:\n")
    archivo.write(f"  Punto: {punto}\n")
    archivo.write(f"  Resistencia requerida: {resistencia_buscada} kPa\n")
    archivo.write(f"  Profundidad mínima: {prof_minima} m\n\n")
    archivo.write("Humedad promedio por punto de muestreo:\n")
    for p, h in humedad_prom.items():
        archivo.write(f"  {p}: {h:.2f} %\n")

print("Resultados guardados en informe_suelos.txt")


# ---------- 3. Sistema de control de calidad ----------
print("\n--- 3. Control de calidad ---")

df_prov = pd.read_csv(r"C:\Users\Usuario\Downloads\proveedores_materiales.csv")


def buscar_proveedores(material, prioridad):
    proveedores = df_prov[df_prov["material"] == material]

    # Ordenar según lo que se quiera priorizar
    if prioridad == "calidad":
        proveedores = proveedores.sort_values(by="calidad", ascending=False)
    elif prioridad == "precio":
        proveedores = proveedores.sort_values(by="precio_unitario", ascending=True)
    else:  # distancia
        proveedores = proveedores.sort_values(by="distancia_km", ascending=True)

    print(f"Proveedores de {material} (priorizando {prioridad}):")
    for i in range(len(proveedores)):
        print(f" - {proveedores['proveedor'].values[i]}: {proveedores['telefono'].values[i]}")


material = input("Ingrese el material: ")
prioridad = input("Priorizar (calidad / precio / distancia): ")
buscar_proveedores(material, prioridad)


# Análisis estadístico de resistencia del hormigón (ensayos de probetas)
print("\n--- Análisis estadístico de resistencia del hormigón ---")

df_probetas = pd.read_csv("ensayos_probetas.csv")
resistencias = df_probetas["resistencia_mpa"]

print(f"Cantidad de probetas: {resistencias.count()}")
print(f"Media: {resistencias.mean():.2f} MPa")
print(f"Desvío estándar: {resistencias.std():.2f} MPa")
print(f"Mínimo: {resistencias.min():.2f} MPa")
print(f"Máximo: {resistencias.max():.2f} MPa")
print(f"Coeficiente de variación: {resistencias.std() / resistencias.mean() * 100:.2f} %")
