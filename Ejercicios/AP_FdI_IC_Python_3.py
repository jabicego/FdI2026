def cotizar_pedido(lista_compras, catalogo_precios):
  costo_total = 0.0
  sin_stock = []
  for material, kg_necesarios in lista_compras.items():
    if material in catalogo_precios:
      precio_kg = catalogo_precios[material]
      costo_total += kg_necesarios * precio_kg
    else:
      sin_stock.append(material)

  return round(costo_total, 2), sin_stock


precios_corralon = {
    "cemento": 180.0,
    "arena": 35.5,
    "piedras": 48.0,
    "cal": 110.0,
}

# --- PRUEBA 1: Pedido donde el corralón tiene todos los materiales ---
pedido_1 = {"cemento": 100.0, "arena": 200.0}

total_1, faltantes_1 = cotizar_pedido(pedido_1, precios_corralon)

print("--- PRUEBA 1: PEDIDO COMPLETO ---")
print("Costo total a pagar:", total_1)
print("Materiales no disponibles en corralón: ", faltantes_1)


# --- PRUEBA 2: Pedido con materiales que el corralón no trabaja ---
pedido_2 = {"cemento": 120.0, "hierro": 50.0, "madera": 30.0}

total_2, faltantes_2 = cotizar_pedido(pedido_2, precios_corralon)

print("--- PRUEBA 2: PEDIDO INCOMPLETO ---")
print("Costo total a pagar:", total_2)
print("Materiales no disponibles en corralón: ", faltantes_2)
