from database import *

turista = {
    "ID": 11,
    "Nombre": "Nombre Anonimo", 
    "Apellido": "Apellido Anonimo",
    "Provincia": "Provincia Desconocida",
    "Comentario": "Sin Comentario"
}

collection_turistas.insert_one(turista)
print("Turista agregado")

