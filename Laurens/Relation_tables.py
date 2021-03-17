import psycopg2


"""
Content Rules (bij bijvoorbeeld het product zelf)

neem van het huidige product de:
1. brand
2. category
3. subcategory
4. subsubcategory
5. gender
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

def connectToDB(host, database, user, password):
    """verbind met de database"""
    conn = psycopg2.connect(host, database ,user ,password)


def getProduct(typelist, productID):
    """pakt de gegevens van het huidige product aan de hand van een list met items om te pakken,
    geeft een lijst met deze gegevens terug"""
    items = []

    for itemName in typelist:
        query = f"SELECT {itemName} FROM products WHERE _id = {productID}"

        items.append(xxxx)

    return items


def getSimilars(typelist, itemlist):
    """zoekt naar soortgelijke product aan de hand van een lijst met specifieke gegevens,
    geeft een lijst met id's terug"""
    for item in itemlist:
        query = f"SELECT _id FROM products WHERE {typelist} = {item}"




def createTable(list, type, weightdict):
    """maakt een tabel aan met de gegeven product id's. dit zijn altijd 5 id's (het product zelf en 4 recommendations
    type is contentrules of collabrules.
    Voor content rules geldt dat van een lager gewicht dingen sneller worden gepakt
    """

    try:
        #drop table if exists
    except ValueError:
        pass

    #create table

    #fill table



def closeDB():
    """sluit verbinding"""




def collabRuleFilter():
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

def getVisitor(typelist, id):
    """neemt aan de hand van buid de visitor en sessions, en haalt daar items uit aan de hand van de meegegeven lijst,
    geeft een lijst van deze gegevens terug"""

    for itemName in typelist:
        query = f"SELECT {itemName} FROM xxx WHERE {id} = xxx"