from marshmallow import Schema, fields
from config import db

class users(db.Model):
    firstName = db.Column(db.String(100))
    lasttName = db.Column(db.String(100))
    email = db.Column("email", db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    telephone = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    verified = db.Column(db.Boolean)
    cdNumber = db.Column(db.String(100))

    def __init__(self, firstName, lasttName, email, password, address, city, country, tel):
        self.firstName = firstName
        self.lasttName = lasttName
        self.email = email
        self.password = password
        self.address = address
        self.city = city
        self.country = country
        self.telephone = tel
        self.amount = 0
        self.verified = False
        cdNumber = "0"

        def __repr__(self):
            return '<User %r>' % self.fname

class UserSchema(Schema):
    firstName = fields.Str()
    lasttName = fields.Str()
    email = fields.Email
    password = fields.Str()
    address = fields.Str()
    city = fields.Str()
    country = fields.Str()
    telephone = fields.Number()
    amount = fields.Integer()
    verified = fields.Boolean()
    cdNumber = fields.Str()