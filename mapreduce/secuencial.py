import sys, csv, time

if len(sys.argv) < 2:
    print("Uso: python3 secuencial.py <archivo.csv>")
    sys.exit(1)

archivo = sys.argv[1]
inicio = time.time()
totales = {}

with open(archivo, 'r') as f:
    reader = csv.reader(f)
    header = next(reader, None)
    for row in reader:
        if len(row) == 8:
            try:
                producto = row[4]
                ingreso = float(row[5]) * float(row[6])
                totales[producto] = totales.get(producto, 0.0) + ingreso
            except ValueError:
                continue

top10 = sorted(totales.items(), key=lambda x: x[1], reverse=True)[:10]
duracion = time.time() - inicio

print("=== Top 10 Productos ===")
for p, ing in top10:
    print(f"{p}: {ing:.2f}")
print(f"\nTiempo de ejecución secuencial: {duracion:.4f} segundos")