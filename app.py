import requests
from flask import Flask, render_template, request, redirect, url_for, session
import time
from Model.transaction import transaction, transaction_to_string
from Model.users import from_string
from Model.creditCard import card_from_string
from config import engine_address
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "user"

@app.route('/')  # prepravljeno
def main():
    if "user" in session:
        return redirect(url_for("userHome"))
    else:
        adresa = engine_address
        cNumber = "4242 4242 4242 4242"
        adresa += '/first'
        r = requests.post(adresa,data = cNumber)
        tmp = r.content.decode()
        found_cd = card_from_string(tmp)
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
                msg = _name + "|" + _surname + "|" + _email + "|" + _password + "|" + _address + "|" \
                      + _city + "|" +_country + "|" + _telephone
                adresa = engine_address
                adresa += '/second'
                r = requests.post(adresa, data=msg.encode("utf-8"))
                msg = r.content
                msg = msg.decode("utf-8")
                if(msg == "User with this email already exists."):
                    error = msg
                    return render_template('register.html', error=error)
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
            msg = request.form["emailLogIn"] + "|" + request.form["passwordLogIn"]
            adresa = engine_address
            adresa += '/third'
            r = requests.post(adresa, data=msg.encode("utf-8"))
            msg = r.content
            msg = msg.decode("utf-8")
            if(msg == "Wrong email address and/or password."):
                error = msg
                return render_template('login.html', error=error)
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
        msg = user
        adresa = engine_address
        adresa += '/fourth'
        r = requests.post(adresa, data=msg.encode("utf-8"))
        msg = r.content
        found_user = from_string(msg.decode("utf-8"))
        return render_template('userHome.html', user=found_user.firstName, amount=found_user.amount)
    else:
         return redirect(url_for("login"))   

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('main'))   

@app.route('/modifyProfile', methods=['POST', 'GET'])
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
            msg = user + "|" + _name + "|"+ _surname + "|"+ _password + "|"
            msg = msg + _address + "|"+ _city + "|"+ _country + "|" + _telephone
            adresa = engine_address
            adresa += '/fifth'
            r = requests.post(adresa, data=msg.encode("utf-8"))
            msg = r.content.decode()
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
            msg = user
            adresa = engine_address
            adresa += '/sixth'
            r = requests.post(adresa, data=msg.encode("utf-8"))
            msg = r.content
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
                msg = _cdNumber
                adresa = engine_address
                adresa += '/seventh'
                r = requests.post(adresa, data=msg.encode("utf-8"))
                msg = r.content.decode("utf-8")
                if(msg == "none"):
                    found_cd = None
                else:
                    found_cd = card_from_string(msg)
                if found_cd != None and _cdNumber == found_cd.cdNumber and _cdName == found_cd.cdName and _expDate == found_cd.expDate and _securityCode == found_cd.securityCode:
                    user = session["user"]
                    msg = user +"|" + _cdNumber
                    adresa = engine_address
                    adresa += '/eighth'
                    r = requests.post(adresa, data=msg.encode("utf-8"))
                    msg = r.content.decode("utf-8")
                    return redirect(url_for("userHome"))
                else:
                    error = "Wrong credentials for credit card."
                    return render_template('addCreditCard.html', error=error)
            else:
                 error = "Every field must be filed."
                 return render_template('addCreditCard.html', error=error)     
        except Exception as e:
            return "Error"
    else:
        if "user" in session:
            user = session["user"]
            msg = user
            adresa = engine_address
            adresa += '/ninth'
            r = requests.post(adresa, data=msg.encode("utf-8"))
            msg = r.content.decode("utf-8")
            found_user = from_string(msg)
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


# Funkcija koja koja nalazi cenu valute
def get_crypto_price(coin):

    url = "https://www.google.com/search?q=" + coin + "+price"

    HTML = requests.get(url)

    soup = BeautifulSoup(HTML.text, 'html.parser')

    text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find("div",attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    return text

@app.route('/deposit', methods=['POST', 'GET'])
def deposit():
    if request.method == "POST":
        user = session["user"]
        msg = user
        adresa = engine_address
        adresa += '/tenth'
        r = requests.post(adresa, data=msg.encode("utf-8"))
        msg = r.content.decode("utf-8")
        found_user = from_string(msg)
        if (found_user.verified == True):
            try:
                _deposit = request.form["deposit"]
                if _deposit:
                    msg = user + "|" + _deposit
                    adresa = engine_address
                    adresa += '/eleventh'
                    r = requests.post(adresa, data=msg.encode("utf-8"))
                    msg = r.content.decode("utf-8")
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

@app.route('/status')
def status():
    if "user" in session:
        user = session["user"]
        msg = user
        adresa = engine_address
        adresa += '/twelveth'
        r = requests.post(adresa, data=msg.encode("utf-8"))
        msg = r.content
        msg = msg.decode("utf-8")
        if(msg == "failure"):
            return render_template('statusError.html')
        else:
            found_cd = card_from_string(msg)
            return render_template('status.html', cdName=found_cd.cdName, expDate=found_cd.expDate,
                                   amount=found_cd.cardAmount)
    else:
        return redirect(url_for("login"))

@app.route('/trade', methods=['POST', 'GET'])
def trade():
    if request.method == "POST":
        user = session["user"]
        adresa = engine_address
        adresa += '/tenth'
        r = requests.post(adresa, data=user.encode("utf-8"))
        found_user = r.content.decode("utf-8")
        found_user = from_string(found_user)

        try:
            _tradeEmail = request.form["tradeEmail"]
            _tradeAmount = request.form["tradeAmount"]

            if _tradeEmail and _tradeAmount:
                adresa = engine_address
                adresa += '/tenth'
                r = requests.post(adresa, data=_tradeEmail.encode("utf-8"))
                _found_user_receiver = r.content.decode("utf-8")
                _found_user_receiver = from_string(_found_user_receiver)
                #_found_user_receiver = users.query.filter_by(email=_tradeEmail).first()
                if (_found_user_receiver == None or _found_user_receiver.verified == False):
                    error = "Transaction failed."
                    adresa = engine_address
                    adresa += '/thirteenth'
                    tr = transaction(found_user.email, _tradeEmail, int(_tradeAmount), "Odbijeno")
                    msg = transaction_to_string(tr)
                    r = requests.post(adresa, data=msg.encode("utf-8"))
                    return render_template('trade.html', error=error)

                if (found_user.amount - int(_tradeAmount) < 0):
                    error = "Transaction failed. Not enough money."
                    tr = transaction(found_user.email, _tradeEmail, int(_tradeAmount), "Odbijeno")
                    msg = transaction_to_string(tr)
                    adresa = engine_address
                    adresa += '/thirteenth'
                    r = requests.post(adresa, data=msg.encode("utf-8"))
                    return render_template('trade.html', error=error)

                tr = transaction(found_user.email, _tradeEmail, int(_tradeAmount), "U obradi")
                adresa = engine_address
                adresa += '/fourteenth'
                msg = transaction_to_string(tr) + "," + found_user.email + "|" + _tradeEmail
                r = requests.post(adresa, data=msg.encode("utf-8"))

                return redirect(url_for("userHome"))

            else:
                error = "Every field must be filed."
                return render_template('trade.html', error=error)
        except Exception as e:
            return "Error"
    else:
        if "user" in session:
            user = session["user"]
            adresa = engine_address
            adresa += '/tenth'
            r = requests.post(adresa, data=user.encode("utf-8"))
            found_user = r.content.decode("utf-8")
            found_user = from_string(found_user)
            if (found_user.verified == True):
                return render_template('transaction.html')
            else:
                return render_template('statusError.html')
        else:
            return redirect(url_for("login"))

@app.route('/transactions', methods=['POST', 'GET'])
def transactions():
    if request.method == "POST":
        return "Post"
    else:
        if "user" in session:
            user = session["user"]
            adresa = engine_address
            adresa += '/tenth'
            r = requests.post(adresa,data = user.encode("utf-8"))
            found_user = r.content.decode("utf-8")
            found_user = from_string(found_user)
            if (found_user.verified == True):
                return render_template('transactions.html')
            else:
                return render_template('statusError.html')
        else:
            return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=5000,debug=True)