import qrcode
import matplotlib.pyplot as plt
from flask import Flask, send_from_directory, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Archivo para almacenar el contador de visitas
contador_archivo = 'contador_visitas.txt'
comentarios_archivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'comentarios.txt')


# Función para leer el contador de visitas desde el archivo
def leer_contador():
    if os.path.exists(contador_archivo):
        with open(contador_archivo, 'r') as f:
            return int(f.read().strip())
    return 0

# Función para escribir el contador de visitas en el archivo
def escribir_contador(contador):
    with open(contador_archivo, 'w') as f:
        f.write(str(contador))

# Inicializar el contador de visitas
visitas = leer_contador()

# URL de tu página web (ajusta esto según tu configuración)
url_pagina_web = "http://localhost:5000"

# Generar el QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4
)
qr.add_data(url_pagina_web)
qr.make(fit=True)

# Crear imagen del QR
imagen_qr = qr.make_image(fill='black', back_color='white')

# Guardar el QR en un archivo
imagen_qr.save("qr_CristoPortezuelo.png")

# Mostrar el QR usando matplotlib
plt.imshow(imagen_qr)
plt.axis('off')
plt.show()

print("QR generado, guardado como qr_CristoPortezuelo.png y mostrado en pantalla.")

@app.route('/')
def index():
    global visitas
    visitas += 1
    escribir_contador(visitas)
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Cantidad de usuarios: {visitas}")
    print(f"Fecha y hora: {fecha_hora_actual}")
    print("-" * 30)
    
    # Ruta al archivo index1.html en la carpeta page
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'page'), 'index1.html')

@app.route('/enviar_comentario', methods=['POST'])
def enviar_comentario():
    comentario = request.form['comentario']
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(comentarios_archivo, 'a') as f:
        f.write(f"{fecha_hora_actual}: {comentario}\n")
    
    print(f"Nuevo comentario recibido: {comentario}")
    return redirect(url_for('index'))

@app.route('/<path:path>')
def serve_file(path):
    # Ruta para servir otros archivos estáticos
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'page'), path)

if __name__ == '__main__':
    print("Servidor iniciado. Escanea el código QR para acceder a la página.")
    app.run(debug=True, host='0.0.0.0')


# Explicación de los cambios:
# Archivo de Contador: Se utiliza un archivo de texto (contador_visitas.txt) para almacenar el número de visitas.
# Funciones de Lectura y Escritura: Se agregaron funciones para leer y escribir el contador de visitas en el archivo.
# Persistencia del Contador: Al iniciar el programa, se lee el contador del archivo, y cada vez que se incrementa el contador, se escribe el nuevo valor en el archivo.