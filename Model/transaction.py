from marshmallow import Schema, fields
from config import db

class transaction(db.Model):
    tSender = db.Column("tSender", db.String(100), primary_key=True)
    tReceiver = db.Column(db.String(100))
    tAmount = db.Column(db.Integer)
    tRandom = db.Column(db.Integer)
    tType = db.Column(db.String(100))

    def __init__(self,tSender,tReceiver,tAmount,tRandom,tType):
        self.tSender = tSender
        self.tReceiver = tReceiver
        self.tAmount = tAmount
        self.tRandom = tRandom
        self.tType = tType

def transaction_to_string(self: transaction):
    ans = self.tSender + "|" + self.tReceiver + "|" + str(self.tAmount) + "|" + str(self.tRandom) + "|" + self.tType
    return ans

def transaction_from_string(text: str):
    spl = text.split("|")
    t = transaction(spl[0], spl[1])
    t.tAmount = int(spl[2])
    t.tRandom = int(spl[3])
    t.Type = spl[4]
    return t

class tSchema(Schema):
    tSender = fields.Str()
    tReceiver = fields.Str()
    tAmount = fields.Integer()
    tRandom = fields.Integer()
    tType = fields.Str();

