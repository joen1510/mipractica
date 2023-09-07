from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fpdf import FPDF
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pandas as pd
from mondconec import mongo
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

b=[]
c=0
print("Pronósticos del Tiempo ")
for bc in base.list_collection_names():
    c+=1
    print(f"{c} .- {bc}")
    b.append(bc)
op=int(input("Ecoja una opción: "))
print("Elejiste",b[op-1])
ciudad=base[b[op-1]]
pdf=FPDF(orientation='P', unit='mm', format='A4')
pdf.set_title(title=f"Reporte de {b[op-1]}")
pdf.set_author(author="Ing. Jonathan Sanmartin")
pdf.set_subject(subject="Proyecto de Tratamiento de datos")
pdf.add_page()
pdf.set_font('Arial','',5)
pdf.text(x=190,y=2, txt="Jonathan Sanmartin")
pdf.set_font('Arial','B',18)
pdf.set_text_color(60,99,234)
pdf.text(x=15,y=10, txt=f"REPORTE DEL CLIMA DE LA CIUDAD DE \"{b[op-1]}\"")
pdf.set_font('Arial','B',14)
pdf.set_text_color(159,35,60)
pdf.text(x=25,y=20, txt="No")
pdf.text(x=40,y=20, txt="Fecha")
pdf.text(x=67,y=20, txt="Temp_Máxima")
pdf.text(x=105,y=20, txt="Temp_Minima")
pdf.text(x=145,y=20, txt="Velocidad")
pdf.set_font('Arial','',10)
f=25
nu=1
pdf.set_text_color(0,0,0)
for documentos in ciudad.find({}):
    print("Ciudad:", documentos["Ciudad"])
    print("Fecha:",documentos["Fecha"])
    print("Temperatura Maxima:", documentos["Temperatutas"]["Temp_Max"])
    print("Temperatura Minima:", documentos["Temperatutas"]["Temp_Min"])
    print("Velocidad del Viento:",documentos["Temperatutas"]["vel_viento"])
    print("*************************************************")
    pdf.text(x=25, y=f, txt=str(nu))
    pdf.text(x=40, y=f, txt=documentos["Fecha"])
    pdf.text(x=80, y=f, txt=documentos["Temperatutas"]["Temp_Max"])
    pdf.text(x=118, y=f, txt=documentos["Temperatutas"]["Temp_Min"])
    pdf.text(x=150, y=f, txt=documentos["Temperatutas"]["vel_viento"])
    pdf.line(25,f+2.5,170,f+2.5)
    f+=8
    nu+=1
print("Total de datos cargados: ",ciudad.count_documents({}))
pdf.output(f"Reportes/REPORTE_{b[op-1]}_JS.pdf")
pdf.output(f"Reportes/general.pdf")
