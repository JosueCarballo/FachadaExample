from flask import Flask, jsonify, request
import mysql.connector
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Configuración de la conexión con MySQL (XAMPP)
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="mascotas_db"
    )

# Endpoint para obtener todas las mascotas
@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mascotas")
    mascotas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(mascotas)

# Endpoint para obtener una mascota por ID
@app.route('/mascotas/<int:id>', methods=['GET'])
def obtener_mascota(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mascotas WHERE id = %s", (id,))
    mascota = cursor.fetchone()
    cursor.close()
    conexion.close()
    if mascota:
        return jsonify(mascota)
    return jsonify({"mensaje": "Mascota no encontrada"}), 404

# Endpoint para agregar una nueva mascota
@app.route('/mascotas', methods=['POST'])
def agregar_mascota():
    datos = request.json
    nombre = datos.get("nombre")
    tipo = datos.get("tipo")
    edad = datos.get("edad")

    if not nombre or not tipo or edad is None:
        return jsonify({"error": "Faltan datos"}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO mascotas (nombre, tipo, edad) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, tipo, edad))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mascota agregada correctamente"}), 201

# Endpoint para actualizar una mascota
@app.route('/mascotas/<int:id>', methods=['PUT'])
def actualizar_mascota(id):
    datos = request.json
    nombre = datos.get("nombre")
    tipo = datos.get("tipo")
    edad = datos.get("edad")

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM mascotas WHERE id = %s", (id,))
    mascota = cursor.fetchone()

    if not mascota:
        return jsonify({"mensaje": "Mascota no encontrada"}), 404

    sql = "UPDATE mascotas SET nombre=%s, tipo=%s, edad=%s WHERE id=%s"
    cursor.execute(sql, (nombre, tipo, edad, id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mascota actualizada correctamente"})

# Endpoint para eliminar una mascota
@app.route('/mascotas/<int:id>', methods=['DELETE'])
def eliminar_mascota(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM mascotas WHERE id = %s", (id,))
    mascota = cursor.fetchone()

    if not mascota:
        return jsonify({"mensaje": "Mascota no encontrada"}), 404

    cursor.execute("DELETE FROM mascotas WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mascota eliminada correctamente"})

# Configurar Swagger UI
SWAGGER_URL = "/veterinaria"
API_URL = "/static/swagger.yaml"
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Ejecutar la API
if __name__ == '__main__':
    app.run(debug=True)
