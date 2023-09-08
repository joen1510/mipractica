from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from dotenv import load_dotenv
import os
load_dotenv()
user = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASSWORD')
hostname = os.getenv('MONGO_HOSTNAME')

uri = f"mongodb+srv://{user}:{password}@{hostname}/?retryWrites=true&w=majority"

mongo_client = MongoClient(uri, server_api=ServerApi('1'))

consulta = input("Ingrese el nombre del artículo: ")

driver = webdriver.Chrome()
driver.get("https://ec.ebay.com/")
cuadro_busqueda=driver.find_element(by=By.CSS_SELECTOR, value="#gh-ac")
cuadro_busqueda.send_keys(consulta)
time.sleep(2)
boton_busqueda=driver.find_element(by=By.CSS_SELECTOR, value="#gh-btn")
boton_busqueda.click()
fila_p=driver.find_elements(by=By.CSS_SELECTOR, value="#srp-river-results > ul>li")
g=driver.find_elements(by=By.CSS_SELECTOR, value="#cityPoisTable > div > div > table > tbody > tr>td.wind")
time.sleep(2)

for pro in fila_p:
    try:
        precio=pro.find_element(By.CSS_SELECTOR, value="#srp-river-results > ul > li >div > div > div > div > span.s-item__price").text
        estado = pro.find_element(By.CSS_SELECTOR, value="#srp-river-results > ul > li >div > div > div > span.SECONDARY_INFO").text
        nombre=pro.find_element(By.CSS_SELECTOR, value="#srp-river-results > ul > li >div > div > a > div > span").text
        print("Nombre: ",nombre)
        print("Estado: ",estado)
        print("Precio",precio)

        articulo = {
            "Nom_pro": nombre.upper(),
            "Est_pro": estado.upper(),
            "Pre_pro": precio
        }
        db = mongo_client.get_database('Productos')
        collection = db.get_collection(consulta.upper())
        collection.insert_one(articulo)
        print("************************************")
    except Exception as e:
        print("Falla del Sistema",e)
        print("eeeeeeeeeeeerroooooooooooooorrrrrrrrrrrrrrrrrrr")
driver.close()
print("Información almacenada con exito en la Base de Datos")