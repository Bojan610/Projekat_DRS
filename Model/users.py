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
        self.cdNumber = "0"

        def __repr__(self):
            return '<User %r>' % self.fname

    def fill_class(self, amount, verified, cdNumber):
        self.amount = amount
        self.verified = verified
        self.cdNumber = cdNumber


def from_string(tekst: str):
    tekst = tekst.split('|')
    ans: users = users(tekst[0], tekst[1], tekst[2], tekst[3], tekst[4], tekst[5], tekst[6], tekst[7])
    if tekst[9] == "False":
        is_verified = False
    else:
        is_verified = True
    ans.fill_class(int(tekst[8]), is_verified , tekst[10])
    return ans


def to_string(self: users):
    ans: str = self.firstName + "|" + self.lasttName + "|"
    ans += self.email + "|" + self.password + "|" + self.address
    ans += "|" + self.city + "|" + self.country + "|"
    ans += self.telephone + "|" + str(self.amount) + "|" + str(self.verified) + "|" + self.cdNumber
    return ans


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