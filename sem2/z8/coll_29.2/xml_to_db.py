from xml.etree.ElementTree import ElementTree, parse
from database import SQLiteDatabase

XML_file = "/home/olga/Projects/domashki/sem2/z8/coll_29.2/currencies_usd.xml"
DB_file =  "/home/olga/Projects/domashki/sem2/z8/coll_29.2/currencies.db"

def to_float(string):
    i = 0
    res = ""
    while i<len(string):
        if string[i] != ',':
            res += string[i]
        i += 1
    return res

with open(XML_file) as f:
    tree = parse(f)

currencies = []

for child in tree.iter():
    if child.tag == "targetCurrency":
        currencies.append(child.text)

cols = {
    "currency": "TEXT",
    "exchange_rate": "REAL",
    "inverse_rate": "REAL"
}
db = SQLiteDatabase("currencies")
db.execute_query("DROP TABLE IF EXISTS usd", commit=True)
db.create_table("usd", cols)

for curr in currencies:
    cols["currency"] = curr
    in_curr = False
    for child in tree.iter():
        if child.tag == "targetCurrency":
            if child.text == curr:
                in_curr = True
        elif child.tag == "exchangeRate" and in_curr:
            # ex_rate = float(child.text)
            cols["exchange_rate"] = to_float(child.text)
        elif child.tag == "inverseRate" and in_curr:
            # inv_rate = float(child.text)
            cols["inverse_rate"] = to_float(child.text)
        elif child.tag == "item" and in_curr:
            in_curr = False
        else:
            pass
    db.join("usd", cols)


