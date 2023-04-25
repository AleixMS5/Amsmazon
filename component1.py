

import pickle


def saveobject(object1, file):
    with open(file, "ab") as file:
        pickle.dump(object1, file)


def restoreobject(index, file):
    with open(file, "rb") as file:
        while True:
            try:
                object1 = pickle.load(file)
            except EOFError:
                return None
            if object1.id == index:
                return object1


def deleteFitxer(file):
    open(file,"wb")


def updateObject(file,id,objecte):
    array =  list()
    with open(file, "rb") as fil:
        while True:
            try:
                object1 = pickle.load(fil)

                if object1.id == id:
                        array.append(objecte)
                else:
                    array.append(object1)
            except EOFError:
                break

    deleteFitxer(file)
    with open(file, "ab") as fil:
        for objecte in array:
            pickle.dump(objecte, fil)


def deleteObject(file,id):
    array =  list()
    with open(file, "rb") as fil:
        while True:
            try:
                object1 = pickle.load(fil)

                if object1.id == id:
                    pass
                else:
                    array.append(object1)
            except EOFError:
                break

    deleteFitxer(file)
    with open(file, "ab") as fil:
        for objecte in array:
            pickle.dump(objecte, fil)


def getall(file):
    array = list()
    with open(file, "rb") as fil:
        while True:
            try:
                object1 = pickle.load(fil)
                array.append(object1)
            except EOFError:
                return array




