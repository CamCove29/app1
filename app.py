from flask import Flask, jsonify, request, json, Response
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a MySQL
db = mysql.connector.connect(
    host="54.224.61.132",
    user="root",
    password="utec",
    database="db_books",
    port="8005"
)

# Crear un cursor global
cursor = db.cursor()

### CRUD para la tabla "Libros" ###

# Get echo test for load balancer's health check
@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}

# Obtener todos los libros
@app.route('/libros', methods=['GET'])
def get_libros():
    cursor.execute("SELECT * FROM Libros")
    libros = cursor.fetchall()
    result = []
    for row in libros:
        result.append({
            'ID_libro': row[0],
            'Título': row[1],
            'ID_autor': row[2],
            'ISBN': row[3],
            'Género': row[4],
            'Fecha_publicación': str(row[5]),
            'Número_páginas': row[6],
            'Editorial': row[7],
            'Idioma': row[8],
            'Resumen': row[9],
            'Disponibilidad': row[10]
        })
    return jsonify(result), 200

# Obtener un libro por su ID
@app.route('/libros/<int:id>', methods=['GET'])
def get_libro(id):
    cursor.execute("SELECT * FROM Libros WHERE ID_libro = %s", (id,))
    libro = cursor.fetchone()
    if libro:
        result = {
            'ID_libro': libro[0],
            'Título': libro[1],
            'ID_autor': libro[2],
            'ISBN': libro[3],
            'Género': libro[4],
            'Fecha_publicación': str(libro[5]),
            'Número_páginas': libro[6],
            'Editorial': libro[7],
            'Idioma': libro[8],
            'Resumen': libro[9],
            'Disponibilidad': libro[10]
        }
        return jsonify(result), 200
    return jsonify({'message': 'Libro no encontrado'}), 404

# Crear un nuevo libro
@app.route('/libros', methods=['POST'])
def create_libro():
    try:
        data = request.get_json()

        # Validar la entrada
        if not data or not all(key in data for key in ('Título', 'ID_autor', 'ISBN', 'Género', 'Fecha_publicación', 'Número_páginas', 'Editorial', 'Idioma', 'Resumen', 'Disponibilidad')):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        query = """
        INSERT INTO Libros (Título, ID_autor, ISBN, Género, Fecha_publicación, Número_páginas, Editorial, Idioma, Resumen, Disponibilidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['Título'], data['ID_autor'], data['ISBN'], data['Género'], data['Fecha_publicación'], data['Número_páginas'], data['Editorial'], data['Idioma'], data['Resumen'], data['Disponibilidad']))
        db.commit()

        return jsonify({'message': 'Libro creado exitosamente'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar un libro existente
@app.route('/libros/<int:id>', methods=['PUT'])
def update_libro(id):
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ('Título', 'ID_autor', 'ISBN', 'Género', 'Fecha_publicación', 'Número_páginas', 'Editorial', 'Idioma', 'Resumen', 'Disponibilidad')):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        query = """
        UPDATE Libros 
        SET Título=%s, ID_autor=%s, ISBN=%s, Género=%s, Fecha_publicación=%s, Número_páginas=%s, Editorial=%s, Idioma=%s, Resumen=%s, Disponibilidad=%s 
        WHERE ID_libro=%s
        """
        cursor.execute(query, (data['Título'], data['ID_autor'], data['ISBN'], data['Género'], data['Fecha_publicación'], data['Número_páginas'], data['Editorial'], data['Idioma'], data['Resumen'], data['Disponibilidad'], id))
        db.commit()

        return jsonify({'message': 'Libro actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un libro
@app.route('/libros/<int:id>', methods=['DELETE'])
def delete_libro(id):
    try:
        cursor.execute("DELETE FROM Libros WHERE ID_libro=%s", (id,))
        db.commit()
        return jsonify({'message': 'Libro eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

### CRUD para la tabla "Autor" ###

# Obtener todos los autores
@app.route('/autores', methods=['GET'])
def get_autores():
    cursor.execute("SELECT * FROM Autor")
    autores = cursor.fetchall()
    result = []
    for row in autores:
        result.append({
            'ID_autor': row[0],
            'Nombre': row[1],
            'Fecha_nacimiento': str(row[2]),
            'Nacionalidad': row[3],
            'Biografía': row[4]
        })
    return jsonify(result), 200

# Obtener un autor por su ID
@app.route('/autores/<int:id>', methods=['GET'])
def get_autor(id):
    cursor.execute("SELECT * FROM Autor WHERE ID_autor = %s", (id,))
    autor = cursor.fetchone()
    if autor:
        result = {
            'ID_autor': autor[0],
            'Nombre': autor[1],
            'Fecha_nacimiento': str(autor[2]),
            'Nacionalidad': autor[3],
            'Biografía': autor[4]
        }
        return jsonify(result), 200
    return jsonify({'message': 'Autor no encontrado'}), 404

# Crear un nuevo autor
@app.route('/autores', methods=['POST'])
def create_autor():
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ('Nombre', 'Fecha_nacimiento', 'Nacionalidad', 'Biografía')):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        query = """
        INSERT INTO Autor (Nombre, Fecha_nacimiento, Nacionalidad, Biografía)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (data['Nombre'], data['Fecha_nacimiento'], data['Nacionalidad'], data['Biografía']))
        db.commit()

        return jsonify({'message': 'Autor creado exitosamente'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar un autor existente
@app.route('/autores/<int:id>', methods=['PUT'])
def update_autor(id):
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ('Nombre', 'Fecha_nacimiento', 'Nacionalidad', 'Biografía')):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        query = """
        UPDATE Autor 
        SET Nombre=%s, Fecha_nacimiento=%s, Nacionalidad=%s, Biografía=%s 
        WHERE ID_autor=%s
        """
        cursor.execute(query, (data['Nombre'], data['Fecha_nacimiento'], data['Nacionalidad'], data['Biografía'], id))
        db.commit()

        return jsonify({'message': 'Autor actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un autor
@app.route('/autores/<int:id>', methods=['DELETE'])
def delete_autor(id):
    try:
        cursor.execute("DELETE FROM Autor WHERE ID_autor=%s", (id,))
        db.commit()
        return jsonify({'message': 'Autor eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

### Relaciones entre APIs ###

# Obtener valoraciones de un libro
@app.route('/libros/<int:id>/valoraciones', methods=['GET'])
def get_valoraciones_libro(id):
    cursor.execute("""
    SELECT v.ID_valoracion, c.Nombre, c.Apellido, v.Puntuacion 
    FROM Valoraciones v 
    JOIN Clientes c ON v.ID_cliente = c.ID_cliente 
    WHERE v.ID_libro = %s
    """, (id,))
    valoraciones = cursor.fetchall()
    result = []
    for row in valoraciones:
        result.append({
            'ID_valoracion': row[0],
            'Nombre_cliente': f"{row[1]} {row[2]}",
            'Puntuacion': row[3]
        })
    return jsonify(result), 200

# Obtener reservas de un libro
@app.route('/libros/<int:id>/reservas', methods=['GET'])
def get_reservas_libro(id):
    cursor.execute("""
    SELECT r.ID_reserva, c.Nombre, c.Apellido 
    FROM Reservas r 
    JOIN Clientes c ON r.ID_cliente = c.ID_cliente 
    WHERE r.ID_libro = %s
    """, (id,))
    reservas = cursor.fetchall()
    result = []
    for row in reservas:
        result.append({
            'ID_reserva': row[0],
            'Nombre_cliente': f"{row[1]} {row[2]}"
        })
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
