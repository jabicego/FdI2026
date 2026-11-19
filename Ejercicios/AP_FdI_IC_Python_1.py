# ============================================
# CONTROL DE MATERIALES PARA UNA VEREDA
# Ingeniería Civil - Primer año - UTN FRVM
# ============================================

# INGRESO DE DATOS DE LA OBRA

obra = input("Ingrese el nombre de la obra: ")
obra = obra.strip()

superficie = float(input("Ingrese los m2 de vereda a realizar: "))

# CEMENTO

print("\n--- CEMENTO ---")

bolsas_cemento = int(input("Cantidad de bolsas disponibles: "))
kg_bolsa_cemento = float(input("Kg de cemento por bolsa: "))

cemento_disponible = bolsas_cemento * kg_bolsa_cemento
cemento_necesario = superficie * 30

print("Cant de cemento disponible: ", cemento_disponible)
print("Cant de cemento necesaria: ", cemento_necesario)

# ARENA

print("\n--- ARENA ---")

bolsas_arena = int(input("Cantidad de bolsas de arena disponibles: "))
kg_bolsa_arena = float(input("Kg de arena por bolsa: "))

arena_disponible = bolsas_arena * kg_bolsa_arena
arena_necesaria = superficie * 18

print("Cant de arena disponible: ", arena_disponible)
print("Cant dearena necesaria: ", arena_necesaria)

# PIEDRA

print("\n--- PIEDRA ---")

bolsas_piedra = int(input("Cantidad de bolsas de piedra disponibles: "))
kg_bolsa_piedra = float(input("Kg de piedra por bolsa: "))

piedra_disponible = bolsas_piedra * kg_bolsa_piedra
piedra_necesaria = superficie * 22

print("Cant de piedra disponible: ", piedra_disponible)
print("Cant de piedra necesaria: ", piedra_necesaria)



# RESUMEN DE LA OBRA

print("\n============================================")
print("       RESUMEN DE MATERIALES")
print("============================================")

print("Obra:", obra.upper())
print("Superficie a construir:", superficie, "m2")

# CONTROL DE DISPONIBILIDAD

materiales = ["Cemento", "Arena", "Piedra"]
disponibles = [cemento_disponible, arena_disponible, piedra_disponible]
necesarios = [cemento_necesario, arena_necesaria, piedra_necesaria]

faltantes = 0

for i in range(len(materiales)):
    print("\nMaterial:", materiales[i])
    #print("Disponible:", disponibles[i], "kg")
    #print("Necesario:", necesarios[i], "kg")

    diferencia = disponibles[i] - necesarios[i]

    if diferencia >= 0:
        print("Hay suficiente material.")

        if diferencia == 0:
            print("La cantidad es exacta.")
        else:
            print("Excedente:", diferencia, "kg")

    else:
        faltante = necesarios[i] - disponibles[i]

        print("Falta material.")
        print("Debe comprar:", faltante, "kg")

        faltantes += 1
      

# VERIFICACIÓN GENERAL DE LA OBRA

print("\n============================================")
print("       RESULTADO FINAL")
print("============================================")

print("Nombre de la Obra:", obra.upper())
print("Superfie total de la vereda:", superficie, "m2")

if faltantes == 0:
    print("Hay suficiente cantidad de todos los materiales.")
    print("LA OBRA PUEDE COMENZAR.")
else:
    print("No hay suficiente cantidad de todos los materiales.")
    print("LA OBRA NO PUEDE COMENZAR.")

print("============================================")
