from function.ConexionDB import collection_turistas
from mongoengine import IntField, StringField


class Turista():
    id = IntField(primary_key=True, required=True)
    nombre = StringField(required=True, max_length=50)
    apellido = StringField(required=True, max_length=50)
    provincia = StringField(required=True, max_length=50)
    comentario = StringField(max_length=200)

# DAO para Turista
class turista_for_dao:

    @staticmethod
    def crear_turista(id, nombre, apellido, provincia, comentario):
        turista = {
            "_id": id,
            "nombre": nombre,
            "apellido": apellido,
            "provincia": provincia,
            "comentario": comentario
        }
        collection_turistas.insert_one(turista)

    @staticmethod
    def obtener_todos_los_turistas():
        for turista in collection_turistas.find():
            print(turista)
    
    @staticmethod
    def obtener_turista_por_id(id):
        for turista in collection_turistas.find({"_id": id}):
            print(turista)
    
    @staticmethod
    def obtener_turista_por_nombre(nombre):
        for turista in collection_turistas.find({"nombre": nombre}):
            print(turista)

    @staticmethod
    def obtener_turistas_por_provincia(provincia):
        for turista in collection_turistas.find({"provincia": provincia}):
            print(turista)

    @staticmethod
    def obtener_turista_por_apellido(apellido):
        for turista in collection_turistas.find({"apellido": apellido}):
            print(turista)

    @staticmethod
    def obtener_turistas_por_comentarios(comentarios):
        for turista in collection_turistas.find({"comentario": comentarios}):
            print(turista)
    
    @staticmethod
    def eliminar_turista_por_id(id):
        collection_turistas.delete_one({"_id": id})
        print(f"Turista con ID {id} eliminado.")

    @staticmethod
    def obtener_turistas_por_nombre_y_provincia(nombre, provincia):
        for turista in collection_turistas.find({"nombre": nombre, "provincia": provincia}):
            print(turista)


    @staticmethod
    def contar_turistas_por_provincia(provincia):
        count = collection_turistas.count_documents({"provincia": provincia})
        print(f"Total de turistas en {provincia}: {count}")

    @staticmethod
    def obtener_turistas_anonimos():
        turistas_anonimos = list(collection_turistas.find({
            "Nombre": "Nombre Anonimo", 
            "Apellido": "Apellido Anonimo", 
            "Provincia": "Provincia Desconocida"
        }))
        
        # Mostrar los turistas anónimos
        for turista in turistas_anonimos:
            print(turista)
        
        # Mostrar la cantidad de turistas anónimos
        print(f"Cantidad de turistas anónimos: {len(turistas_anonimos)}")

    @staticmethod
    def obtener_turistas_registrados():
        turistas_registrados = list(collection_turistas.find({
            "Nombre": {"$ne": "Nombre Anonimo"}, 
            "Apellido": {"$ne": "Apellido Anonimo"}, 
            "Provincia": {"$ne": "Provincia Desconocida"}
        }))
        
        # Mostrar los turistas registrados
        for turista in turistas_registrados:
            print(turista)
        
        # Mostrar la cantidad de turistas registrados
        print(f"Cantidad de turistas registrados: {len(turistas_registrados)}")


    @staticmethod
    def actualizar_turista_por_id(id, nuevo_nombre=None, nuevo_apellido=None, nueva_provincia=None, nuevo_comentario=None):
        # Creamos el diccionario con los campos que se desean actualizar
        cambios = {}
        
        if nuevo_nombre:
            cambios["nombre"] = nuevo_nombre
        if nuevo_apellido:
            cambios["apellido"] = nuevo_apellido
        if nueva_provincia:
            cambios["provincia"] = nueva_provincia
        if nuevo_comentario:
            cambios["comentario"] = nuevo_comentario

        # Si hay cambios que hacer, ejecutamos el update
        if cambios:
            resultado = collection_turistas.update_one(
                {"_id": id},  # Filtro para encontrar el turista por ID
                {"$set": cambios}  # Operador $set para actualizar los campos especificados
            )
            
            if resultado.matched_count > 0:
                print(f"El turista con ID '{id}' fue actualizado exitosamente.")
            else:
                print(f"No se encontró ningún turista con ID '{id}'.")
        else:
            print("No se proporcionaron cambios para actualizar.")

    @staticmethod
    def lugar_mas_visitado():
        pipeline = [
            {"$group": {"_id": "$comentario.lugar_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        resultado = list(collection_turistas.aggregate(pipeline))
        if resultado:
            lugar_id = resultado[0]["_id"]
            visitas = resultado[0]["count"]
            print(f"El lugar con ID '{lugar_id}' es el más visitado, con {visitas} visitas.")
            return lugar_id, visitas
        else:
            print("No hay visitas registradas.")
            return None

    @staticmethod
    def cantidad_comentarios():
        count = collection_turistas.count_documents({"comentario": {"$exists": True}})
        print(f"Hay {count} comentarios registrados.")
        return count

    @staticmethod
    def log_visitas_por_lugar(lugar_id):
        visitas = collection_turistas.find({"comentario.lugar_id": lugar_id})
        print(f"Log de visitas para el lugar con ID '{lugar_id}':")
        for visita in visitas:
            print(f"Turista: {visita['nombre']} {visita['apellido']}, Comentario: {visita['comentario']['texto']}, Fecha: {visita.get('fecha_hora', 'Sin fecha registrada')}")

# Nota: Se ha consolidado 'turista_for_dao' en una única clase.
