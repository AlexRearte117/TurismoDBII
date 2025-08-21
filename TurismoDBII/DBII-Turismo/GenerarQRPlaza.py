import qrcode
import matplotlib.pyplot as plt

# Información del Lugar
monumento = {
    "Codigo QR" : "https://gabito2.github.io/plazaPrincipal.github.io/"
}

# URL de Google Maps
url_google_maps = monumento["Codigo QR"]

# Generar el QR
qr = qrcode.QRCode(
    version=1,  # Tamaño del QR
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
    box_size=10,  # Tamaño de cada caja
    border=4  # Borde alrededor del QR
)
qr.add_data(url_google_maps)  # Añadir URL al QR
qr.make(fit=True)

# Crear imagen del QR
imagen_qr = qr.make_image(fill='black', back_color='white')

# Guardar el QR en un archivo
imagen_qr.save("qr_PlazaPrincipal.png")

# Mostrar el QR usando matplotlib
plt.imshow(imagen_qr)
plt.axis('off')  # No mostrar ejes
plt.show()

print("QR generado, guardado como qr_PlazaPrincipal.png y mostrado en pantalla.")

