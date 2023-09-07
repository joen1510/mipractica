from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from ciudad import Ciudad
import subprocess
from report import reportes
db = dbase.dbConnection()

app = Flask(__name__)

#Rutas de la aplicación
"""@app.route('/')
def home():
    products = db['CUENCA']
    productsReceived = products.find()
    return render_template('index.html', ciudad = productsReceived, nomb='CUENCA', tot=products.count_documents({}))
"""
@app.route('/')
def home():
    lb = db.list_collection_names()
    return render_template('index.html', listadb=lb)
#Method Post

@app.route('/llamar',methods=['POST'])
def llamar():
    env = request.form['enviar']
    products = db[env.upper()]
    reportes(products,env.upper())
    productsReceived = products.find()
    return render_template('consulta.html', ciudad = productsReceived,nom_ciu=env,tot=products.count_documents({}))

@app.route('/generar',methods=['POST'])
def generar():
    path = f'Reportes\general.pdf'
    subprocess.Popen([path], shell=True)
    return "<h2>Reporte Generado!</h2>"


@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4000)