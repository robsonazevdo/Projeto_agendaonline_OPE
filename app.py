from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from contextlib import closing
import sqlite3
import os
import werkzeug




app = Flask(__name__)



        

@app.route('/')
def inicio():
    return render_template('index.html')



@app.route("/login")
def menu():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return render_template("/login.html", erro = "")

    # Monta a resposta.
    return render_template("menu.html", logado = logado, mensagem = "")

@app.route("/login", methods = ["POST"])
def login():
    # Extrai os dados do formulário.
    f = request.form
    if "login" not in f or "senha" not in f:
        return ":(", 422
    login = f["login"]
    senha = f["senha"]

    # Faz o processamento.
    logado = db_fazer_login(login, senha)

    # Monta a resposta.
    if logado is None:
        return render_template("login.html", erro = "Ops. A senha estava errada.")
    resposta = make_response(redirect("/"))

    # Armazena o login realizado com sucesso em cookies (autenticação).
    resposta.set_cookie("login", login, samesite = "Strict")
    resposta.set_cookie("senha", senha, samesite = "Strict")
    return resposta

    

@app.route('/users', methods=['GET', 'POST'])
def criar_serie_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome = request.form["nome"]
    email = request.form["email"]
    numero = request.form["numero"]
    endereco = request.form["endereco"]


    # Faz o processamento.
    ja_existia, serie = criar_serie(numero, turma)

    # Monta a resposta.
    mensagem = f"A série {numero}{turma} já existia com o id {serie['id_serie']}." if ja_existia else f"A série {numero}{turma} foi criada com id {serie['id_serie']}."
    return render_template("menu.html", logado = logado, mensagem = mensagem)







#### Definições básicas do banco. ####

sql_create = """ 
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    logradouro VARCHAR(50) NOT NULL,
    numero INTEGER NOT NULL,
    cep VARCHAR(9) NOT NULL,
    complemento VARCHAR(50) NOT NULL,
    senha VARCHAR(20) NOT NULL,
    UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS funcao (
    id_funcao INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_funcao VARCHAR(50) NOT NULL

);

CREATE TABLE IF NOT EXISTS servico (
    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_sevico VARCHAR(50) NOT NULL,
    preco_servico REAL NOT NULL,
    duracao_servico DATETIME NOT NULL

);

CREATE TABLE IF NOT EXISTS funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_funcao INTEGER NOT NULL,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    email VARCHAR(50) NOT NULL,
    logradouro VARCHAR(50) NOT NULL,
    numero INTEGER NOT NULL,
    cep VARCHAR(9) NOT NULL,
    complemento VARCHAR(50) NOT NULL,
    senha VARCHAR(20) NOT NULL,
    UNIQUE(email),
    FOREIGN KEY (id_funcao) REFERENCES funcao(id_funcao)

);

CREATE TABLE IF NOT EXISTS servico_funcionario (
    id_servico INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario),
    PRIMARY KEY (id_servico, id_funcionario)
);

CREATE TABLE IF NOT EXISTS agendamento (
    id_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    id_cliente INTEGER NOT NULL,
    observaçao VARCHAR(150),
    id_servico INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_servico, id_funcionario) REFERENCES servico_funcionario(id_servico, id_funcionario)
);


"""



def conectar():
    return sqlite3.connect('agenda.db')

def db_inicializar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit()





if __name__ == '__main__':
    db_inicializar()
    app.run(debug=True)    