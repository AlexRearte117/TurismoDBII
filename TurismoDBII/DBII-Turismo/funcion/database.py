from pymongo import MongoClient

client = MongoClient("")
db = client['Turismo']
collection_turistas = db['turista']

