from marshmallow import Schema, fields
from config import db

class wallet(db.Model):
    id = db.Column("id", db.String(100), primary_key=True)
    currency1 = db.Column(db.Integer)
    currency2 = db.Column(db.Integer)
    currency3 = db.Column(db.Integer)
    currency4 = db.Column(db.Integer)
    currency5 = db.Column(db.Integer)
    currency6 = db.Column(db.Integer)
    currency7 = db.Column(db.Integer)
    currency8 = db.Column(db.Integer)
    currency9 = db.Column(db.Integer)
    currency10 = db.Column(db.Integer)
    currency11 = db.Column(db.Integer)
    currency12 = db.Column(db.Integer)
    

    def __init__(self,id,currency1,currency2,currency3, currency4, currency5, currency6, currency7, currency8, currency9, currency10, currency11, currency12):
        self.id = id
        self.currency1 = currency1
        self.currency2 = currency2
        self.currency3 = currency3
        self.currency4 = currency4
        self.currency5 = currency5
        self.currency6 = currency6
        self.currency7 = currency7
        self.currency8 = currency8
        self.currency9 = currency9
        self.currency10 = currency10
        self.currency11 = currency11
        self.currency12 = currency12

def wallet_to_string(tr : wallet):
    id = tr.id
    currency1 = tr.currency1
    currency2 = tr.currency2
    currency3 = tr.currency3
    currency4 = tr.currency4
    currency5 = tr.currency5
    currency6 = tr.currency6
    currency7 = tr.currency7
    currency8 = tr.currency8
    currency9 = tr.currency9
    currency10 = tr.currency10
    currency11 = tr.currency11
    currency12 = tr.currency12
    retval: str = id + "|" + str(currency1) + "|" + str(currency2) + "|" + str(currency3) + "|" + str(currency4) + "|" + str(currency5) + "|" + str(currency6) + "|" + str(currency7) + "|" + str(currency8) + "|" + str(currency9) + "|" + str(currency10) + "|" + str(currency11) + "|" + str(currency12)
    return retval

def wallet_from_string(msg : str):
    m = msg.split("|")
    id = m[0]
    retval = wallet(id, m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12])
    return retval

def lista_u_string_wallet(lista):
    s = ""
    length = len(lista)
    for i in range(length):
        s += wallet_to_string(lista[i]) + ";"
    s = s.removesuffix(';')
    return s


def lista_iz_stringa_wallet(string):
    lista_stringova = string.split(";")
    length = len(lista_stringova)
    lista_valuta : list = []
    for i in range(length):
        lista_valuta.insert(i,wallet_from_string(lista_stringova[i]))
    return lista_valuta

class cdSchema(Schema):
    id = fields.Str()
    currency1 = fields.Integer()
    currency2 = fields.Integer()
    currency3 = fields.Integer()
    currency4 = fields.Integer()
    currency5 = fields.Integer()
    currency6 = fields.Integer()
    currency7 = fields.Integer()
    currency8 = fields.Integer()
    currency9 = fields.Integer()
    currency10 = fields.Integer()
    currency11 = fields.Integer()
    currency12 = fields.Integer()