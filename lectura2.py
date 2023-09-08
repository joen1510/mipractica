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

base=mongo_client['Productos']

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
pdf.set_font('Arial','B',16)
pdf.set_text_color(60,99,234)
pdf.text(x=10,y=10, txt=f"REPORTE DEL PRODUCTO \"{b[op-1]}\"")
f=15
nu=1
hoja=1
for documentos in ciudad.find({}):
    try:
        hoja += 1
        print("articulo--> ", hoja)
        print("Nombre", documentos["Nom_pro"])
        print("Estado:",documentos["Est_pro"])
        print("Precio:", documentos["Pre_pro"])
        print("*************************************************")
        #pdf.text(x=17, y=20, txt="No")
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(159, 35, 60)
        pdf.text(x=17, y=f+8, txt="Artículo:")
        pdf.text(x=17, y=f+13, txt="Estado :")
        pdf.text(x=17, y=f+18, txt="Precio  :")
        pdf.set_font('Arial', '', 8)
        pdf.set_text_color(0, 0, 0)
        pdf.text(x=10, y=f+12, txt=str(nu))
        pdf.text(x=38, y=f+8, txt=documentos["Nom_pro"].encode('latin-1', 'replace').decode('latin-1'))
        pdf.text(x=38, y=f+13, txt=documentos["Est_pro"])
        pdf.text(x=38, y=f+18, txt=documentos["Pre_pro"])
        pdf.line(10,f+2,200,f+2)
        f+=18
        nu+=1
        if (hoja == 15):
            pdf.add_page()
            hoja = 0
            f = 15
    except Exception as e:
        print("Falla del Sistema",e)
        print("eeeeeeeeeeeerroooooooooooooorrrrrrrrrrrrrrrrrrr")
print("Total de datos cargados: ",ciudad.count_documents({}))
pdf.output(f"Reportes/REPORTE_{b[op-1]}_JS.pdf")
pdf.output(f"Reportes/general.pdf")
