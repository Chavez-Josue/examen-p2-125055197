#!/usr/bin/env python3
import sys

# Formato CSV: id, fecha_hora, tienda, categoria, producto, cantidad, precio_unitario, metodo_pago
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("id"):
        continue  # Ignorar línea vacía o encabezado

    parts = line.split(",")
    if len(parts) != 8:
        continue  # Ignorar líneas corruptas

    try:
        producto = parts[4]
        cantidad = float(parts[5])
        precio_unitario = float(parts[6])

        ingreso = cantidad * precio_unitario
        print(f"{producto}\t{ingreso:.2f}")
    except ValueError:
        continue