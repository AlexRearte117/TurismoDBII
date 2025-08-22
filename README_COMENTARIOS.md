# 🗺️ Sistema de Comentarios DB-Turismo

Sistema completo para gestionar comentarios de turistas en lugares turísticos, integrado con MongoDB.

## 🚀 Características

- ✅ **Formulario web** para ingresar comentarios
- ✅ **API REST** para procesar comentarios
- ✅ **Integración con MongoDB** para almacenamiento
- ✅ **Sistema de análisis** de sentimientos
- ✅ **Estadísticas en tiempo real**
- ✅ **Interfaz responsive** y moderna

## 📁 Estructura del Proyecto

```
DB-Turismo/
├── paginawebPlaza/
│   ├── plaza.html          # Página principal de la plaza
│   ├── comentarios.html    # Formulario de comentarios
│   └── page.css            # Estilos CSS
├── servidor_comentarios.py # Servidor Flask backend
├── test_comentarios.py     # Script de pruebas
├── requirements.txt        # Dependencias Python
└── function/
    └── ConexionDB.py      # Conexión a MongoDB
```

## 🛠️ Instalación

### 1. Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### 2. Configurar MongoDB
Asegúrate de que las credenciales en `function/ConexionDB.py` sean correctas.

### 3. Iniciar el servidor
```bash
python servidor_comentarios.py
```

## 🌐 Uso del Sistema

### Página Principal
- **URL**: `http://localhost:5000/paginawebPlaza/plaza.html`
- **Funcionalidad**: Información sobre la Plaza Principal con botón para comentarios

### Formulario de Comentarios
- **URL**: `http://localhost:5000/paginawebPlaza/comentarios.html`
- **Campos**:
  - Nombre
  - Apellido
  - Provincia
  - Comentario
- **Funcionalidad**: Envía comentarios a la base de datos

## 🔌 API Endpoints

### POST `/api/comentario`
Recibe y procesa nuevos comentarios.

**Body JSON:**
```json
{
    "nombre": "Juan",
    "apellido": "Pérez",
    "provincia": "Buenos Aires",
    "comentario": "¡Me encantó el lugar!",
    "lugar_id": 1,
    "lugar_nombre": "Plaza Principal"
}
```

### GET `/api/lugares/<id>/comentarios`
Obtiene todos los comentarios de un lugar específico.

### GET `/api/estadisticas`
Obtiene estadísticas generales del sistema.

## 🧪 Pruebas

### Ejecutar pruebas automáticas
```bash
python test_comentarios.py
```

### Pruebas manuales
1. Abrir `http://localhost:5000` en el navegador
2. Navegar a la página de comentarios
3. Llenar y enviar el formulario
4. Verificar en la base de datos

## 📊 Base de Datos

### Colección `turistas`
```json
{
    "_id": "ObjectId",
    "nombre": "Juan",
    "apellido": "Pérez",
    "provincia": "Buenos Aires",
    "comentario": "¡Me encantó el lugar!",
    "fecha_hora": "2024-01-01T12:00:00Z",
    "lugar_id": 1,
    "lugar_nombre": "Plaza Principal"
}
```

### Colección `lugares`
```json
{
    "_id": 1,
    "nombre": "Plaza Principal",
    "comentarios": [
        {
            "turista_id": "ObjectId",
            "comentario": "¡Me encantó el lugar!",
            "fecha_hora": "2024-01-01T12:00:00Z",
            "nombre_turista": "Juan Pérez",
            "provincia": "Buenos Aires"
        }
    ],
    "visitas": 1
}
```

## 🔧 Personalización

### Cambiar lugar turístico
1. Modificar `lugar_id` y `lugar_nombre` en `comentarios.html`
2. Actualizar el título y descripción de la página
3. Ajustar el ID en el servidor si es necesario

### Agregar nuevos campos
1. Modificar el formulario HTML
2. Actualizar el endpoint `/api/comentario`
3. Ajustar la estructura de la base de datos

## 🚨 Solución de Problemas

### Error de conexión MongoDB
- Verificar credenciales en `function/ConexionDB.py`
- Comprobar que el clúster esté activo
- Verificar permisos del usuario

### Error CORS
- El servidor ya incluye CORS habilitado
- Si persiste, verificar configuración del navegador

### Formulario no envía
- Verificar que el servidor esté ejecutándose
- Comprobar la consola del navegador para errores
- Verificar que la URL de la API sea correcta

## 📱 Tecnologías Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask
- **Base de Datos**: MongoDB
- **APIs**: REST API
- **Estilos**: CSS personalizado con diseño responsive

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

**Desarrollado para DB-Turismo - Sistema de Gestión de Turistas y Lugares Turísticos**
