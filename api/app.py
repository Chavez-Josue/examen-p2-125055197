from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "ventas_db"),
        user=os.getenv("DB_USER", "usuario_db"),
        password=os.getenv("DB_PASSWORD", "password_seguro")
    )

@app.route('/', methods=['GET'])
def vista_web():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, producto, ingreso_total FROM top_productos ORDER BY ingreso_total DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Top 10 Productos - DataMart</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; background: #fff; margin-top: 20px; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #007bff; color: white; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Top 10 Productos por Ingreso Total</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Ingreso Total ($)</th>
            </tr>
    """
    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>${float(r[2]):,.2f}</td></tr>"
        
    html += """
        </table>
    </body>
    </html>
    """
    return html

@app.route('/resultados', methods=['GET'])
def get_resultados():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, producto, ingreso_total FROM top_productos;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "producto": r[1], "ingreso_total": float(r[2])} for r in rows])

@app.route('/resultados/<producto>', methods=['GET'])
def get_by_producto(producto):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, producto, ingreso_total FROM top_productos WHERE LOWER(producto) = LOWER(%s);", (producto,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "producto": r[1], "ingreso_total": float(r[2])} for r in rows])

@app.route('/resultados', methods=['POST'])
def add_resultado():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO top_productos (producto, ingreso_total) VALUES (%s, %s) RETURNING id;",
        (data['producto'], data['ingreso_total'])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "message": "Registro agregado"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)