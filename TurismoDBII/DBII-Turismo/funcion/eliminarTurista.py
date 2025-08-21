from database import collection_turistas

collection_turistas.delete_one({"ID": 11})
print("Turista eliminado")

for turistas in collection_turistas.find():
    print(turistas)