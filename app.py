from os import error
from typing import Counter
from flask import Flask, render_template, request, json,  redirect, url_for

app = Flask(__name__)

@app.route('/')
def main():
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
                return redirect(url_for("login"))      
            else:
                 error = "Every field must be filed."
                 return render_template('register.html', error=error)
        except Exception as e:
            return "Error"
    else:
         return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
     if request.method == "POST":
        if  request.form["emailLogIn"] == "Admin@gmail.com" and request.form["passwordLogIn"] == "Admin":
            return "<h2>Hello Admin@gmail.com!</h2>"
        else:
            error = "Wrong email address or/and password."
            return render_template('login.html', error=error)
     else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(port=5000)
