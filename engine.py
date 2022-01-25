import threading
import time
import threading as thread
from flask import request
from Model.transaction import transaction_from_string
from config import specified_port, db, engine
from Model.users import users, to_string
from Model.creditCard import creditCard, card_to_string

@engine.route('/first', methods=['POST'])
def first_function():
    db.create_all()
    db.session.commit()
    _cdNumber = request.get_data()
    _cdNumber = _cdNumber.decode()
    found_cd = creditCard.query.filter_by(cdNumber=_cdNumber).first()
    #trans = transaction.query.filter_by(tName='').first()
    if (found_cd == None):
        cd = creditCard("4242 4242 4242 4242", "Pera Peric", "02/23", "123")
        db.session.add(cd)
        db.session.commit()
        found_cd = creditCard.query.filter_by(cdNumber=_cdNumber).first()
        rv = card_to_string(found_cd)
        print("Retval is: " + rv)
    else:
        rv = card_to_string(found_cd)
        print("Retval is: " + rv)
    return rv

@engine.route('/second',methods=['POST'])
def second_function():
    poruka = request.get_data().decode()
    p_list = poruka.split('|')
    found_user = users.query.filter_by(email=p_list[2]).first()
    if found_user:
        ans = "User with this email already exists."
        return ans.encode("utf-8")
    else:
        usr = users(p_list[0], p_list[1], p_list[2], p_list[3], p_list[4], p_list[5], p_list[6], p_list[7])
        db.session.add(usr)
        db.session.commit()
        return "success".encode("utf-8")

@engine.route('/third',methods=['POST'])
def third_function():
    poruka = request.get_data().decode()
    p_list = poruka.split('|')
    found_user = users.query.filter_by(email=p_list[0]).first()
    if found_user != None and p_list[0] == found_user.email and p_list[1] == found_user.password:
        return found_user.email.encode("utf-8")
    else:
        return "Wrong email address and/or password."

@engine.route('/fourth',methods=['POST'])
def fourth_function():
    poruka = request.get_data().decode()
    found_user = users.query.filter_by(email=poruka).first()
    return to_string(found_user).encode("utf-8")

@engine.route('/fifth',methods=['POST'])
def fifth_function():
    #user|_name|_surname|_password|_address|_city|_country|_telephone
    poruka = request.get_data().decode()
    poruka = poruka.split('|')
    found_user = users.query.filter_by(email=poruka[0]).first()
    if (poruka[1] and poruka[2] and poruka[3] and poruka[4] and poruka[5] and poruka[6] and poruka[7]):
        found_user.firstName = poruka[1]
        found_user.lasttName = poruka[2]
        found_user.password = poruka[3]
        found_user.address = poruka[4]
        found_user.country = poruka[5]
        found_user.city = poruka[6]
        found_user.telephone = poruka[7]
        db.session.commit()
        return to_string(found_user).encode("utf-8")
    else:
        return ("err||" + to_string(found_user)).encode("utf-8")

@engine.route('/sixth',methods=['POST'])
def sixth_function():
    poruka = request.get_data().decode()
    found_user = users.query.filter_by(email=poruka).first()
    return to_string(found_user).encode("utf-8")

@engine.route('/seventh',methods=['POST'])
def seventh_function():
    #_cdNumber
    poruka = request.get_data().decode()
    found_cd = creditCard.query.filter_by(cdNumber=poruka).first()
    if(found_cd == None):
        return "none"
    else:
        return card_to_string(found_cd).encode("utf-8")

@engine.route('/eighth',methods=['POST'])
def eighth_function():
    #user|_cdNumber
    poruka = request.get_data().decode()
    poruka = poruka.split("|")
    user = poruka[0]
    _cdNumber = poruka[1]
    found_user = users.query.filter_by(email=user).first()
    found_cd = creditCard.query.filter_by(cdNumber=_cdNumber).first()
    found_user.verified = True
    found_user.cdNumber = _cdNumber
    found_cd.cardAmount = found_cd.cardAmount - 1
    db.session.commit()
    return "Success"

@engine.route('/ninth',methods=['POST'])
def ninth_function():
    poruka = request.get_data().decode()
    found_user =users.query.filter_by(email=poruka).first()
    return to_string(found_user).encode("utf-8")

@engine.route('/tenth',methods=['POST'])
def tenth_function():
    poruka = request.get_data().decode()
    found_user = users.query.filter_by(email=poruka).first()
    return to_string(found_user).encode("utf-8")

@engine.route('/eleventh',methods=['POST'])
def eleventh_function():
    poruka = request.get_data().decode()
    #user|_deposit
    p = poruka.split("|")
    user = p[0]
    _deposit = p[1]
    found_user = users.query.filter_by(email=user).first()
    found_cd = creditCard.query.filter_by(cdNumber=found_user.cdNumber).first()
    if (found_cd.cardAmount - int(_deposit) >= 0):
        found_cd.cardAmount = found_cd.cardAmount - int(_deposit)
        found_user.amount = found_user.amount + int(_deposit)
        db.session.commit()
        return "success"
    else:
        return "failure"

@engine.route('/twelveth',methods=['POST'])
def twelveth_function():
    poruka = request.get_data().decode()
    found_user = users.query.filter_by(email=poruka).first()
    if (found_user.verified == True):
        # slati serveru
        found_cd = creditCard.query.filter_by(cdNumber=found_user.cdNumber).first()
        return card_to_string(found_cd).encode("utf-8")
    else:
        return "failure"

@engine.route('/thirteenth',methods=['POST'])
def thirteenth_function():
    poruka = request.get_data().decode("utf-8")
    poruka = transaction_from_string(poruka)
    db.session.add(poruka)
    db.session.commit()

def sleep_thread(first, second, trans):
    time.sleep(300)
    db.session.add(trans)
    found_user = users.query.filter_by(email=first).first()
    traded_user = users.query.filter_by(email=second).first()
    traded_user.amount = traded_user.amount + int(trans.tAmount)
    trans.tState = "Obradjeno"
    db.session.expire_on_commit = True
    db.session.commit()

@engine.route('/fourteenth',methods=['POST'])
def fourteenth_function():

    poruka = request.get_data().decode("utf-8")
    p = poruka.split(",")
    p1 = p[1].split("|")
    first = p1[0]
    second = p1[1]
    trans = transaction_from_string(p[0])
    db.session.add(trans)
    found_user = users.query.filter_by(email=first).first()
    found_user.amount = found_user.amount - int(trans.tAmount)
    db.session.commit()
    x = threading.Thread(target=sleep_thread, args=(first, second, trans))
    x.start()
    return "success"

if __name__ == "__main__":
    engine.run(port=specified_port,debug=True)
