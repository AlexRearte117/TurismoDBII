from transformers import pipeline
from function.ConexionDB import collection_lugares, collection_turistas
import os
os.environ["MONGODB_URI"] = "mongodb+srv://reartefalex:EGkGmPDP4KkkyuIU@cluster0.jg7mg15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Conexión centralizada importada desde function/ConexionDB.py

class lugares_for_dao:

    @staticmethod
    def crear_lugar(id, nombre, ubicacion, descripción, horario, comentarios, visitas):
        lugar = {
            "_id" : id,
            "nombre": nombre,
            "ubicacion": ubicacion,
            "descripción": descripción,
            "horario": horario,
            "comentarios": comentarios,
            "visitas": visitas
        }
        collection_lugares.insert_one(lugar)
        print("Lugar creado")

    @staticmethod
    def obtener_todos_los_lugares():
        for lugares in collection_lugares.find():
            print(lugares)
    
    @staticmethod
    def obtener_lugar_por_id(id):
        for lugar in collection_lugares.find({"_id": id}):
            print(lugar)
    
    @staticmethod
    def obtener_lugar_por_nombre(nombre):
        for lugar in collection_lugares.find({"nombre": nombre}):
            print(lugar)

    @staticmethod
    def obtener_lugar_por_ubicacion(ubicacion):
        for lugar in collection_lugares.find({"ubicacion": ubicacion}):
            print(lugar)

    @staticmethod
    def obtener_lugar_por_descripción(descripción):
        for lugar in collection_lugares.find({"descripción": descripción}):
            print(lugar)
    
    @staticmethod
    def obtener_lugar_por_horario(horario):
        for lugar in collection_lugares.find({"horario": horario}):
            print(lugar)
    
    @staticmethod
    def obtener_lugar_por_visitas(visitas):
        for lugar in collection_lugares.find({"visitas": visitas}):
            print(lugar)

    @staticmethod
    def Eliminar_Lugar_por_id(id):
        collection_lugares.delete_one({"_id": id})
        print(f"Lugar con ID {id} eliminado.")

    @staticmethod
    def Obtener_lugar_por_visitas_mayor(visitas):
        for lugar in collection_lugares.find({"visitas": {"$gt": visitas}}):
            print(lugar)

    @staticmethod
    def Obtener_lugar_por_visitas_menor(visitas):
        for lugar in collection_lugares.find({"visitas": {"$lt": visitas}}):
            print(lugar)

    @staticmethod
    def agregar_comentario_a_lugar(lugar_id, turista_id, comentario_texto):
        comentario = {
            "turista_id": turista_id,
            "texto": comentario_texto
        }
        
        collection_lugares.update_one(
            {"_id": lugar_id},
            {"$push": {"comentarios": comentario}}
        )
        print(f"Comentario añadido al lugar con ID {lugar_id}.")
    
    @staticmethod
    def obtener_Estrellas_Comentarios(lugar_id):
        # Obtiene el lugar por ID
        lugar = collection_lugares.find_one({"_id": lugar_id})
    
        if lugar and "comentarios" in lugar:
            # Analizador de sentimientos usando Transformers
            analizador_sentimientos = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
            
            # Listas de palabras clave
            palabras_buenas = [
                "encantó", "excelente", "fantástico", "maravilloso", "increíble", "bueno", "perfecto", "agradable", "sorprendente", "recomiendo"
            ]

            palabras_malas = [
                "mala", "peor", "terrible", "horrible", "desagradable", "no recomiendo", "queja", "falló", "deficiente", "aburrido"
            ]

            # Procesa cada comentario
            for comentario in lugar["comentarios"]:
                texto = comentario["texto"]
                
                # Análisis de sentimientos usando listas de palabras clave
                conteo_buenas = sum(1 for palabra in palabras_buenas if palabra in texto.lower())
                conteo_malas = sum(1 for palabra in palabras_malas if palabra in texto.lower())

                # Clasificación basada en los conteos
                if conteo_buenas > conteo_malas:
                    sentimiento = "Bueno"
                elif conteo_buenas < conteo_malas:
                    sentimiento = "Malo"
                else:
                    sentimiento = "Normal"
                
                # (Opcional) Análisis de sentimientos usando Transformers
                resultado = analizador_sentimientos(texto)
                label = resultado[0]['label']

                # Comparar resultados de ambos métodos
                print(f"Comentario: '{texto}' - Sentimiento (Transformers): {label}")

        else:
            print(f"No se encontró el lugar con ID {lugar_id} o no tiene comentarios.")

    # @staticmethod
    # def lugar_con_mas_comentarios_positivos():
    #     lugares = collection_lugares.find() 
    #     conteos_positivos = {}

    #     for lugar in lugares:
    #         if "comentarios" in lugar:
    #             conteo_positivo = sum(
    #                 1 for comentario in lugar["comentarios"]
    #                 if any(palabra in comentario["texto"].lower() for palabra in [
    #                     "encantó", "excelente", "fantástico", "maravilloso", "increíble", "bueno", "perfecto", "agradable", "sorprendente", "recomiendo"
    #                 ])
    #             )
    #             conteos_positivos[lugar["_id"]] = conteo_positivo

    #     # Determinar el lugar con el mayor número de comentarios positivos
    #     if conteos_positivos:
    #         lugar_maximo = max(conteos_positivos, key=conteos_positivos.get)
    #         max_comentarios = conteos_positivos[lugar_maximo]
    #         return lugar_maximo, max_comentarios
    #     else:
    #         return None, 0