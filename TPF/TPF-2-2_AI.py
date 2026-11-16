import csv
import os


def leer_datos_csv(nombre_archivo):
  # Busca el CSV en la misma carpeta donde está guardado este script
  carpeta_actual = os.path.dirname(os.path.abspath(__file__))
  ruta_csv = os.path.join(carpeta_actual, nombre_archivo)

  datos = []
  with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
      datos.append({
          "punto": fila["punto_muestreo"].strip().upper(),
          "profundidad": float(fila["profundidad_m"]),
          "tipo_suelo": fila["tipo_suelo"],
          "resistencia": float(fila["resistencia_kpa"]),
          "humedad": float(fila["humedad_porcentaje"]),
      })
  return datos


def buscar_profundidad_minima(datos, punto_buscado, resistencia_objetivo):
  # Filtramos los registros del punto de muestreo elegido
  registros_punto = [d for d in datos if d["punto"] == punto_buscado]

  if not registros_punto:
    return None, "Punto de muestreo no encontrado en el archivo."

  # Ordenamos de menor a mayor profundidad (1.5m -> 3.0m -> 5.0m)
  registros_punto.sort(key=lambda x: x["profundidad"])

  # Buscamos el primer estrato que alcance o supere la resistencia pedida
  for registro in registros_punto:
    if registro["resistencia"] >= resistencia_objetivo:
      return registro["profundidad"], registro["tipo_suelo"]

  max_res = max(r["resistencia"] for r in registros_punto)
  return (
      None,
      f"Ningún estrato alcanza {resistencia_objetivo} kPa (máximo en"
      f" {punto_buscado}: {max_res} kPa).",
  )


def calcular_humedad_promedio(datos):
  humedades_por_punto = {}

  # Agrupamos todas las humedades por cada punto (P1, P2, etc.)
  for d in datos:
    punto = d["punto"]
    if punto not in humedades_por_punto:
      humedades_por_punto[punto] = []
    humedades_por_punto[punto].append(d["humedad"])

  # Calculamos el promedio para cada punto
  promedios = {}
  for punto, lista_humedades in humedades_por_punto.items():
    promedios[punto] = round(sum(lista_humedades) / len(lista_humedades), 2)

  return promedios


def guardar_informe(
    nombre_salida, punto, resistencia, prof_min, detalle_suelo, promedios_humedad
):
  carpeta_actual = os.path.dirname(os.path.abspath(__file__))
  ruta_txt = os.path.join(carpeta_actual, nombre_salida)

  with open(ruta_txt, mode="w", encoding="utf-8") as archivo:
    archivo.write("====================================================\n")
    archivo.write("   INFORME DE ENSAYOS DE SUELO - VILLA MARÍA\n")
    archivo.write("====================================================\n\n")

    archivo.write("1. CONSULTA DE PROFUNDIDAD MÍNIMA\n")
    archivo.write("----------------------------------------------------\n")
    archivo.write(f" - Punto de muestreo analizado: {punto}\n")
    archivo.write(f" - Resistencia requerida: {resistencia} kPa\n")

    if prof_min is not None:
      archivo.write(f" - Profundidad mínima a alcanzar: {prof_min} m\n")
      archivo.write(f" - Tipo de suelo en ese estrato: {detalle_suelo}\n\n")
    else:
      archivo.write(f" - Resultado: {detalle_suelo}\n\n")

    archivo.write("2. HUMEDAD PROMEDIO POR PUNTO DE MUESTREO\n")
    archivo.write("----------------------------------------------------\n")
    for p, prom in promedios_humedad.items():
      archivo.write(f" - {p}: {prom} %\n")

    archivo.write("\n====================================================\n")

  return ruta_txt


def main():
  archivo_csv = "ensayos_suelo.csv"
  datos = leer_datos_csv(archivo_csv)

  print("--- ANÁLISIS DE SUELOS DE VILLA MARÍA ---")
  punto_ingresado = (
      input("Ingrese el punto de muestreo (ej: P1, P2, ..., P7): ")
      .strip()
      .upper()
  )
  resistencia_ingresada = float(
      input("Ingrese la resistencia mínima requerida en kPa: ")
  )

  # Cálculos principales
  prof_min, detalle_suelo = buscar_profundidad_minima(
      datos, punto_ingresado, resistencia_ingresada
  )
  promedios_humedad = calcular_humedad_promedio(datos)

  # Mostrar resultados en consola
  print("\n--- RESULTADOS ---")
  if prof_min is not None:
    print(
        f"Para alcanzar {resistencia_ingresada} kPa en {punto_ingresado}, debe"
        f" excavar hasta {prof_min} m ({detalle_suelo})."
    )
  else:
    print(f"Aviso: {detalle_suelo}")

  print("\nHumedad promedio por punto:")
  for p, prom in promedios_humedad.items():
    print(f" - {p}: {prom}%")

  # Guardar en archivo de texto
  ruta_guardada = guardar_informe(
      "informe_suelos.txt",
      punto_ingresado,
      resistencia_ingresada,
      prof_min,
      detalle_suelo,
      promedios_humedad,
  )
  print(f"\nInforme guardado exitosamente en: {ruta_guardada}")


main()
