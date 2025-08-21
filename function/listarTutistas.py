from ConexionDB import *

print("Turistas:")
for turista in collection_turistas.find():
    print(turista)

#Listar por id
# print("Turistas:")
# for turista in collection_turistas.find({"id": "1"}):
#     print(turista)

#Listar por nombre
print("Turistas:")
for turista in collection_turistas.find({"nombre": "Gabriel"}):
    print(turista)