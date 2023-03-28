from tkinter import ttk, messagebox
import tkinter as tk
import json
from types import SimpleNamespace
llistaProductes=[]
json_o1=[]
class producte:
    def __init__(self, nom, preu, descripcio, descripciollarga,destacat,valoracio,imatge):
        self.nom=nom
        self.preu=preu
        self.descripcio=descripcio
        self.descripciollarga=descripciollarga
        self.destacat=destacat
        self.valoracio=valoracio
        self.imatge=imatge

def llegir() :
    try:
        llistaProductes.clear()
        with open('productes.json') as fitxer:
            json_02 = json.load(fitxer)
            for jsons in json_02:
                llistaProductes.append( json.loads(jsons, object_hook=lambda d: SimpleNamespace(**d)))
    except Exception:
        pass

def guardar() :
    lbl_resultat.config(text="")
    llegir()
    json_o1.clear()

    try:
        nomg=nom.get()
        if (len(nomg)==0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="ha de tenir un nom", title="Avís")
    try:
        preug=float(ed.get())
        if (preug < 0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="el preu ha de ser un numero", title="Avís")
    try:
        val=float(pess.get())
        if (val>5 or val<0):
            raise Exception
    except Exception:
        lbl_resultat.config(text="")
        messagebox.showinfo(message="la valoracio ha de ser un numero i ha de ser superior a 0 i inferior a 5", title="Avís")
    try:
        desgc=desc.get()
        if (len(desgc)==0):
            raise Exception
    except Exception:

        messagebox.showinfo(message="ha de tenir una descripció", title="Avís")

    try:

        product = producte(nomg, preug,desgc , alt.get(), combo1.get(), val, força.get())
        llistaProductes.append(product)
        for product in llistaProductes:
            json_o1.append(json.dumps(product.__dict__))
        with open('productes.json', 'w') as fitxer:
            json.dump(json_o1, fitxer)
    except Exception:
        pass



if __name__ == '__main__':
    root = tk.Tk()

    # Formulari 1:
    frame2 = tk.Frame(root)
    frame2.pack()


    combo1 = ttk.Combobox(frame2,
                          state="readonly",
                          values=[True, False]
                          )
    button3 = tk.Button(frame2,
                        text="Guardar",
                        command=guardar
                        )
    nom = tk.Entry(frame2, width="50")
    desc = tk.Entry(frame2, width="50")
    ed = tk.Entry(frame2, width="50")
    alt = tk.Entry(frame2, width="50")
    pess = tk.Entry(frame2, width="50")
    força = tk.Entry(frame2, width="50")

    destacat = tk.Label(frame2, text="destacat", width="50", justify=tk.LEFT)
    lbl_nom = tk.Label(frame2, text="nom", width="50", justify=tk.LEFT)
    lbl_desc = tk.Label(frame2, text="descripcio", width="50", justify=tk.LEFT)
    preu = tk.Label(frame2, text="preu", width="50", justify=tk.LEFT)
    descripcio = tk.Label(frame2, text="descripcio llarga", width="50", justify=tk.LEFT)
    valoracio = tk.Label(frame2, text="valoracio", width="50", justify=tk.LEFT)
    imatge = tk.Label(frame2, text="imatge", width="50", justify=tk.LEFT)
    lbl_resultat = tk.Label(frame2, text="", width="50", justify=tk.LEFT)


    button3.pack()
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


    root.mainloop()