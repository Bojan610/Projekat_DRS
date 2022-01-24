from marshmallow import Schema, fields
from config import db, ma

class transaction(db.Model):
    tSender = db.Column("tSender", db.String(100), primary_key=True)
    tReceiver = db.Column(db.String(100))
    tAmount = db.Column(db.Integer)
    tRandom = db.Column(db.Integer)

    def __init__(self,tSender,tReceiver,tAmount,tRandom):
        self.tSender = tSender
        self.tReceiver = tReceiver
        self.tAmount = tAmount
        self.tRandom = tRandom

def transaction_to_string(self: transaction):
    ans = self.tSender + "|" + self.tReceiver + "|" + str(self.tAmount) + "|" + str(self.tRandom)
    return ans

def transaction_from_string(text: str):
    spl = text.split("|")
    t = transaction(spl[0], spl[1])
    t.tAmount = int(spl[2])
    t.tRandom = int(spl[3])
    return t

class tSchema(Schema):
    tSender = fields.Str()
    tReceiver = fields.Str()
    tAmount = fields.Integer()
    tRandom = fields.Integer()

