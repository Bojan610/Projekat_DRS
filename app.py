from os import error
from typing import Counter
from flask import Flask, render_template, request, json,  redirect, url_for, session

from Model.users import users
from Model.creditCard import creditCard
from config import db, app


@app.route('/')
def main():
     if "user" in session:
        return redirect(url_for("userHome"))
     else:
        return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
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
                found_user = users.query.filter_by(email=_email).first()
                if found_user:
                    error = "User with this email already exists."
                    return render_template('register.html', error=error)
                else:
                    usr = users(_name, _surname, _email, _password, _address, _city, _country, _telephone)
                    db.session.add(usr)
                    db.session.commit()
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

@app.route('/login', methods=['POST', 'GET'])
def login():
     if request.method == "POST":
        if request.form["emailLogIn"] and request.form["passwordLogIn"]:
            found_user = users.query.filter_by(email=request.form["emailLogIn"]).first()
            if found_user != None and request.form["emailLogIn"] == found_user.email and request.form["passwordLogIn"] == found_user.password:
                session["user"] = found_user.email
                return redirect(url_for("userHome"))  
            else:
                error = "Wrong email address or/and password."
                return render_template('login.html', error=error)
        else:
            error = "Wrong email address or/and password."
            return render_template('login.html', error=error)
     else:
        if "user" in session:
            return redirect(url_for("userHome"))
        else:
            return render_template('login.html')

@app.route('/userHome')
def userHome():
    if "user" in session:
        user = session["user"]
        return render_template('userHome.html', user=user)
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
            found_user = users.query.filter_by(email=user).first()
            if (_name and _surname and _password and _address and _city and _country and _telephone):               
                found_user.firsName = _name
                found_user.lasttName = _surname
                found_user.password = _password
                found_user.address = _address
                found_user.country = _country
                found_user.city = _city
                found_user.telephone = _telephone
                db.session.commit()
                return redirect(url_for("userHome"))   
            else:
                error = "Every field must be filed."
                return render_template('modifyProfile.html', fn=found_user.firstName, ln=found_user.lasttName, email=found_user.email, password=found_user.password, 
                    address=found_user.address, country=found_user.country, city=found_user.city, tel=found_user.telephone, amount=found_user.amount, 
                    verified=found_user.verified, error=error)
        except Exception as e:
            return "Error"
    else:
        if "user" in session:
            user = session["user"]
            found_user = users.query.filter_by(email=user).first()
            return render_template('modifyProfile.html', fn=found_user.firstName, ln=found_user.lasttName, email=found_user.email, password=found_user.password, 
                    address=found_user.address, country=found_user.country, city=found_user.city, tel=found_user.telephone, amount=found_user.amount, 
                    verified=found_user.verified)
        else:
            return redirect(url_for("login")) 

@app.route('/addCreditCard', methods=['POST', 'GET'])
def addCreditCard():
    if request.method == "POST":
        try:
            _cdNumber = request.form["cdNumModify"]
            _cdName = request.form["cdNameModify"]
            _expDate = request.form["expModify"]
            _securityCode = request.form["codeModify"]
            
            if _cdNumber and _cdName and _expDate and _securityCode:
                found_user = creditCard.query.filter_by(cdNumber=_cdNumber).first()
                if found_user:               
                    error = "User with this credit card number already exists."
                    return render_template('addCreditCard.html', error=error)
                else:
                    usr = creditCard(_cdNumber,_cdName,_expDate,_securityCode)
                    db.session.add(usr)
                    db.session.commit()
                    return redirect(url_for("modifyProfile"))   
        except Exception as e:
            return "Error"
    else:
        return redirect(url_for("modifyProfile"))
@app.route('/market')
def market():
    if "user" in session:
        user = session["user"]
        return render_template('market.html', user=user)
    else:
        return redirect(url_for("login"))
@app.route('/depositWithdraw')
def depositWithdraw():
    if "user" in session:
        user = session["user"]
        return render_template('depositWithdraw.html', user=user)
    else:
        return redirect(url_for("login"))
@app.route('/status')
def status():
    if "user" in session:
        user = session["user"]
        return render_template('status.html', user=user)
    else:
        return redirect(url_for("login"))
@app.route('/trade')
def trade():
    if "user" in session:
        user = session["user"]
        return render_template('trade.html', user=user)
    else:
        return redirect(url_for("login"))
@app.route('/transactions')
def transactions():
    if "user" in session:
        user = session["user"]
        return render_template('transactions.html', user=user)
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(port=5000,debug=True)
