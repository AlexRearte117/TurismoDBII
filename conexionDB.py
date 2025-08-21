from pymongo import MongoClient
#URL de MongoDB
client = MongoClient("mongodb+srv://reartefalex:<EGkGmPDP4KkkyuIU>@cluster0.jg7mg15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#Seleccionar la db
db = client['Turismo']
#Seleccionar la colección
collection_turistas = db['turista']
collection_lugares = db['lugar']