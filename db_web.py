import sqlite3
import hashlib
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 1. Gestión de Base de Datos y Claves Hash
conexion = sqlite3.connect('usuarios.db')
cursor = conexion.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT, password_hash TEXT)''')

# Integrantes del grupo
integrantes = [("Bryan Castillo", "cisco123"), ("Bastian Inostroza", "cisco456")]

for nombre, password in integrantes:
    hash_pass = hashlib.sha256(password.encode()).hexdigest()
    # Se inserta el usuario (esto se ejecutará cada vez que corras el script)
    cursor.execute("INSERTA usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, hash_pass))

conexion.commit()
print("Base de datos 'usuarios.db' creada. Usuarios y hashes almacenados.")

# 2. Servidor Web
puerto = 5800
server_address = ('', puerto)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"Servidor web iniciado correctamente en el puerto {puerto}...")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServidor detenido por el usuario.")
    conexion.close()