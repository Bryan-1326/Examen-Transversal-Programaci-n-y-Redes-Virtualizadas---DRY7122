import sqlite3
import hashlib
from http.server import HTTPServer, SimpleHTTPRequestHandler

conexion = sqlite3.connect('usuarios.db')
cursor = conexion.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, password_hash TEXT)''')
integrantes = [
    ("Bryan Castillo", "cisco123"), 
    ("Bastian Inostroza", "cisco456")
]
for nombre, password in integrantes:
    hash_pass = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, hash_pass))

conexion.commit()
print("Base de datos 'usuarios.db' generada exitosamente con los usuarios encriptados.")

puerto = 5800
server_address = ('', puerto)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"Servidor web iniciado correctamente en el puerto {puerto}...")
print("Presiona Ctrl+C para detener el servidor.")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServidor detenido por el usuario.")
    conexion.close()