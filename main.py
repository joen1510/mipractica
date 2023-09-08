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

consulta = input("Ingrese el nombre de la ciudad: ")

driver = webdriver.Chrome()
driver.get("https://www.eltiempo.es/")
aceptar_button = driver.find_element(by=By.CSS_SELECTOR, value="#didomi-notice-agree-button")
aceptar_button.click()
#cuadro_busqueda=driver.find_element(by=By.CSS_SELECTOR, value="input#term")
cuadro_busqueda=driver.find_element(by=By.XPATH, value='/html/body/header/nav/div[1]/div[2]/div/form/input')
cuadro_busqueda.click()
time.sleep(10)
cuadro_busqueda.send_keys(consulta)
cuadro_busqueda.click()
time.sleep(2)
boton_busqueda=driver.find_element(by=By.CSS_SELECTOR, value="#search > form > label > button > i")
boton_busqueda.click()
seleccionar=driver.find_element(by=By.CSS_SELECTOR, value="#main > div.-t-xs-6.section_search-results > div > section:nth-child(2) > div.col-12.col-md-8.m_list_block.m_search > div > ul > li:nth-child(1) > a > strong")
seleccionar.click()
time.sleep(3)
fila_p=driver.find_elements(by=By.CSS_SELECTOR, value="#cityPoisTable > div > div > table > thead > tr > th")
g=driver.find_elements(by=By.CSS_SELECTOR, value="#cityPoisTable > div > div > table > tbody > tr>td.wind")
time.sleep(5)
c=0
viento=[]
for card in g:
    c+=1
    kilo = card.find_element(By.CSS_SELECTOR, value="p.velocity").text
    viento.append(card.find_element(By.CSS_SELECTOR, value="p.velocity").text)
    print("velocidad:", str(card.find_element(By.CSS_SELECTOR, value="p.velocity").text))
print(viento)
c=0
for ca in fila_p:
    try:
        fecha = ca.find_element(By.CSS_SELECTOR, value="#cityPoisTable > div > div > table > thead > tr > th > div.datetime").text
        tmax= ca.find_element(By.CSS_SELECTOR, value="#cityPoisTable > div > div > table > thead > tr > th > div.text-poppins-medium.header-max-min > div.max-temperature").text
        tmin = ca.find_element(By.CSS_SELECTOR,value="#cityPoisTable > div > div > table > thead > tr > th > div.text-poppins-medium.header-max-min > div.min-temperature").text
        vel_viento=viento[c]
        print(f"Fecha= {fecha}")
        print(f"Temperatura maxima= {tmax}")
        print(f"Temperatura minima= {tmin}")
        print(f"{c} Velocidad del viento= {vel_viento}")
        print("----------------")
        c += 1

        tiempo = {
            "Ciudad": consulta.upper(),
            "Fecha": fecha,
            "Temperatutas": {
                "Temp_Max": tmax,
                "Temp_Min": tmin,
                "vel_viento": vel_viento,
            }
        }
        db = mongo_client.get_database('Pronosticos_tiempo')
        collection = db.get_collection(consulta.upper())
        collection.insert_one(tiempo)
        #print(tiempo)

    except Exception as e:
        print("Falla del Sistema",e)
        print("erorrrrrrrrrrrrrrrrrrrrrrrrrrr")
time.sleep(4)
driver.close()
print("Información almacenada con exito en la Base de Datos")