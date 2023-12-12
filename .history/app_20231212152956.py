import mysql.connector
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os, time

app = Flask(__name__)
CORS(app)

class Catalogo:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vehiculos (
            codigo INT,
            marca VARCHAR(30) NOT NULL,
            modelo VARCHAR (255) NOT NULL,
            año INT NOT NULL,
            precio DECIMAL (10,2) NOT NULL,
            foto VARCHAR (255)
            )''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

        
    def agregar_vehiculo(self, codigo, marca, modelo, anio, precio): # foto):
        self.cursor.execute(f"SELECT * FROM vehiculos WHERE codigo = {codigo}")
        vehiculo_existe = self.cursor.fetchone()
        if vehiculo_existe:
            return False
        
        sql = f"INSERT INTO vehiculos (codigo, marca, modelo, año, precio) VALUES ({codigo}, '{marca}', '{modelo}', {anio}, {precio})" #  '{foto}')" # {precio}"
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    def listar_vehiculos(self):
            self.cursor.execute("SELECT * FROM vehiculos")
            vehiculos = self.cursor.fetchall()
            print(vehiculos)
            return vehiculos

    def consultar_vehiculo(self, codigo):
        self.cursor.execute(f"SELECT * FROM vehiculos WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    def modificar_vehiculo(self, codigo, nueva_marca, nuevo_modelo, nuevo_anio, nuevo_precio):#, nueva_foto):
        sql = f"UPDATE vehiculos SET marca = '{nueva_marca}', modelo = '{nuevo_modelo}', año = {nuevo_anio}, precio = {nuevo_precio} WHERE codigo = {codigo}" #( falta nueva_foto)
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.rowcount > 0

    def listar_vehiculos(self):
        self.cursor.execute("SELECT * FROM vehiculos")
        vehiculos = self.cursor.fetchall()
        return vehiculos

    def eliminar_vehiculo(self, codigo):
        self.cursor.execute(f"DELETE FROM vehiculos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def mostrar_vehiculo(self, codigo):
        vehiculo = self.consultar_vehiculo(codigo)
        if vehiculo:
            print("-" * 30)
            print(f"    Codigo: {vehiculo['codigo']}")
            print(f"     Marca: {vehiculo['marca']}")
            print(f"    Modelo: {vehiculo['modelo']}")
            print(f"       Año: {vehiculo['anio']}")
            print(f"    Precio: {vehiculo['precio']}")
            #print(f"      Foto: {vehiculo['foto']}")
            print("-" * 30)
        else:
            print("Vehículo no encontrado.")

# Crear una instancia de la clase catalogo
catalogo = Catalogo(host='mauropy.mysql.pythonanywhere-services.com', user='mauropy', password='passDataBase', database='mauropy$app_concesionaria')
# catalogo = Catalogo(host='localhost', user='root', password='', database='app_concesionaria')

# Carpeta para guardar las imagenes
# ruta_destino = '/home/mauropy/mysite/static/img/'
ruta_destino = './set_imagenes/'

# Listar Vehiculos
@app.route("/vehiculos", methods=["GET"])
def listar_vehiculos():
    vehiculos = catalogo.listar_vehiculos()
    print(vehiculos)
    return jsonify(vehiculos)

# Ruta Mostrar Vehiculo
@app.route("/vehiculos/<int:codigo>", methods=["GET"])
def mostrar_vehiculo(codigo):
    vehiculo = catalogo.consultar_vehiculo(codigo)
    if vehiculo:
        return jsonify(vehiculo)
    else:
        return "Vehículo no encontrado", 404

# Ruta Agregar Vehiculo    
@app.route("/vehiculos", methods=["POST"])
def agregar_vehiculo():
    # Recojo los datos del form
    codigo = request.form['codigo']
    marca = request.form['marca']
    modelo = request.form['modelo']
    anio = request.form['año']
    precio = request.form['precio']
    # foto = request.form['foto']
    # foto = request.files['foto']
    # nombre_imagen = secure_filename(foto.filename)

    # nombre_base, extension = os.path.splitext(nombre_imagen)
    # nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    # foto.save(os.path.join(ruta_destino, nombre_imagen))  

    if catalogo.agregar_vehiculo(codigo, marca, modelo, anio, precio): # (foto, nombre_imagen):
        return jsonify({"mensaje": "Vehículo agregado"}), 201
    else:
        return jsonify({"mensaje": "No se completo la carga, el vehículo fue registrado anteriormente"}), 400

@app.route("/vehiculos/<int:codigo>", methods=["PUT"])
def modificar_vehiculo(codigo):
    # Recojo los datos del form
    nueva_marca = request.form.get("marca")
    nuevo_modelo = request.form.get("modelo")
    nuevo_anio = request.form.get("año")
    nuevo_precio = request.form.get("precio")
    # Procesamiento de la imagen
    # foto = request.files['foto']
    # nombre_imagen = secure_filename(foto.filename)
    # nombre_base, extension = os.path.splitext(nombre_imagen)
    # nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    # foto.save(os.path.join(ruta_destino, nombre_imagen))
    
    # Actualización del vehículo
    if catalogo.modificar_vehiculo(codigo, nueva_marca, nuevo_modelo, nuevo_anio, nuevo_precio):#, nombre_imagen):
        return jsonify({"mensaje": "Datos de vehículo modificado"}), 200
    else:
        return jsonify({"mensaje": "Vehículo no encontrado"}), 404

@app.route("/vehiculos/<int:codigo>", methods=["DELETE"])
def eliminar_vehiculo(codigo):
    # Primero, obtén la información del producto para encontrar la imagen
    # vehiculo = catalogo.consultar_vehiculo(codigo)
    # if vehiculo:
        # Eliminar la imagen asociada si existe
        # ruta_imagen = os.path.join(ruta_destino, vehiculo['foto'])
        # if os.path.exists(ruta_imagen):
        #     os.remove(ruta_imagen)
        # Luego, elimina el producto del catálogo
    if catalogo.eliminar_vehiculo(codigo):
        return jsonify({"mensaje": "Vehículo eliminado"}), 200
    else:
        # return jsonify({"mensaje": "Error al eliminar el vehículo"}), 500
    # else:
        return jsonify({"mensaje": "Vehículo no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
