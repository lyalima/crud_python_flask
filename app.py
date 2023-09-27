#instalação das libs necessárias:
#pip install flask
#pip install -U Flask-SQLAlchemy
#pip install mysql-python
#pip install mysql-connector-python
#pip install mysqlclient==1.4.6

#importação das libs necessárias
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector 
import json

#criação do app flask
app = Flask(__name__)
app.app_context().push()
#configuração do banco de dados(já deve estar criado)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://teste:AbCd!12345@localhost/teste'
db = SQLAlchemy(app)

#criação da classe que será a tabela do banco de dados
class Livros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), unique=True, nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    #após modelar a classe deve ir no terminal do venv e executar "db.create_all()"

    #método que retorna a tabela em json após ela ser criada
    def to_json(self):
        return {"id": self.id, "titulo": self.titulo, "autor": self.autor}

#endpoints testados no postman

#api para selecionar todos os livros
@app.route("/livros", methods=["GET"])
def selecionar_livros():
    livros_objetos = Livros.query.all()
    livros_json = [livro.to_json() for livro in livros_objetos]
    return gera_response(200, "livros", livros_json, "ok")

#api para selecionar apenas um livro por id
@app.route("/livro/<id>", methods=["GET"])
def selecionar_livro(id):
    livro_objeto = Livros.query.filter_by(id=id).first()
    livro_json = livro_objeto.to_json()
    return gera_response(200, "livro", livro_json)

#api para criar um novo livro
@app.route("/livro", methods=["POST"])
def criar_livro():
    body = request.get_json()

    try:
        livro = Livros(titulo=body["titulo"], autor=body["autor"])
        db.session.add(livro)
        db.session.commit()
        return gera_response(201, "livro", livro.to_json(), "Livro criado com sucesso")
    except Exception as e:
        print(f'Erro: {e}')
        return gera_response(400, "livro", {}, "Erro ao cadastrar o livro")

#api para atualizar um livro por id
@app.route("/livro/<id>", methods=["PUT"])
def atualizar_livro(id):
    body = request.get_json()

    try:
        livro_objeto = Livros.query.filter_by(id=id).first()
        if 'titulo' in body:
            livro_objeto.titulo = body["titulo"]
        if 'autor' in body:
            livro_objeto.autor = body["autor"]

        db.session.add(livro_objeto)
        db.session.commit()
        return gera_response(200, "livro", livro_objeto.to_json(), "Livro atualizado com sucesso")
    except Exception as e:
        print(f'Erro: {e}')
        return gera_response(400, "livro", {}, "Erro ao atualizar livro")
    
#api para deletar um livro por id
@app.route("/livro/<id>", methods=["DELETE"])
def deletar_livro(id):
    livro_objeto = Livros.query.filter_by(id=id).first()

    try:
        db.session.delete(livro_objeto)
        db.session.commit()
        return gera_response(200, "livro", livro_objeto.to_json(), "Livro detelado com sucesso")
    except Exception as e:
        print(f'Erro: {e}')
        return gera_response(400, "livro", {}, "Erro ao deletar livro")

#função que gera a response para o usuário
def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

#comando para subir o servidor flask no localhost
app.run(debug=True)

