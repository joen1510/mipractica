from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# flask.ext.pymongo import Pymongo
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
load_dotenv()
user = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASSWORD')
hostname = os.getenv('MONGO_HOSTNAME')

uri = f"mongodb+srv://{user}:{password}@{hostname}/?retryWrites=true&w=majority"

mongo_client = MongoClient(uri, server_api=ServerApi('1'))
#print(mongo_client.list_database_names())
base=mongo_client['Pronosticos_tiempo']
ciudad=base['CUENCA']
print(ciudad.find())
app = Flask(__name__)
app.config['MONGO_URI']=uri
app.config['MONGO_DBNAME']="Pronosticos_tiempo"
#mong=Pymongo(app)
mongo=PyMongo(app)
print(mongo.db)
@app.route("/")
def hello():

    return f""

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='127.0.0.1', port=3000, debug=True)