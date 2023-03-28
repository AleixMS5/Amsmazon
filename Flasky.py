import pymongo
from bson import ObjectId
from flask import Flask, request, app,make_response
from jinja2 import Environment, FileSystemLoader
from markupsafe import escape
from main import  producteAmbId

app = Flask(__name__)
enviroment = Environment(loader=FileSystemLoader("templates/"))


def connectar():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["productes"]
    mycol = mydb["productes"]
    return  mycol


@app.route('/')
def plantilla():
    resultados = []
    template = enviroment.get_template("llistatproductes.html")
    for x in connectar().find().sort([("destacat",pymongo.DESCENDING),("nom",pymongo.ASCENDING)]):
        resultados.append(producteAmbId(
            x.get("_id"), x.get("nom"), x.get("preu"), x.get("descripcio"), x.get("descripciollarga"),
            x.get("destacat"),
            x.get("valoracio"), x.get("imatge"))
        )
    info = {"cataleg": resultados}
    contingut = template.render(info)
    return f'{contingut}'

@app.route('/nom')
def mostrar_productes():
    resultados = []
    template = enviroment.get_template("llistatproductes.html")
    for x in connectar().find().sort([("destacat",pymongo.DESCENDING),("nom",pymongo.ASCENDING)]):
        resultados.append(producteAmbId(
            x.get("_id"), x.get("nom"), x.get("preu"), x.get("descripcio"), x.get("descripciollarga"),
            x.get("destacat"),
            x.get("valoracio"), x.get("imatge"))
        )
    info = {"cataleg": resultados}
    contingut = template.render(info)
    return f'{contingut}'

@app.route('/preuasc')
def mostrar_productes_preuasc():
    resultados = []
    template = enviroment.get_template("llistatproductes.html")
    for x in connectar().find().sort([("destacat",pymongo.DESCENDING),("preu",pymongo.ASCENDING)]):
        resultados.append(producteAmbId(
            x.get("_id"), x.get("nom"), x.get("preu"), x.get("descripcio"), x.get("descripciollarga"),
            x.get("destacat"),
            x.get("valoracio"), x.get("imatge"))
        )
    info = {"cataleg": resultados}
    contingut = template.render(info)
    return f'{contingut}'

@app.route('/preudesc')
def mostrar_productes_preudesc():
    resultados = []
    template = enviroment.get_template("llistatproductes.html")
    for x in connectar().find().sort([("destacat",pymongo.DESCENDING),("preu",pymongo.DESCENDING)]):
        resultados.append(producteAmbId(
            x.get("_id"), x.get("nom"), x.get("preu"), x.get("descripcio"), x.get("descripciollarga"),
            x.get("destacat"),
            x.get("valoracio"), x.get("imatge"))
        )
    info = {"cataleg": resultados}
    contingut = template.render(info)
    return f'{contingut}'
@app.route('/valoracioasc')
def mostrar_productes_valoracioasc():
    resultados = []
    template = enviroment.get_template("llistatproductes.html")
    for x in connectar().find().sort([("destacat",pymongo.DESCENDING),("valoracio",pymongo.ASCENDING)]):
        resultados.append(producteAmbId(
            x.get("_id"), x.get("nom"), x.get("preu"), x.get("descripcio"), x.get("descripciollarga"),
            x.get("destacat"),
            x.get("valoracio"), x.get("imatge"))
        )
    info = {"cataleg": resultados}
    contingut = template.render(info)
    return f'{contingut}'

@app.route('/valoraciodesc')
def mostrar_productes_valoraciodesc():
    resultados = []
    template = enviroment.get_template("llistatproductes.html")
    for x in connectar().find().sort([("destacat",pymongo.DESCENDING),("valoracio",pymongo.DESCENDING)]):
        resultados.append(producteAmbId(
            x.get("_id"), x.get("nom"), x.get("preu"), x.get("descripcio"), x.get("descripciollarga"),
            x.get("destacat"),
            x.get("valoracio"), x.get("imatge"))
        )
    info = {"cataleg": resultados}
    contingut = template.render(info)
    return f'{contingut}'


@app.route('/product/<id>')
def show_product_profile(id):
    template = enviroment.get_template("producte.html")
    # show the user profile for that user
    info =   connectar().find_one({"_id": ObjectId(id)})
    infoa = {"producte": info}
    contingut = template.render(infoa)
    return f'{contingut}'


@app.route('/buscar', methods=['POST'])
def mostrar_segun_texto():
    resultados = []
    palabra = request.form['palabra']
    template = enviroment.get_template("llistatproductes.html")
    query = {
        "$or": [
            {"nom": {"$regex": ".*"+palabra+".*", '$options' : 'i'}},
            {"descripcio": {"$regex": ".*"+palabra+".*" , '$options' : 'i'}}
        ]
    }
    for x in connectar().find(query):
        resultados.append(producteAmbId(
            x.get("_id"), x.get("nom"), x.get("preu"), x.get("descripcio"), x.get("descripciollarga"),
            x.get("destacat"),
            x.get("valoracio"), x.get("imatge"))
        )
    info = {"cataleg": resultados}
    contingut = template.render(info)
    return f'{contingut}'