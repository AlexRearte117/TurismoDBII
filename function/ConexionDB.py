from pymongo import MongoClient
from urllib.parse import quote_plus
import os

#mongodb.com		a13x8520/ff			EGkGmPDP4KkkyuIU
#mongosh "mongodb+srv://cluster0.jg7mg15.mongodb.net/" --apiVersion 1 --username reartefalex
#pasword: EGkGmPDP4KkkyuIU

# Preferir variables de entorno para credenciales
# Opción 1: MONGODB_URI (cadena completa)
# Opción 2: MONGODB_USER, MONGODB_PASS, MONGODB_CLUSTER

mongodb_uri = os.getenv("MONGODB_URI")

if not mongodb_uri:
	username = os.getenv("MONGODB_USER")
	password = os.getenv("MONGODB_PASS")
	cluster = os.getenv("MONGODB_CLUSTER")  # p.ej.: cluster0.dffoict.mongodb.net
	if username and password and cluster:
		mongodb_uri = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@{cluster}/?retryWrites=true&w=majority"
	

client = MongoClient(mongodb_uri)

# Validar conexión con ping (levanta excepción si hay credenciales o red incorrecta)
try:
	client.admin.command('ping')
except Exception as exc:
	raise RuntimeError(f"No se pudo conectar a MongoDB: {exc}")

# Seleccionar la base de datos y colecciones
db = client['Turismo']
collection_turistas = db['turista']
collection_lugares = db['lugar']