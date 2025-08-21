from database import collection_turistas

collection_turistas.update_one({"ID": 11}, {"$set": {"Nombre": "Pedro Leon", "Apellido": "Perez Leon", "Provincia": "Cordoba", "Comentario": "No hay comentarios"}})
print("Turista actualizado")

for turistas in collection_turistas.find():
    print(turistas)
    