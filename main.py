from tkinter import ttk, messagebox, CENTER
import tkinter as tk
import json
from types import SimpleNamespace
import pymongo
from bson import ObjectId

llistaProductes = []
json_o1 = []


class producte:
    def __init__(self, nom, preu, descripcio, descripciollarga, destacat, valoracio, imatge):
        self.nom = nom
        self.preu = preu
        self.descripcio = descripcio
        self.descripciollarga = descripciollarga
        self.destacat = destacat
        self.valoracio = valoracio
        self.imatge = imatge


def buscar1(a):
    curItem = tree.focus()
    text = tree.item(curItem)["values"]
    força.delete(0, tk.END)
    pess.delete(0, tk.END)
    combo1.delete(0, tk.END)
    alt.delete(0, tk.END)
    desc.delete(0, tk.END)
    ed.delete(0, tk.END)
    nom.delete(0, tk.END)
    idmod1.delete(0, tk.END)
    força.insert(0, text[7])
    pess.insert(0, text[6])
    combo1.insert(0, text[5])
    alt.insert(0, text[4])
    desc.insert(0, text[3])
    ed.insert(0, text[2])
    nom.insert(0, text[1])
    idmod1.insert(0, text[0])


def guardar():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["productes"]
    mycol = mydb["productes"]
    global nomg, preug, desgc, val
    lbl_resultat.config(text="")

    json_o1.clear()

    try:
        nomg = nom.get()
        if (len(nomg) == 0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="ha de tenir un nom", title="Avís")
    try:
        preug = float(ed.get())
        if (preug < 0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="el preu ha de ser un numero", title="Avís")
    try:
        val = float(pess.get())
        if (val > 5 or val < 0):
            raise Exception
    except Exception:
        lbl_resultat.config(text="")
        messagebox.showinfo(message="la valoracio ha de ser un numero i ha de ser superior a 0 i inferior a 5",
                            title="Avís")
    try:
        desgc = desc.get()
        if (len(desgc) == 0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="ha de tenir una descripció", title="Avís")
    if (combo1.get() == "True" or combo1.get() == "False"):
        destacat = combo1.get()
    else:
        destacat = "False"

    product = producte(nomg, preug, desgc, alt.get(), destacat, val, força.get())
    mydict = product.__dict__

    mydict = {"nom": product.nom, "preu": product.preu, "descripcio": product.descripcio,
              "descripciollarga": product.descripciollarga, "destacat": product.destacat,
              "valoracio": product.valoracio, "imatge": product.imatge}

    mycol.insert_one(mydict)
    llegir()


def modificar():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["productes"]
    mycol = mydb["productes"]
    global nomg, preug, desgc, val
    lbl_resultat.config(text="")

    json_o1.clear()

    try:
        nomg = nom.get()
        if (len(nomg) == 0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="ha de tenir un nom", title="Avís")
    try:
        preug = float(ed.get())
        if (preug < 0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="el preu ha de ser un numero", title="Avís")
    try:
        val = float(pess.get())
        if (val > 5 or val < 0):
            raise Exception
    except Exception:
        lbl_resultat.config(text="")
        messagebox.showinfo(message="la valoracio ha de ser un numero i ha de ser superior a 0 i inferior a 5",
                            title="Avís")
    try:
        desgc = desc.get()
        if (len(desgc) == 0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="ha de tenir una descripció", title="Avís")
    if (combo1.get() == "True" or combo1.get() == "False"):
        destacat = combo1.get()
    else:
        destacat = "False"

    product = producte(nomg, preug, desgc, alt.get(), destacat, val, força.get())
    print(product.nom)
    newvalues = [{"$set": {"nom": product.nom}}, {"$set": {"preu": product.preu}},
                 {"$set": {"descripcio": product.descripcio}}, {"$set": {"descripciollarga": product.descripciollarga}},
                 {"$set": {"destacat": product.destacat}}, {"$set": {"valoracio": product.valoracio}},
                 {"$set": {"imatge": product.imatge}}]
    pepe = idmod1.get()
    myquery = {"_id": ObjectId(pepe)}
    print(myquery)

    print(mycol.update_one(myquery, newvalues))
    llegir()


def delete():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["productes"]
    mycol = mydb["productes"]
    pepe = idmod1.get()
    myquery = {"_id": ObjectId(pepe)}
    mycol.delete_one(myquery)
    llegir()


def deleteAll():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["productes"]
    mycol = mydb["productes"]

    x = mycol.delete_many({})

    print(x.deleted_count, " documents deleted.")
    llegir()


root = tk.Tk()

# Formulari 1:
frame2 = tk.Frame(root)
frame2.pack()
tree = ttk.Treeview(frame2, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), show='headings', height=10)

tree.column("# 1", anchor=CENTER)
tree.heading("# 1", text="id")
tree.column("# 2", anchor=CENTER)
tree.heading("# 2", text="nom")
tree.column("# 3", anchor=CENTER)
tree.heading("# 3", text="preu")
tree.column("# 4", anchor=CENTER)
tree.heading("# 4", text="descripco")
tree.column("# 5", anchor=CENTER)
tree.heading("# 5", text="descripcio llarga")
tree.column("# 6", anchor=CENTER)
tree.heading("# 6", text="destacat")
tree.column("# 7", anchor=CENTER)
tree.heading("# 7", text="valoracio")
tree.column("# 8", anchor=CENTER)
tree.heading("# 8", text="imatge")
tree.bind('<ButtonRelease-1>', buscar1)
tree.pack()

combo1 = ttk.Combobox(frame2,
                      state="readonly",
                      values=[True, False]
                      )
button3 = tk.Button(frame2,
                    text="Guardar",
                    command=guardar
                    )
button4 = tk.Button(frame2,
                    text="Modificar",
                    command=modificar
                    )
button5 = tk.Button(frame2,
                    text="Borrar",
                    command=delete
                    )
button6 = tk.Button(frame2,
                    text="Borrar TOTS NO HO TOQUES BURRO QUE HO BORRA TOT",
                    command=deleteAll
                    )
nom = tk.Entry(frame2, width="50")
desc = tk.Entry(frame2, width="50")
ed = tk.Entry(frame2, width="50")
alt = tk.Entry(frame2, width="50")
pess = tk.Entry(frame2, width="50")
força = tk.Entry(frame2, width="50")
idmod1 = tk.Entry(frame2, width="50")

destacat = tk.Label(frame2, text="destacat", width="50", justify=tk.LEFT)
lbl_nom = tk.Label(frame2, text="nom", width="50", justify=tk.LEFT)
lbl_desc = tk.Label(frame2, text="descripcio", width="50", justify=tk.LEFT)
preu = tk.Label(frame2, text="preu", width="50", justify=tk.LEFT)
descripcio = tk.Label(frame2, text="descripcio llarga", width="50", justify=tk.LEFT)
valoracio = tk.Label(frame2, text="valoracio", width="50", justify=tk.LEFT)
imatge = tk.Label(frame2, text="imatge", width="50", justify=tk.LEFT)
lbl_resultat = tk.Label(frame2, text="", width="50", justify=tk.LEFT)
idmod = tk.Label(frame2, text="id operacions", width="50", justify=tk.LEFT)

button3.pack()
button4.pack()
button5.pack()
button6.pack()
lbl_resultat.pack()
destacat.pack()
combo1.pack()
lbl_nom.pack()
nom.pack()
lbl_desc.pack()
desc.pack()
preu.pack()
ed.pack()
descripcio.pack()
alt.pack()
valoracio.pack()
pess.pack()
imatge.pack()
força.pack()
idmod.pack()
idmod1.pack()


def llegir():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["productes"]
    mycol = mydb["productes"]
    for item in tree.get_children():
        tree.delete(item)
    for x in mycol.find():
        tree.insert('', 'end', text="1", values=(
            x.get("_id"), x.get("nom"), x.get("preu"), x.get("descripcio"), x.get("descripciollarga"),
            x.get("destacat"),
            x.get("valoracio"), x.get("imatge")
        ))


llegir()

tree.column("# 7", anchor=CENTER)
tree.heading("# 7", text="valoracio")
tree.column("# 8", anchor=CENTER)
tree.heading("# 8", text="imatge")
root.mainloop()
