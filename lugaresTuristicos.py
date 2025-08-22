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
    def editar_comentario_a_lugar(lugar_id, comentario_id, comentario_texto):
        collection_lugares.update_one(
            {"_id": lugar_id, "comentarios.turista_id": comentario_id},
            {"$set": {"comentarios.$.comentario": comentario_texto}}
        )
        print(f"Comentario {comentario_id} editado en el lugar con ID {lugar_id}.")

    @staticmethod
    def agregar_comentario_a_lugar(lugar_id, turista_id, comentario_texto):
        comentario = {
            "turista_id": turista_id,
            "comentario": comentario_texto
        }
        
        collection_lugares.update_one(
            {"_id": lugar_id},
            {"$push": {"comentarios": comentario}}
        )
        print(f"Comentario añadido al lugar con ID {lugar_id}.")
    
    @staticmethod
    def diagnosticar_comentarios(lugar_id):
        """Método de diagnóstico para ver la estructura de los comentarios"""
        lugar = collection_lugares.find_one({"_id": lugar_id})
        
        if not lugar:
            print(f"No se encontró el lugar con ID {lugar_id}")
            return
            
        print(f"📋 DIAGNÓSTICO DEL LUGAR {lugar_id}:")
        print(f"Nombre: {lugar.get('nombre', 'N/A')}")
        print(f"Campos disponibles: {list(lugar.keys())}")
        
        if "comentarios" in lugar:
            comentarios = lugar["comentarios"]
            print(f"Total de comentarios: {len(comentarios)}")
            print(f"Tipo de comentarios: {type(comentarios)}")
            
            for i, comentario in enumerate(comentarios):
                print(f"\nComentario {i}:")
                print(f"  Tipo: {type(comentario)}")
                print(f"  Contenido: {comentario}")
                if isinstance(comentario, dict):
                    print(f"  Claves: {list(comentario.keys())}")
        else:
            print("No hay campo 'comentarios' en este lugar")
            
        print("-" * 50)

    @staticmethod
    def obtener_Estrellas_Comentarios(lugar_id):
        """Método simplificado para análisis de sentimientos sin transformers"""
        lugar = collection_lugares.find_one({"_id": lugar_id})
    
        if lugar and "comentarios" in lugar:
            # Listas de palabras clave
            palabras_buenas = [
                "encantó", "excelente", "fantástico", "maravilloso", "increíble", "bueno", "perfecto", "agradable", "sorprendente", "recomiendo", "gusto", "me gustó"
            ]

            palabras_malas = [
                "mala", "peor", "terrible", "horrible", "desagradable", "no recomiendo", "queja", "falló", "deficiente", "aburrido", "malo", "pésimo"
            ]

            sentimientos_palabras = []
            puntuaciones_manuales = []

            print(f"🔍 ANÁLISIS DE COMENTARIOS - LUGAR {lugar_id}: {lugar.get('nombre', 'Sin nombre')}")
            print("=" * 60)

            # Procesa cada comentario
            for i, comentario in enumerate(lugar["comentarios"]):
                # Extraer texto del comentario
                if isinstance(comentario, dict):
                    if "texto" in comentario:
                        texto = comentario["texto"]
                    elif "comentario" in comentario:
                        texto = comentario["comentario"]
                    else:
                        texto = str(comentario)
                else:
                    texto = str(comentario)
                
                # Análisis de sentimientos usando palabras clave
                texto_lower = texto.lower()
                conteo_buenas = sum(1 for palabra in palabras_buenas if palabra in texto_lower)
                conteo_malas = sum(1 for palabra in palabras_malas if palabra in texto_lower)

                # Clasificación basada en los conteos
                if conteo_buenas > conteo_malas:
                    sentimiento = "Bueno"
                    estrellas = 4 + min(conteo_buenas, 2)  # 4-6 estrellas
                elif conteo_buenas < conteo_malas:
                    sentimiento = "Malo"
                    estrellas = 1 + max(0, 2 - conteo_malas)  # 1-3 estrellas
                else:
                    sentimiento = "Normal"
                    estrellas = 3  # 3 estrellas neutral
                
                sentimientos_palabras.append(sentimiento)
                puntuaciones_manuales.append(estrellas)
                
                # Mostrar resultados
                print(f"💬 Comentario {i+1}: '{texto}'")
                print(f"   📊 Sentimiento: {sentimiento}")
                print(f"   ⭐ Estrellas: {estrellas}")
                print(f"   🔍 Palabras buenas: {conteo_buenas}, Palabras malas: {conteo_malas}")
                print("-" * 40)

            # Calcular estadísticas generales
            if puntuaciones_manuales:
                promedio_estrellas = sum(puntuaciones_manuales) / len(puntuaciones_manuales)
                print(f"\n📊 RESUMEN FINAL DEL LUGAR {lugar_id}:")
                print(f"  🎯 Total de comentarios: {len(lugar['comentarios'])}")
                print(f"  ⭐ Promedio de estrellas: {promedio_estrellas:.1f}")
                print(f"  😊 Sentimientos:")
                print(f"     * Buenos: {sentimientos_palabras.count('Bueno')}")
                print(f"     * Normales: {sentimientos_palabras.count('Normal')}")
                print(f"     * Malos: {sentimientos_palabras.count('Malo')}")
                
                return promedio_estrellas, len(lugar['comentarios'])
            else:
                print("❌ No se pudieron procesar las puntuaciones.")
                return 0, 0

        else:
            print(f"❌ No se encontró el lugar con ID {lugar_id} o no tiene comentarios.")
            return 0, 0

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