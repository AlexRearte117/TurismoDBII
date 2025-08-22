#!/usr/bin/env python3
"""
Script para verificar que los comentarios se estén guardando correctamente
"""

import os
from function.ConexionDB import collection_turistas, collection_lugares

# Configurar variables de entorno para MongoDB
os.environ["MONGODB_URI"] = "mongodb+srv://reartefalex:EGkGmPDP4KkkyuIU@cluster0.jg7mg15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def verificar_colecciones():
    """Verifica el estado de las colecciones"""
    print("🔍 VERIFICANDO ESTADO DE LAS COLECCIONES")
    print("=" * 60)
    
    # Verificar colección de turistas
    total_turistas = collection_turistas.count_documents({})
    turistas_con_comentarios = collection_turistas.count_documents({
        "comentario": {"$exists": True, "$ne": ""}
    })
    
    print(f"📊 COLECCIÓN TURISTAS:")
    print(f"   Total de documentos: {total_turistas}")
    print(f"   Turistas con comentarios: {turistas_con_comentarios}")
    
    # Verificar colección de lugares
    total_lugares = collection_lugares.count_documents({})
    lugares_con_comentarios = collection_lugares.count_documents({
        "comentarios": {"$exists": True, "$ne": []}
    })
    
    print(f"\n📊 COLECCIÓN LUGARES:")
    print(f"   Total de documentos: {total_lugares}")
    print(f"   Lugares con comentarios: {lugares_con_comentarios}")
    
    return total_turistas, turistas_con_comentarios

def mostrar_ultimos_turistas():
    """Muestra los últimos turistas agregados"""
    print("\n👥 ÚLTIMOS TURISTAS AGREGADOS:")
    print("=" * 60)
    
    # Obtener los últimos 5 turistas
    ultimos_turistas = list(collection_turistas.find().sort("_id", -1).limit(5))
    
    if not ultimos_turistas:
        print("❌ No hay turistas en la base de datos")
        return
    
    for i, turista in enumerate(ultimos_turistas, 1):
        print(f"\n👤 TURISTA #{i}")
        print(f"   ID: {turista.get('_id', 'N/A')}")
        print(f"   Nombre: {turista.get('nombre', 'N/A')} {turista.get('apellido', 'N/A')}")
        print(f"   Provincia: {turista.get('provincia', 'N/A')}")
        print(f"   Comentario: {turista.get('comentario', 'Sin comentario')}")
        print(f"   Lugar: {turista.get('lugar_nombre', 'Sin lugar')}")
        print(f"   Fecha: {turista.get('fecha_hora', 'Sin fecha')}")

def mostrar_estructura_turista():
    """Muestra la estructura de un documento de turista"""
    print("\n🏗️ ESTRUCTURA DE UN DOCUMENTO TURISTA:")
    print("=" * 60)
    
    turista = collection_turistas.find_one()
    if turista:
        print("Campos disponibles:")
        for campo, valor in turista.items():
            print(f"   • {campo}: {valor}")
    else:
        print("❌ No hay turistas para mostrar estructura")

def crear_turista_prueba():
    """Crea un turista de prueba para verificar que funciona"""
    print("\n🧪 CREANDO TURISTA DE PRUEBA:")
    print("=" * 60)
    
    from datetime import datetime
    from bson import ObjectId
    
    turista_prueba = {
        "_id": str(ObjectId()),
        "nombre": "Usuario",
        "apellido": "Prueba",
        "provincia": "La Rioja",
        "comentario": "Este es un comentario de prueba para verificar el sistema",
        "fecha_hora": datetime.now(),
        "lugar_id": 1,
        "lugar_nombre": "Plaza Principal"
    }
    
    try:
        resultado = collection_turistas.insert_one(turista_prueba)
        print(f"✅ Turista de prueba creado exitosamente")
        print(f"   ID: {resultado.inserted_id}")
        print(f"   Nombre: {turista_prueba['nombre']} {turista_prueba['apellido']}")
        print(f"   Comentario: {turista_prueba['comentario']}")
        return True
    except Exception as e:
        print(f"❌ Error al crear turista de prueba: {e}")
        return False

def main():
    print("🚀 VERIFICADOR DE SISTEMA DE COMENTARIOS")
    print("=" * 80)
    
    # 1. Verificar estado de las colecciones
    total_turistas, turistas_con_comentarios = verificar_colecciones()
    
    # 2. Mostrar estructura de un turista
    mostrar_estructura_turista()
    
    # 3. Mostrar últimos turistas
    mostrar_ultimos_turistas()
    
    # 4. Si no hay turistas, crear uno de prueba
    if total_turistas == 0:
        print("\n⚠️ No hay turistas en la base de datos. Creando uno de prueba...")
        if crear_turista_prueba():
            print("\n🔄 Verificando nuevamente después de crear turista de prueba...")
            verificar_colecciones()
            mostrar_ultimos_turistas()
    
    print("\n" + "=" * 80)
    print("🏁 Verificación completada!")
    
    if turistas_con_comentarios > 0:
        print(f"✅ El sistema está funcionando. Hay {turistas_con_comentarios} turistas con comentarios.")
    else:
        print("⚠️ No hay turistas con comentarios. Verifica que el formulario web esté funcionando.")

if __name__ == "__main__":
    main()
