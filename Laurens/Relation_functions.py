import psycopg2
from classes.send_data import DataSender
import itertools



DataSenderObject = DataSender()

def getProduct(typelist, productID):
    """pakt de gegevens van het huidige product aan de hand van een list met items om te pakken,
    geeft een lijst met deze gegevens terug"""

    liststring = ', '.join(typelist)

    con = DataSenderObject.openconnection()
    cur = con.cursor()

    query = "SELECT {} FROM products a " \
            "FULL JOIN properties c ON a.idproducts = c.products_idproducts " \
            "FULL JOIN category g ON a.idproducts = g.products_idproducts " \
            "FULL JOIN subcategory k ON g.idcategory = k.category_idcategory " \
            "WHERE (idproducts = '{}')".format(liststring, productID)


    cur.execute(query)
    con.commit()
    items = cur.fetchall()

    cur.close()
    con.close()

    return items

def getSimilars(typelist, itemlist):
    """zoekt naar soortgelijke product aan de hand van een lijst met specifieke gegevens,
    geeft een lijst met id's terug"""

    newclause = whereClause(typelist, itemlist)
    idlist = []

    con = DataSenderObject.openconnection()
    cur = con.cursor()

    query = "SELECT idproducts FROM products a " \
            "FULL JOIN properties c ON a.idproducts = c.products_idproducts " \
            "FULL JOIN category g ON a.idproducts = g.products_idproducts " \
            "FULL JOIN subcategory k ON g.idcategory = k.category_idcategory " \
            "WHERE ({})".format(newclause)
    cur.execute(query)
    con.commit()
    idlist.append(list(itertools.chain(*(cur.fetchall()))))

    #moet worden uitgebreid om met steeds 1 where clausule minder te kunnen werken,
    #mochten er zoveel voorwaardes zijn en geen resultaten om de voorwaardes te verminderen
    #en toch nog resultaten krijgen

    cur.close()
    con.close()

    return idlist

def whereClause(typelist, itemlist):

    clause = ""
    firstinsert = True

    for i in range(len(typelist)):
        if typelist[i] != "brand":
            if type(typelist[i]) != "decimal.Decimal":
                if firstinsert:
                    insert = "{} = '{}'".format(typelist[i], itemlist[0][i])
                    clause += insert
                else:
                    insert = " and {} = '{}'".format(typelist[i], itemlist[0][i])
                    clause += insert
                firstinsert = False
            else:
                stuff = itemlist[0][i]
                floatstuff = float(stuff)
                intstuff = int(floatstuff)

                if firstinsert:
                    insert = "{} = '{}'".format(typelist[i], intstuff)
                    clause += insert
                else:
                    insert = " and {} = '{}'".format(typelist[i], intstuff)
                    clause += insert
                firstinsert = False
        else:
            continue

    return clause

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

def insertdata(ruletype, idlist, currentID):

    firstidlist = idlist.pop()
    try:
        theID = f'{currentID}'
        firstidlist.remove(theID)
    except:
        pass

    query = "INSERT INTO {}Rules(current_item, recomm_one, recomm_two, recomm_three, recomm_four) VALUES ({}, {}, {}, {}, {})".format(ruletype, currentID, firstidlist[0], firstidlist[1], firstidlist[2], firstidlist[4])
    #kan wellicht problemen gaan geven als de eerste lijst leeg was, wellicht pop if empty, meer voor vorige functie getsimilars

    con = DataSenderObject.openconnection()
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    cur.close()
    con.close()



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