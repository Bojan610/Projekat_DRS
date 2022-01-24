from flask import Flask, render_template, request, json,  redirect, url_for, session

from Model.users import from_string
from Model.creditCard import card_from_string
from config import app, specified_port
import socket


@app.route('/')  # prepravljeno
def main():
    s = socket.socket()
    # connect to the server on local computer
    s.connect(('127.0.0.1', specified_port))
    if "user" in session:
        s.close()
        return redirect(url_for("userHome"))
    else:
        cNumber = "4242 4242 4242 4242"
        send_string = "req-1|" + cNumber
        x = send_string.encode()
        s.sendall(x)
        print("This hit")
        tmp = s.recv(2048)
        found_cd = card_from_string(tmp.decode("utf-8"))
        print("This hit")
        s.close()
        return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])  #prepravljeno
def register():
    if request.method == "POST":
        try:
            _name = request.form["name"]
            _surname = request.form["surname"]
            _email = request.form["email"]
            _password = request.form["password"]
            _address = request.form["address"]
            _city = request.form["city"]
            _country = request.form["country"]
            _telephone = request.form["tel"]

            if _name and _surname and _email and _password and _address and _city and _country and _telephone:
                #OVO ISTO SLATI SERVERU I CEKATI ODGOVOR
                msg = "req-2|" + _name + "|" + _surname + "|" + _email + "|" + _password + "|" + _address + "|" \
                      + _city + "|" +_country + "|" + _telephone
                s = socket.socket()
                # connect to the server on local computer
                s.connect(('127.0.0.1', specified_port))
                s.send(msg.encode())
                # found_user = users.query.filter_by(email=_email).first()
                msg = s.recv(2048)
                s.close()
                msg = msg.decode("utf-8")
                if(msg == "User with this email already exists."):
                    error = msg
                    return render_template('register.html', error=error)
                #if found_user:
                #    error = "User with this email already exists."
                #    return render_template('register.html', error=error)
                #else:
                #    usr = users(_name, _surname, _email, _password, _address, _city, _country, _telephone)
                #    db.session.add(usr)
                #    db.session.commit()
                if(msg == "success"):
                    return redirect(url_for("login"))
            else:
                 error = "Every field must be filed."
                 return render_template('register.html', error=error)
        except Exception as e:
            return "Error"
    else:
         if "user" in session:
            return redirect(url_for("userHome"))
         else:
            return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])# prepravljeno
def login():
     if request.method == "POST":
        if request.form["emailLogIn"] and request.form["passwordLogIn"]:
            #OVO SE ISTO SALJE SERVERU I CEKA SE ODGOVOR
            msg = "req-3|" + request.form["emailLogIn"] + "|" + request.form["passwordLogIn"]
            s = socket.socket()
            # connect to the server on local computer
            s.connect(('127.0.0.1', specified_port))
            s.send(msg.encode())
            msg = s.recv(2048)
            msg = msg.decode("utf-8")
            s.close()
            if(msg == "Wrong email address and/or password."):
                error = msg
                return render_template('login.html', error=error)
            #found_user = users.query.filter_by(email=request.form["emailLogIn"]).first()
            else:
                session["user"] = msg
                return redirect(url_for("userHome"))
        else:
            error = "Wrong email address or/and password."
            return render_template('login.html', error=error)
     else:
        if "user" in session:
            return redirect(url_for("userHome"))
        else:
            return render_template('login.html')


@app.route('/userHome')# prepravljeno
def userHome():
    if "user" in session:
        user = session["user"]
        #OVO ISTO SE SIGURNO SALJE SERVERU
        msg = "req-4|" + user
        s = socket.socket()
        # connect to the server on local computer
        s.connect(('127.0.0.1', specified_port))
        s.send(msg.encode())
        msg = s.recv(2048)
        s.close()
        found_user = from_string(msg.decode("utf-8"))
        #found_user =
        #found_user = users.query.filter_by(email=user).first()
        return render_template('userHome.html', user=found_user.firstName, amount=found_user.amount)
    else:
         return redirect(url_for("login"))   

@app.route('/logout') # prepravljeno
def logout():
    session.pop("user", None)
    return redirect(url_for('main'))   

@app.route('/modifyProfile', methods=['POST', 'GET']) #NIJE prepravljeno
def modifyProfile():
    if request.method == "POST":
        try:
            _name = request.form["nameModify"]
            _surname = request.form["surnameModify"]
            _password = request.form["passwordModify"]
            _address = request.form["addressModify"]
            _city = request.form["cityModify"]
            _country = request.form["countryModify"]
            _telephone = request.form["telModify"]

            user = session["user"]
            #SLATI SERVERU
            msg = "req-5|" + user + "|" + _name + "|"+ _surname + "|"+ _password + "|"
            msg = msg + _address + "|"+ _city + "|"+ _country + "|" + _telephone
            s = socket.socket()
            # connect to the server on local computer
            s.connect(('127.0.0.1', specified_port))
            s.send(msg.encode())
            msg = s.recv(2048)
            msg = msg.decode("utf-8")
            s.close()
            if("err||" in msg):
                error = "Every field must be filled."
                m = msg
                m.removeprefix("err||")
                found_user = from_string(m)
                return render_template('modifyProfile.html', fn=found_user.firstName, ln=found_user.lasttName, email=found_user.email, password=found_user.password,
                address=found_user.address, country=found_user.country, city=found_user.city, tel=found_user.telephone, verified=found_user.verified, error=error)
            else:
                found_user = from_string(msg)
                error = ""
                return render_template('modifyProfile.html', fn=found_user.firstName, ln=found_user.lasttName, email=found_user.email, password=found_user.password,
                address=found_user.address, country=found_user.country, city=found_user.city, tel=found_user.telephone, verified=found_user.verified, error=error)
        except Exception as e:
            return "Error"
    else:
        if "user" in session:
            user = session["user"]
            #SLATI SERVERU
            #found_user = users.query.filter_by(email=user).first()
            msg = "req-6|" + user
            s = socket.socket()
            # connect to the server on local computer
            s.connect(('127.0.0.1', specified_port))
            s.send(msg.encode())
            msg = s.recv(2048)
            s.close()
            found_user = from_string(msg.decode("utf-8"))
            return render_template('modifyProfile.html', fn=found_user.firstName, ln=found_user.lasttName, email=found_user.email, password=found_user.password, 
                    address=found_user.address, country=found_user.country, city=found_user.city, tel=found_user.telephone, amount=found_user.amount, 
                    verified=found_user.verified)
        else:
            return redirect(url_for("login")) 

@app.route('/addCreditCard', methods=['POST', 'GET']) #PREBACENO
def addCreditCard():
    if request.method == "POST":
        try:
            _cdNumber = request.form["cdNumber"]
            _cdName = request.form["cdName"]
            _expDate = request.form["expDate"]
            _securityCode = request.form["securityCode"]
            
            if _cdNumber and _cdName and _expDate and _securityCode:
                #SLATI SERVERU
                msg = "req-7|" + _cdNumber
                s = socket.socket()
                # connect to the server on local computer
                s.connect(('127.0.0.1', specified_port))
                s.send(msg.encode())
                msg = s.recv(2048)
                msg = msg.decode("utf-8")
                s.close()
                if(msg == "none"):
                    found_cd = None
                else:
                    found_cd = card_from_string(msg)
                #found_cd = creditCard.query.filter_by(cdNumber=_cdNumber).first()
                if found_cd != None and _cdNumber == found_cd.cdNumber and _cdName == found_cd.cdName and _expDate == found_cd.expDate and _securityCode == found_cd.securityCode:
                    error = "Wrong credentials for credit card."
                    return render_template('addCreditCard.html', error=error)
                else:
                    user = session["user"]
                    msg = "req-8|" + user +"|" + _cdNumber
                    s = socket.socket()
                    # connect to the server on local computer
                    s.connect(('127.0.0.1', specified_port))
                    s.send(msg.encode())
                    msg = s.recv(2048)
                    return redirect(url_for("userHome"))
            else:
                 error = "Every field must be filed."
                 return render_template('addCreditCard.html', error=error)     
        except Exception as e:
            return "Error"
    else:
        if "user" in session:
            user = session["user"]
            #slati serveru
            msg = "req-9|" + user
            s = socket.socket()
            # connect to the server on local computer
            s.connect(('127.0.0.1', specified_port))
            s.send(msg.encode())
            msg = s.recv(2048)
            msg = msg.decode("utf-8")
            s.close()
            found_user = from_string(msg)
            #
            #found_user = users.query.filter_by(email=user).first()
            if (found_user.verified):
                return render_template("addCreditCardError.html")
            else:
                return render_template("addCreditCard.html")
        else:
            return redirect(url_for("login"))

@app.route('/market')#NEMA STA ZA SAD
def market():
    if "user" in session:
        user = session["user"]
        return render_template('market.html', user=user)
    else:
        return redirect(url_for("login"))

@app.route('/deposit', methods=['POST', 'GET'])#NIJE PREBACENO
def deposit():
    if request.method == "POST":
        user = session["user"]
        #slati serveru
        msg = "req-10|" + user
        s = socket.socket()
        # connect to the server on local computer
        s.connect(('127.0.0.1', specified_port))
        s.send(msg.encode())
        msg = s.recv(2048)
        msg = msg.decode("utf-8")
        s.close()
        found_user = from_string(msg)
        #found_user = users.query.filter_by(email=user).first()
        if (found_user.verified == True):
            try:
                _deposit = request.form["deposit"]
                if _deposit:
                    #slati serveru
                    msg = "req-11|" + user + "|" + _deposit
                    s.send(msg.encode())
                    msg = s.recv(2048)
                    msg = msg.decode("utf-8")
                    #
                    #found_cd = creditCard.query.filter_by(cdNumber=found_user.cdNumber).first()
                    if (msg == "success"):
                        return redirect(url_for("userHome")) 
                    else:
                        error = "Deposit failed. Not enough money on card."
                        return render_template('deposit.html', error=error)  
                else:
                    error = "Every field must be filed."
                    return render_template('deposit.html', error=error)  
            except Exception as e:
                return "Error"
        else:
            error = "User is not verified!"
            return render_template('deposit.html', error=error)   
    else:
        if "user" in session:
            return render_template('deposit.html')
        else:
            return redirect(url_for("login"))

@app.route('/status')#NIJE PREBACENO
def status():
    if "user" in session:
        user = session["user"]
        # slati serveru
        msg = "req-12|" + user
        s = socket.socket()
        # connect to the server on local computer
        s.connect(('127.0.0.1', specified_port))
        s.send(msg.encode())
        msg = s.recv(2048)
        msg = msg.decode("utf-8")
        s.close()
        if(msg == "failure"):
            return render_template('statusError.html')
        else:
            found_cd = card_from_string(msg)
            return render_template('status.html', cdName=found_cd.cdName, expDate=found_cd.expDate,
                                   amount=found_cd.cardAmount)
    else:
        return redirect(url_for("login"))

@app.route('/trade') #NE TREBA ZA SAD
def trade():
    if "user" in session:
        user = session["user"]
        return render_template('trade.html', user=user)
    else:
        return redirect(url_for("login"))

@app.route('/transactions') #NE TREBA ZA SAD
def transactions():
    if "user" in session:
        user = session["user"]
        return render_template('transactions.html', user=user)
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":

    print("Supposedly connected to server")
    app.run(port=5000,debug=True)