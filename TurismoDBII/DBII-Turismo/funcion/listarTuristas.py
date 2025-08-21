from database import collection_turistas

for turista in collection_turistas.find():
    print(turista)