from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
from function.ConexionDB import collection_turistas, collection_lugares

app = Flask(__name__)
CORS(app)  # Permitir CORS para desarrollo local

# Configurar variables de entorno para MongoDB
os.environ["MONGODB_URI"] = "mongodb+srv://reartefalex:EGkGmPDP4KkkyuIU@cluster0.jg7mg15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

@app.route('/')
def index():
    return "Servidor de Comentarios DB-Turismo funcionando!"

@app.route('/api/comentario', methods=['POST'])
def recibir_comentario():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombre', 'apellido', 'provincia', 'comentario', 'lugar_id', 'lugar_nombre']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo requerido faltante: {field}'}), 400
        
        # Generar ID único para el turista (puedes mejorar esto)
        from bson import ObjectId
        turista_id = str(ObjectId())
        
        # Crear documento del turista
        turista = {
            "_id": turista_id,
            "nombre": data['nombre'],
            "apellido": data['apellido'],
            "provincia": data['provincia'],
            "comentario": data['comentario'],
            "fecha_hora": datetime.now(),
            "lugar_id": data['lugar_id'],
            "lugar_nombre": data['lugar_nombre']
        }
        
        # Insertar turista en la colección de turistas
        collection_turistas.insert_one(turista)
        
        # Crear comentario para el lugar
        comentario_lugar = {
            "turista_id": turista_id,
            "comentario": data['comentario'],
            "fecha_hora": datetime.now(),
            "nombre_turista": f"{data['nombre']} {data['apellido']}",
            "provincia": data['provincia']
        }
        
        # Agregar comentario al lugar
        collection_lugares.update_one(
            {"_id": data['lugar_id']},
            {"$push": {"comentarios": comentario_lugar}}
        )
        
        # Incrementar contador de visitas del lugar
        collection_lugares.update_one(
            {"_id": data['lugar_id']},
            {"$inc": {"visitas": 1}}
        )
        
        print(f"✅ Comentario recibido y guardado:")
        print(f"   Turista: {data['nombre']} {data['apellido']}")
        print(f"   Lugar: {data['lugar_nombre']}")
        print(f"   Comentario: {data['comentario']}")
        
        return jsonify({
            'success': True,
            'message': 'Comentario guardado exitosamente',
            'turista_id': turista_id
        }), 200
        
    except Exception as e:
        print(f"❌ Error al procesar comentario: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/lugares/<int:lugar_id>/comentarios', methods=['GET'])
def obtener_comentarios_lugar(lugar_id):
    try:
        lugar = collection_lugares.find_one({"_id": lugar_id})
        if not lugar:
            return jsonify({'error': 'Lugar no encontrado'}), 404
        
        comentarios = lugar.get('comentarios', [])
        return jsonify({
            'lugar': lugar.get('nombre', 'Sin nombre'),
            'comentarios': comentarios,
            'total': len(comentarios)
        }), 200
        
    except Exception as e:
        print(f"❌ Error al obtener comentarios: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    try:
        # Contar total de turistas
        total_turistas = collection_turistas.count_documents({})
        
        # Contar total de lugares
        total_lugares = collection_lugares.count_documents({})
        
        # Contar total de comentarios
        total_comentarios = collection_turistas.count_documents({"comentario": {"$exists": True, "$ne": ""}})
        
        return jsonify({
            'total_turistas': total_turistas,
            'total_lugares': total_lugares,
            'total_comentarios': total_comentarios
        }), 200
        
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# Servir archivos estáticos para desarrollo
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("🚀 Iniciando servidor de comentarios DB-Turismo...")
    print("📱 API disponible en: http://localhost:5000")
    print("🌐 Página de comentarios: http://localhost:5000/paginawebPlaza/comentarios.html")
    print("📊 Estadísticas: http://localhost:5000/api/estadisticas")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
