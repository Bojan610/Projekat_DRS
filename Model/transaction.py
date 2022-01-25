from marshmallow import Schema, fields
from config import db
import sha3
from random import randint

class transaction(db.Model):
    tHash = db.Column("tHash", db.String(100), primary_key=True)
    tSender = db.Column(db.String(100))
    tReceiver = db.Column(db.String(100))
    tAmount = db.Column(db.Integer)
    tState = db.Column(db.String(100))

    def __init__(self, tSender, tReceiver, tAmount, tState):
        k = sha3.keccak_256()
        sb = (tSender + tReceiver + str(tAmount) + str(randint(0, 100))).encode('ascii')
        k.update(sb)
        self.tHash = k.hexdigest()
        self.tSender = tSender
        self.tReceiver = tReceiver
        self.tAmount = tAmount
        self.tState = tState


def transaction_to_string(tr : transaction):
    state = tr.tState
    hash = tr.tHash
    amount = tr.tAmount
    sender = tr.tSender
    receiver = tr.tReceiver
    retval: str = hash + "|" + sender + "|" + receiver + "|" + str(amount) + "|" + state
    return retval

def transaction_from_string(msg : str):
    m = msg.split("|")
    state = m[4]
    hash = m[0]
    amount = int(m[3])
    sender = m[1]
    receiver = m[2]
    retval = transaction(sender,receiver,amount,state)
    retval.tHash = hash
    return retval

class tSchema(Schema):
    tSender = fields.Str()
    tReceiver = fields.Str()
    tAmount = fields.Integer()
    tRandom = fields.Integer()
    tType = fields.Str()

