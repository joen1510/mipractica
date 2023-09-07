from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://jonapapi86:9qQfgKwNZtSJTfmE@cluster0.q111vzh.mongodb.net/?retryWrites=true&w=majority'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["Pronosticos_tiempo"]
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db