from flask_sqlalchemy import SQLAlchemy
from flask import Flask


engine = Flask(__name__)
engine.secret_key = "user"
engine.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
engine.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(engine)

specified_port = 20000
current_address = "127.0.0.1"
engine_address = "http://" + current_address + ":" + str(specified_port)
