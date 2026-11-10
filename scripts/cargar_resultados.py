import psycopg2
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "datamart")
DB_USER = os.getenv("POSTGRES_USER", "usuario_db")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password_seguro")

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS top_productos (
        id SERIAL PRIMARY KEY,
        producto VARCHAR(100),
        ingreso_total NUMERIC(15, 2)
    );
""")

with open('/data/output/resultado/part-00000', 'r') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            producto, ingreso = parts
            cur.execute(
                "INSERT INTO top_productos (producto, ingreso_total) VALUES (%s, %s);",
                (producto, float(ingreso))
            )

conn.commit()
cur.close()
conn.close()
print("Resultados cargados exitosamente en PostgreSQL.")