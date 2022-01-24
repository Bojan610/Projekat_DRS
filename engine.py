#from flask import Flask
import socket
from config import specified_port, db
from Model.creditCard import creditCard
from Model.users import users, to_string
from Model.creditCard import creditCard, card_to_string

def first_function(_cdNumber):
    found_cd = creditCard.query.filter_by(cdNumber=_cdNumber).first()
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

def second_function(poruka):
    p_list = poruka.split('|')
    found_user = users.query.filter_by(email=p_list[2]).first()
    if found_user:
        ans = "User with this email already exists."
        return ans
    else:
        usr = users(p_list[0], p_list[1], p_list[2], p_list[3], p_list[4], p_list[5], p_list[6], p_list[7])
        db.session.add(usr)
        db.session.commit()
        return "success"


def third_function(poruka):
    p_list = poruka.split('|')
    found_user = users.query.filter_by(email=p_list[0]).first()
    if found_user != None and p_list[0] == found_user.email and p_list[1] == found_user.password:
        return found_user.email
    else:
        return "Wrong email address and/or password."


def fourth_function(poruka):
    found_user = users.query.filter_by(email=poruka).first()
    return to_string(found_user)


def fifth_function(poruka):
    #user|_name|_surname|_password|_address|_city|_country|_telephone
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
        return to_string(found_user)
    else:
        return "err||" + to_string(found_user)

def sixth_function(poruka):
    found_user = users.query.filter_by(email=poruka).first()
    return to_string(found_user)


def seventh_function(poruka):
    #_cdNumber
    found_cd = creditCard.query.filter_by(cdNumber=poruka).first()
    if(found_cd == None):
        return "none"
    else:
        return card_to_string(found_cd)


def eighth_function(poruka):
    #user|_cdNumber
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


def ninth_function(poruka):
    found_user =users.query.filter_by(email=poruka).first()
    return to_string(found_user)


def tenth_function(poruka):
    found_user = users.query.filter_by(email=poruka).first()
    return to_string(found_user)


def eleventh_function(poruka):
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

def twelveth_function(poruka):
    found_user = users.query.filter_by(email=poruka).first()
    if (found_user.verified == True):
        # slati serveru
        found_cd = creditCard.query.filter_by(cdNumber=found_user.cdNumber).first()
        return card_to_string(found_cd)
    else:
        return "failure"


if __name__ == "__main__":
    db.create_all()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    print ("Socket successfully created!")
    s.bind(('',specified_port))
    print("socket binded to %s" % (specified_port))
    #parametar oznacava broj "unaccepted" konekcija koje su dozvoljene pre nego sto "server" pocne da odbija nove konekcije
    s.listen(12)
    print("socket is listening")

    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)
        try:
            msg = c.recv(4096)
            x = msg.decode("utf-8")
            print("Message received: " + x)
            if("req-1|" in x):
                e = x.removeprefix("req-1|")
                answer = first_function(e)
            elif("req-2|" in x):
                e = x.removeprefix("req-2|")
                answer = second_function(e)
            elif("req-3|" in x):
                e = x.removeprefix("req-3|")
                answer = third_function(e)
            elif("req-4|" in x):
                e = x.removeprefix("req-4|")
                answer = fourth_function(e)
            elif("req-5|" in x):
                e = x.removeprefix("req-5|")
                answer = fifth_function(e)
            elif("req-6|" in x):
                e = x.removeprefix("req-6|")
                answer = sixth_function(e)
            elif ("req-7|" in x):
                e = x.removeprefix("req-7|")
                answer = seventh_function(e)
            elif ("req-8|" in x):
                e = x.removeprefix("req-8|")
                answer = eighth_function(e)
            elif ("req-9|" in x):
                e = x.removeprefix("req-9|")
                answer = ninth_function(e)
            elif ("req-10|" in x):
                e = x.removeprefix("req-10|")
                answer = tenth_function(e)
            elif ("req-11|" in x):
                e = x.removeprefix("req-11|")
                answer = eleventh_function(e)
            elif ("req-12|" in x):
                e = x.removeprefix("req-12|")
                answer = twelveth_function(e)
            else:
                answer = "unknown request"
            print("Answer sent: " + answer)
            c.sendall(answer.encode())
        except:
            continue
        finally:
            continue
c.close()




