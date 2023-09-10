import pytholog as pl
import json

dictCommands = {}
dictSales = {}


with open("Development/Pablo/palabras.json", "r") as file:
    dictCommands = json.load(file)

# print(dictCommands)


def listName(data):
    list = []
    for key, value in data.items():
        temp = key
        list.append(temp)
    return list


def listPalabras(data):
    list = []
    for key, value in data.items():
        temp = value["palabras"]
        list.append(temp)
    return list


def listUbic(data):
    list = []
    for key, value in data.items():
        temp = value["ubicacion"]
        list.append(temp)
    return list


def listDo(data):
    list = []
    for key, value in data.items():
        temp = value["hacer"]
        list.append(temp)
    return list


listaP = listPalabras(dictCommands)
listaU = listUbic(dictCommands)
listaD = listDo(dictCommands)
listaNam = listName(dictCommands)


def baseConocimiento():
    inventary_kb = pl.KnowledgeBase("commands")
    facts = []

    # lista de productos y cantidad
    for i in listaNam:
        facts.append("comando(" + str(i) + ")")
        for j in dictCommands[i]["palabras"]:
            facts.append("sinonimos(" + str(j) + "," + str(i) + ")")

    for i, j in zip(listaNam, listaD):
        facts.append("es(" + str(i) + "," + str(j) + ")")

    for i, j in zip(listaD, listaU):
        facts.append("donde(" + str(i) + "," + str(j) + ")")

    # rules
    facts.append("comandos(X):- sinonimos(X, Y), comando(Y)")

    # prolog

    inventary_kb(facts)

    # query
    print(facts)
    print(inventary_kb.query(pl.Expr("comandos(investiga)")))


baseConocimiento()


def addSeller(name):
    name = name.lower()
    if dictSales.get(name) == None:
        dictSales[name] = {}
    else:
        print("Vendedor " + name + " ya registrado")


def ventaProducto(seller, product, quantity, data):
    seller = seller.lower()
    product = product.lower()

    # verifica si el vendedor existe
    if dictSales.get(seller) == None:
        print(
            "Vendedor"
            + seller
            + " no encontrado, agrega este vendedor con addSeller("
            + seller
            + ")"
        )

    # Agrega la cantidad de producto vendio en una diccionario si existe el producto
    elif (
        dictSales.get(seller).get(product) != None
        and (data.get(product).get("cantidad") - quantity) >= 0
    ):
        dictSales[seller][product] = dictSales.get(seller).get(product) + quantity

    # Agrega la cantidad de producto vendio en una diccionario sino existe el producto
    elif dictSales.get(seller) != None:
        temp = quantity
        dictSales[seller][product] = temp

    # Actualiza la cantidad de productos segun los vendidos
    if (data.get(product).get("cantidad") - quantity) >= 0:
        data[product]["cantidad"] = data.get(product).get("cantidad") - quantity
    else:
        print("No es posible realizar la venta de " + str(product))
    print("Unidades de " + str(product) + ": " + str(data.get(product).get("cantidad")))


def compraProducto(product, quantity, data):
    # Actualiza el diccionario
    data[product]["cantidad"] = data.get(product).get("cantidad") + quantity


addSeller("tomas")
addSeller("juan")
addSeller("pedro")
addSeller("alberto")
addSeller("tulio")
# compraProducto("papas", 4, )

ventaProducto("tomas", "papas", 10, dictCommands)
ventaProducto("tomas", "cheetos", 5, dictCommands)
ventaProducto("tomas", "papas", 3, dictCommands)
ventaProducto("tomas", "ponky", 4, dictCommands)

ventaProducto("juan", "papas", 10, dictCommands)
ventaProducto("juan", "cheetos", 5, dictCommands)
ventaProducto("juan", "papas", 3, dictCommands)
ventaProducto("juan", "ponky", 4, dictCommands)

ventaProducto("pedro", "papas", 10, dictCommands)
ventaProducto("pedro", "cheetos", 5, dictCommands)
ventaProducto("pedro", "papas", 3, dictCommands)
ventaProducto("pedro", "ponky", 4, dictCommands)

ventaProducto("alberto", "papas", 10, dictCommands)
ventaProducto("alberto", "cheetos", 5, dictCommands)
ventaProducto("alberto", "papas", 3, dictCommands)
ventaProducto("alberto", "ponky", 4, dictCommands)

ventaProducto("tulio", "papas", 1, dictCommands)
# ventaProducto("tulio","cheetos",0,dictProducts)
# ventaProducto("tulio","papas",0,dictProducts)
# ventaProducto("tulio","ponky",0,dictProducts)
