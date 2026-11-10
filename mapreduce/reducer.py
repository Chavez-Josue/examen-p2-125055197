#!/usr/bin/env python3
import sys

totales = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        producto, ingreso = line.split("\t")
        ingreso = float(ingreso)
        totales[producto] = totales.get(producto, 0.0) + ingreso
    except ValueError:
        continue

# Ordenar productos de mayor a menor ingreso y tomar los 10 primeros
top10 = sorted(totales.items(), key=lambda x: x[1], reverse=True)[:10]

for producto, ingreso_total in top10:
    print(f"{producto}\t{ingreso_total:.2f}")