from Relation_functions import createTable, getProduct, getSimilars, insertdata
from classes.send_data import DataSender


idsToUse = [16118, 3357, 9553, 32457, 48575]
rule = "content"

itemsToGet = ["brand", "category", "doelgroep", "price"]
DataSenderObject = DataSender()


createTable(rule)

for i in idsToUse:            #aan te passen naar alle items van de database, voor gemak nu even 5 items gekozen
    items = getProduct(itemsToGet, i)
    idlist = getSimilars(itemsToGet, items)
    insertdata(rule, idlist, i)