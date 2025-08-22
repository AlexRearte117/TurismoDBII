#!/usr/bin/env python3
"""
Script para mostrar qué turista visitó qué lugar con su comentario
"""

import os
from function.ConexionDB import collection_turistas, collection_lugares

# Configurar variables de entorno para MongoDB
os.environ["MONGODB_URI"] = "mongodb+srv://reartefalex:EGkGmPDP4KkkyuIU@cluster0.jg7mg15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def mostrar_turistas_vs_lugares():
    """Muestra qué turista visitó qué lugar con su comentario"""
    print("🗺️ REPORTE: TURISTAS VS LUGARES VISITADOS")
    print("=" * 80)
    
    # Buscar todos los turistas que tienen comentarios
    turistas_con_comentarios = collection_turistas.find({
        "comentario": {"$exists": True, "$ne": ""}
    }).sort("fecha_hora", -1)  # Ordenar por fecha más reciente
    
    turistas_lista = list(turistas_con_comentarios)
    
    if not turistas_lista:
        print("❌ No hay turistas con comentarios registrados.")
        print("\n💡 Posibles causas:")
        print("   • El formulario web no se ha usado aún")
        print("   • El servidor Flask no está ejecutándose")
        print("   • Hay un problema de conexión con MongoDB")
        print("   • Los comentarios se están guardando en otra colección")
        return 0
    
    print(f"✅ Se encontraron {len(turistas_lista)} turistas con comentarios\n")
    
    # Mostrar cada turista y su visita
    for i, turista in enumerate(turistas_lista, 1):
        print(f"👤 VISITA #{i}")
        print(f"   🏛️ LUGAR: {turista.get('lugar_nombre', 'Sin especificar')}")
        print(f"   👨‍💼 TURISTA: {turista.get('nombre', 'N/A')} {turista.get('apellido', 'N/A')}")
        print(f"   🏠 PROVINCIA: {turista.get('provincia', 'N/A')}")
        print(f"   💬 COMENTARIO: '{turista.get('comentario', 'Sin comentario')}'")
        print(f"   🗓️ FECHA: {turista.get('fecha_hora', 'Sin fecha')}")
        print(f"   🆔 ID: {turista.get('_id', 'N/A')}")
        print("-" * 70)
    
    # Resumen por lugar
    print("\n📊 RESUMEN POR LUGAR:")
    print("=" * 40)
    
    lugares_contador = {}
    for turista in turistas_lista:
        lugar = turista.get('lugar_nombre', 'Desconocido')
        if lugar not in lugares_contador:
            lugares_contador[lugar] = 0
        lugares_contador[lugar] += 1
    
    for lugar, cantidad in lugares_contador.items():
        print(f"   🏛️ {lugar}: {cantidad} visitas")
    
    # Resumen por provincia
    print("\n🌍 RESUMEN POR PROVINCIA:")
    print("=" * 40)
    
    provincias_contador = {}
    for turista in turistas_lista:
        provincia = turista.get('provincia', 'Desconocida')
        if provincia not in provincias_contador:
            provincias_contador[provincia] = 0
        provincias_contador[provincia] += 1
    
    for provincia, cantidad in provincias_contador.items():
        print(f"   🏠 {provincia}: {cantidad} turistas")
    
    return len(turistas_lista)

def mostrar_estadisticas_detalladas():
    """Muestra estadísticas detalladas del sistema"""
    print("\n📈 ESTADÍSTICAS DETALLADAS")
    print("=" * 50)
    
    # Total de turistas
    total_turistas = collection_turistas.count_documents({})
    turistas_con_comentarios = collection_turistas.count_documents({
        "comentario": {"$exists": True, "$ne": ""}
    })
    
    # Total de lugares
    total_lugares = collection_lugares.count_documents({})
    
    print(f"👥 Total de turistas en BD: {total_turistas}")
    print(f"💬 Turistas con comentarios: {turistas_con_comentarios}")
    print(f"🏛️ Total de lugares: {total_lugares}")
    
    if total_turistas > 0:
        porcentaje_con_comentarios = (turistas_con_comentarios / total_turistas) * 100
        print(f"📊 Porcentaje con comentarios: {porcentaje_con_comentarios:.1f}%")
    
    # Verificar si hay turistas sin comentarios
    turistas_sin_comentarios = total_turistas - turistas_con_comentarios
    if turistas_sin_comentarios > 0:
        print(f"⚠️ Turistas sin comentarios: {turistas_sin_comentarios}")

def main():
    print("🚀 SISTEMA DE VISITAS TURÍSTICAS - REPORTE COMPLETO")
    print("=" * 80)
    
    # Mostrar turistas vs lugares
    total_visitas = mostrar_turistas_vs_lugares()
    
    # Mostrar estadísticas
    mostrar_estadisticas_detalladas()
    
    print("\n" + "=" * 80)
    if total_visitas > 0:
        print(f"✅ Sistema funcionando correctamente. {total_visitas} visitas registradas.")
    else:
        print("⚠️ No hay visitas registradas. Verifica:")
        print("   1. Que el servidor Flask esté ejecutándose")
        print("   2. Que hayas usado el formulario web")
        print("   3. Que la conexión a MongoDB funcione")
        print("   4. Ejecuta: python verificar_comentarios.py")

if __name__ == "__main__":
    main()
