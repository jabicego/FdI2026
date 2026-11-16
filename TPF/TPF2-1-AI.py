import csv
import math
from pathlib import Path


def cargar_suelo(csv_path="ensayos_suelo.csv"):
    """
    Lee el CSV de ensayos de suelo y devuelve una lista de diccionarios.
    """
    ruta = Path(csv_path)

    if not ruta.exists():
        # Si el archivo está en una carpeta parent o subcarpeta
        alternativas = [
            Path.cwd() / csv_path,
            Path.cwd() / "TPF" / csv_path,
            Path(__file__).resolve().parent / csv_path,
            Path(__file__).resolve().parent / "TPF" / csv_path
        ]
        for p in alternativas:
            if p.exists():
                ruta = p
                break

    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        datos = list(csv.DictReader(archivo))

    return datos


def buscar_resistencia_en_profundidad(punto_muestreo, profundidad_deseada, datos):
    """
    Busca la resistencia del suelo para un punto y profundidad.
    Si la profundidad no coincide exactamente, hace interpolación lineal.
    """
    punto = str(punto_muestreo).strip().upper()
    perfiles = [d for d in datos if d["punto_muestreo"].strip().upper() == punto]

    if not perfiles:
        raise ValueError(f"No existe el punto de muestreo '{punto_muestreo}'.")

    perfiles = sorted(perfiles, key=lambda x: float(x["profundidad_m"]))

    profundidades = [float(d["profundidad_m"]) for d in perfiles]
    resistencias = [float(d["resistencia_kpa"]) for d in perfiles]
    tipos = [d["tipo_suelo"] for d in perfiles]

    if profundidad_deseada <= profundidades[0]:
        return resistencias[0], tipos[0]

    if profundidad_deseada >= profundidades[-1]:
        return resistencias[-1], tipos[-1]

    for i in range(len(profundidades) - 1):
        p1 = profundidades[i]
        p2 = profundidades[i + 1]

        if p1 <= profundidad_deseada <= p2:
            r1 = resistencias[i]
            r2 = resistencias[i + 1]

            if p2 == p1:
                return r1, tipos[i]

            fraccion = (profundidad_deseada - p1) / (p2 - p1)
            resistencia = r1 + (r2 - r1) * fraccion

            tipo = tipos[i] if abs(profundidad_deseada - p1) <= abs(profundidad_deseada - p2) else tipos[i + 1]
            return resistencia, tipo

    raise ValueError("No se pudo calcular la resistencia para esa profundidad.")


def dimensionar_zapata(carga_columna, punto_muestreo, profundidad_deseada,
                      forma="cuadrada", relacion_lados=1.0, csv_path="ensayos_suelo.csv"):
    """
    Dimensiona una zapata aislada según la carga, profundidad y tipo de suelo.
    """
    if carga_columna <= 0:
        raise ValueError("La carga de la columna debe ser mayor que cero.")
    if forma.lower() not in {"cuadrada", "rectangular"}:
        raise ValueError("La forma debe ser 'cuadrada' o 'rectangular'.")
    if relacion_lados <= 0:
        raise ValueError("La relación de lados debe ser mayor que cero.")

    datos = cargar_suelo(csv_path)
    resistencia_kpa, tipo_suelo = buscar_resistencia_en_profundidad(punto_muestreo, profundidad_deseada, datos)

    tipo = tipo_suelo.lower()
    if "grava" in tipo or "arena" in tipo:
        factor_seguridad = 2.0
    elif "limo" in tipo or "arcilla" in tipo:
        factor_seguridad = 2.5
    else:
        factor_seguridad = 2.8

    esfuerzo_admisible = resistencia_kpa / factor_seguridad  # kPa = kN/m²
    area_requerida = carga_columna / esfuerzo_admisible

    if forma.lower() == "cuadrada":
        lado = math.sqrt(area_requerida)
        ancho = lado
        largo = lado
    else:
        ancho = math.sqrt(area_requerida / relacion_lados)
        largo = ancho * relacion_lados

    resultado = {
        "punto_muestreo": str(punto_muestreo).upper(),
        "tipo_suelo": tipo_suelo,
        "profundidad_deseada_m": profundidad_deseada,
        "resistencia_suelo_kpa": round(resistencia_kpa, 2),
        "esfuerzo_admisible_kpa": round(esfuerzo_admisible, 2),
        "area_requerida_m2": round(area_requerida, 2),
        "forma": forma.lower(),
        "relacion_lados": relacion_lados,
        "ancho_m": round(ancho, 2),
        "largo_m": round(largo, 2),
        "lado_m": round(math.sqrt(area_requerida), 2) if forma.lower() == "cuadrada" else None
    }
    return resultado


# ----------------------------
# Programa principal con input()
# ----------------------------
if __name__ == "__main__":
    print("=== DIMENSIONADO DE ZAPATA ===")

    try:
        carga_columna = float(input("Ingrese la carga de la columna en kN: "))
        punto_muestreo = input("Ingrese el punto de muestreo (ej: P1, P2, ..., P7): ").strip()
        profundidad_deseada = float(input("Ingrese la profundidad deseada en m: "))
        forma = input("Ingrese la forma de la zapata (cuadrada o rectangular): ").strip().lower()
        relacion_lados = 1.0

        if forma == "rectangular":
            relacion_lados = float(input("Ingrese la relación largo/ancho (ej: 1.5): "))

        resultado = dimensionar_zapata(
            carga_columna=carga_columna,
            punto_muestreo=punto_muestreo,
            profundidad_deseada=profundidad_deseada,
            forma=forma,
            relacion_lados=relacion_lados,
            csv_path="ensayos_suelo.csv"
        )

        print("\nRESULTADO:")
        print(f" - Punto de muestreo: {resultado['punto_muestreo']}")
        print(f" - Tipo de suelo: {resultado['tipo_suelo']}")
        print(f" - Resistencia del suelo: {resultado['resistencia_suelo_kpa']} kPa")
        print(f" - Esfuerzo admisible: {resultado['esfuerzo_admisible_kpa']} kPa")
        print(f" - Área requerida: {resultado['area_requerida_m2']} m²")

        if forma == "cuadrada":
            print(f" - Lado de la zapata: {resultado['lado_m']} m")
        else:
            print(f" - Ancho: {resultado['ancho_m']} m")
            print(f" - Largo: {resultado['largo_m']} m")

    except ValueError as e:
        print(f"\nError: {e}")
    except FileNotFoundError:
        print("\nError: No se encontró el archivo 'ensayos_suelo.csv'.")
        print("Verifique que el archivo esté en la misma carpeta del script.")