from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector 
import json


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://teste:AbCd!12345@localhost/teste'
db = SQLAlchemy(app)

class Livros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), unique=True, nullable=False)
    autor = db.Column(db.String(50), nullable=False)

