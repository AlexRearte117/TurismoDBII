from turista import turista
from pymongo import MongoClient

#URL de MongoDB
client = MongoClient("mongodb+srv://reartefalex:EGkGmPDP4KkkyuIU@cluster0.jg7mg15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#Seleccionar la db
db = client['Turismo']
#Seleccionar la colección
collection_turistas = db['turista']


print("Todos los turistas: ")
turista.obtener_todos_los_turistas()
print("turista id: ")
turista.obtener_turista_por_id(1)
print("turista por nombre: ")
turista.obtener_turista_por_nombre("Gabriel")
print("turista por apellido: ")
turista.obtener_turista_por_apellido("Rearte")
print("turistas por provincia: ")
turista.obtener_turistas_por_provincia("La Rioja")
print("turistas por comentarios: ")
turista.obtener_turistas_por_comentarios("None")

#from turista import turista_for_dao
#turista_for_dao.lugar_mas_visitado()