import psycopg2
from classes.send_data import DataSender
import itertools

"""
Content Rules (bij bijvoorbeeld het product zelf)

neem van het huidige product de:
1. brand
2. category
3. subcategory
4. subsubcategory
5. gender (/doelgroep)
6. prijs

kijk voor elk nieuw product (lager gewicht = meer prioriteit):
type          | gewicht
brand = brand | 6
category = category | 5
subcategory = subcategory | 4
subsub = subsub | 3
gender = gender | 3
folder_actief = true | 2, maximaal 1 product
availability != 0 | 1
prijs = prijs | 3/4
"""

weight = [ #type, weight, special rules
    ["brand", "category", "subcategory", "subsubcategory", "gender", "doelgroep", "folder_actief", "availability", "price"],
    [6, 5, 4, 3, 4, 3, 2, 1, 3],
    ["", "", "", "", "", "", "max 1", "", ""]
]

itemsToGet = ["brand", "category", "doelgroep", "price"]
DataSenderObject = DataSender()

def getProduct(typelist, productID):
    """pakt de gegevens van het huidige product aan de hand van een list met items om te pakken,
    geeft een lijst met deze gegevens terug"""
    print(typelist)
    liststring = ', '.join(typelist)

    con = DataSenderObject.openconnection()
    cur = con.cursor()

    query = "SELECT {} FROM products a " \
            "FULL JOIN properties c ON a.idproducts = c.products_idproducts " \
                "FULL JOIN category g ON a.idproducts = g.products_idproducts " \
                "FULL JOIN subcategory k ON g.idcategory = k.category_idcategory " \
                "WHERE (idproducts = '{}')".format(liststring, productID)
    print(query)

    cur.execute(query)
    con.commit()
    items = cur.fetchall()

    cur.close()
    con.close()

    print(items)
    return getSimilars(typelist, items, productID)



def getSimilars(typelist, itemlist, productID):
    """zoekt naar soortgelijke product aan de hand van een lijst met specifieke gegevens,
    geeft een lijst met id's terug"""

    idlist = []

    con = DataSenderObject.openconnection()
    cur = con.cursor()

    for i in range(len(typelist)):

        query = "SELECT idproducts FROM products a " \
                "FULL JOIN properties c ON a.idproducts = c.products_idproducts " \
                "FULL JOIN category g ON a.idproducts = g.products_idproducts " \
                "FULL JOIN subcategory k ON g.idcategory = k.category_idcategory " \
                "WHERE ({} = '{}')".format(typelist[i], itemlist[0][i])
        print(query)
        cur.execute(query)
        con.commit()
        idlist.append(list(itertools.chain(*(cur.fetchall()))))

    cur.close()
    con.close()

    return idlist

#print(getProduct(itemsToGet,7674))

def createTable(ruletype):
    """maakt een tabel aan met de gegeven product id's. dit zijn altijd 5 id's (het product zelf en 4 recommendations
    type is contentrules of collabrules."""

    if ((ruletype.lower() == "content") or (ruletype.lower() == "collab")):
        newtype = ruletype.lower()
    else:
        return "An error occured on table type. Please check if the correct type of rules has been entered (content/collab)"

    deletequery = "DROP TABLE IF EXISTS {}Rules CASCADE ".format(newtype)
    createquery = "CREATE TABLE IF NOT EXISTS {}Rules (" \
                  "current_item VARCHAR(255) NOT NULL, " \
                  "recomm_one VARCHAR(255) NOT NULL, " \
                  "recomm_two VARCHAR(255) NOT NULL, " \
                  "recomm_three VARCHAR(255) NOT NULL, " \
                  "recomm_four VARCHAR(255) NOT NULL, " \
                  "PRIMARY KEY (current_item))".format(newtype)
                  #this query needs a different first item for collab rules!!!!!!!!!

    con = DataSenderObject.openconnection()
    cur = con.cursor()
    cur.execute(deletequery)
    print("table deleted succesfully")
    cur.execute(createquery)
    print("table created succesfully")
    con.commit()
    cur.close()
    con.close()


def fillTable(typelist, IDlist, weight):
    """selecteerd welke id's uit de lijst worden genomen aan de hand van gewicht en vult de tabel"""

    finalIDs = []







print(createTable("content"))


"""
Collaboration Rules (bij bijvoorbeeld de homepagina of het uitchecken)

neem van de huidige visitor:
1. buids om te koppelen aan user (en eerdere sessies)
2. waar mogelijk wat eerder in het winkelmandje heeft gelegen maar niet is gekocht

kijk voor elk nieuw product (lager gewicht = meer prioriteit):
type                                            | gewicht
eerder gekocht + product.herhaalaankopen = true | x bij hoofdpagina, max x product
eerder in winkelmand | x bij hoofdpagina, y bij winkelmand, max x product
combinaties product winkelmand vergeleken met andere mandjes | , enkel bij winkelmand, max x product
"""

stuffToGet = ["has_sale + idproducts + herhaalaankopen", "viewed before", ""]

def getVisitor(typelist, id):
    """neemt aan de hand van buid de visitor en sessions, en haalt daar items uit aan de hand van de meegegeven lijst,
    geeft een lijst van deze gegevens terug"""
    liststring = ', '.join(typelist)

    query = "SELECT {} FROM sessions a "\
            "FULL JOIN orders c ON a.idsessions = c.sessions_idsessions "\ 
            "FULL JOIN buids g ON a.idsessions = g.sessions_idsessions "\
            "FULL JOIN visitors k ON g.visitors_idvisitors = k.idvisitors "\
            "FULL JOIN has_sale m ON a.idsessions = m.sessions_idsessions "\
            "FULL JOIN products p ON m.products_idproducts = p.idproducts "\
            "FULL JOIN viewed_before t ON k.idvisitors = t.visitors_idvisitors "\
            "WHERE (idsessions = {})".format(liststring, id)