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

    def to_json(self):
        return {"id": self.id, "titulo": self.titulo, "autor": self.autor}


#selecionar todos os livros
@app.route("/livros", methods=["GET"])
def selecionar_livros():
    livros_objetos = Livros.query.all()
    livros_json = [livro.to_json() for livro in livros_objetos]
    return gera_response(200, "livros", livros_json, "ok")

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run(debug=True)

