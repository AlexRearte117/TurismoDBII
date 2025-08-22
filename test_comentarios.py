#!/usr/bin/env python3
"""
Script de prueba para el sistema de comentarios DB-Turismo
"""

import requests
import json

def test_api_comentarios():
    """Prueba la API de comentarios"""
    
    # URL base del servidor
    base_url = "http://localhost:5000"
    
    print("🧪 Probando API de comentarios...")
    print("=" * 50)
    
    # 1. Probar endpoint principal
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Endpoint principal: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error en endpoint principal: {e}")
        return
    
    # 2. Probar envío de comentario
    comentario_test = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "provincia": "Buenos Aires",
        "comentario": "¡Me encantó la Plaza Principal! Es un lugar hermoso para visitar.",
        "lugar_id": 1,
        "lugar_nombre": "Plaza Principal"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/comentario",
            json=comentario_test,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Comentario enviado exitosamente:")
            print(f"   Turista ID: {data.get('turista_id')}")
            print(f"   Mensaje: {data.get('message')}")
        else:
            print(f"❌ Error al enviar comentario: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error al enviar comentario: {e}")
    
    # 3. Probar obtención de comentarios del lugar
    try:
        response = requests.get(f"{base_url}/api/lugares/1/comentarios")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Comentarios del lugar obtenidos:")
            print(f"   Lugar: {data.get('lugar')}")
            print(f"   Total comentarios: {data.get('total')}")
            
            comentarios = data.get('comentarios', [])
            for i, comentario in enumerate(comentarios):
                print(f"   Comentario {i+1}: {comentario.get('comentario', 'N/A')}")
        else:
            print(f"❌ Error al obtener comentarios: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al obtener comentarios: {e}")
    
    # 4. Probar estadísticas
    try:
        response = requests.get(f"{base_url}/api/estadisticas")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Estadísticas obtenidas:")
            print(f"   Total turistas: {data.get('total_turistas')}")
            print(f"   Total lugares: {data.get('total_lugares')}")
            print(f"   Total comentarios: {data.get('total_comentarios')}")
        else:
            print(f"❌ Error al obtener estadísticas: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas completadas!")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del sistema de comentarios...")
    print("⚠️  Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
    print()
    
    test_api_comentarios()
