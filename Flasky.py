import pymongo
from bson import ObjectId
from flask import Flask, request, app, make_response, redirect, url_for
from jinja2 import Environment, FileSystemLoader
from markupsafe import escape
import component1 as c
import comanda
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


@app.route('/about')
def about():
    resultados = []

    template = enviroment.get_template("about.html")
    contingut = template.render()
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
@app.route('/carrito')
def mostrar_carrito():
    resultados = []

    template = enviroment.get_template("carrito.html")
    resultados=c.getall("comandes.bin")
    pepe = 0
    for result in resultados:
        pepe = pepe + (float(result.price) * float(result.quantity))

    info = {"carrito": resultados,"total":pepe}
    contingut = template.render(info)
    return f'{contingut}'

@app.route('/carrito' , methods=['POST'])
def mostrar_carrito_update():
    resultados = []
    resultados = c.getall("comandes.bin")

    quantity = request.form['tentacles']
    precio=0
    producto = request.form['product']
    for resultado in resultados:
        if resultado.id == producto:
            precio = resultado.price

    c1 = comanda.comanda(producto, quantity, precio)
    c.updateObject("comandes.bin", producto, c1)



    return redirect(url_for("mostrar_carrito"))

@app.route('/carrito/<id>')
def mostrar_carrito_borrar(id):
    c.deleteObject("comandes.bin",id)
    return redirect(url_for("mostrar_carrito"))


@app.route('/borrar/<id>')
def carrito_borrar_producte(id):
    c.deleteObject("comandes.bin",id)
    return redirect(url_for("mostrar_productes_preuasc"))
@app.route('/delete')
def mostrar_carrito_borrarall():
    c.deleteFitxer("comandes.bin")
    return redirect(url_for("mostrar_carrito"))
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
    comanda=c.restoreobject(id,"comandes.bin")
    infoa = {"producte": info,"comanda":comanda}

    contingut = template.render(infoa)
    return f'{contingut}'

@app.route('/product/<id>', methods=['POST'])
def añadir_carrito(id):

    info = connectar().find_one({"_id": ObjectId(id)})

    template = enviroment.get_template("producte.html")
    quantity = request.form['tentacles']
    precio= str(info.get('preu'))
    producto = str(id)

    c1 = comanda.comanda(producto, quantity, precio)
    if (c.restoreobject(producto,"comandes.bin")==None):
        c.saveobject(c1, "comandes.bin")
        print(quantity+" "+precio+" "+producto)
    else:
        c.updateObject("comandes.bin",producto,c1)
    comandas = c.restoreobject(id, "comandes.bin")
    # show the user profile for that user

    infoa = {"producte": info,"comanda":comandas}
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