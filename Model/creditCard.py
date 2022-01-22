from marshmallow import Schema, fields
from config import db

class creditCard(db.Model):
    cdNumber = db.Column("cdNumber", db.String(16), primary_key=True)
    cdName = db.Column(db.String(100))
    expDate = db.Column(db.String(100))
    securityCode = db.Column(db.String(3))
    cardAmount = db.Column(db.Integer)

    def __init__(self,cdNumber,cdName,expDate,securityCode):
        self.cdNumber = cdNumber
        self.cdName = cdName
        self.expDate = expDate
        self.securityCode = securityCode
        self.cardAmount = 200

        def __repr__(self):
            return '<User %r>' % self.cdNumber

class cdSchema(Schema):
    cdNumber = fields.Str()
    cdName = fields.Str()
    expDate = fields.Str()
    securityCode = fields.Str()
    cardAmount = fields.Integer()