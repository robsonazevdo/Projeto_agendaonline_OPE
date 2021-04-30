from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response, send_from_directory
from contextlib import closing
import sqlite3
import os
import werkzeug


app = Flask(__name__)








@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/agenda')
def agenda():
    return render_template('calendario.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro_cliente.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/cadastro_funcionario')
def cadastro_funcionario():
    return render_template('cadastro_funcionario.html')


@app.route('/servico')
def cadastro_servico():
    return render_template('servico.html')
    

@app.route('/funcao')
def cadastro_funcao():
    return render_template('funcao.html')    


@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')

@app.route('/historico')
def historico():
    return render_template('historico.html')

@app.route("/login")
def menu():
    return render_template("/login.html", erro="")
'''   # Autenticação.
    logado = autenticar_login()
    if logado is None:

    # Monta a resposta.
    return render_template("menu.html", logado = logado, mensagem = "")
'''
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
    senha VARCHAR(10) NOT NULL,
    data_nascimento TEXT NOT NULL,
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
    duracao_servico TEXT NOT NULL,
    status VARCHAR(7) NOT NULL

);

CREATE TABLE IF NOT EXISTS funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_funcao INTEGER NOT NULL,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    email VARCHAR(50) NOT NULL,
    endereco VARCHAR(50) NOT NULL,
    telefone VARCHAR(12) NOT NULL,
    status VARCHAR(7) NOT NULL,
    senha VARCHAR(8) NOT NULL,
    UNIQUE(email),
    FOREIGN KEY (id_funcao) REFERENCES funcao(id_funcao)

);

CREATE TABLE IF NOT EXISTS servico_funcionario (
    id_servico_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_servico INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
    
);

CREATE TABLE IF NOT EXISTS agendamento (
    id_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
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