from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "datamart"),
        user=os.getenv("DB_USER", "usuario_db"),
        password=os.getenv("DB_PASSWORD", "password_seguro")
    )

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