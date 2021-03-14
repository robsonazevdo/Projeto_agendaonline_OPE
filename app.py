from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from contextlib import closing
import sqlite3
import os
import werkzeug


app = Flask(__name__)



        
 

@app.route('/')
def inicio():
    return render_template('index.html')



    

@app.route('/users', methods=['GET', 'POST'])
def cliente():
    if request.method == "POST":
        '''cliente = TB_Cliente(nome = request.form['nome'],
                        email = request.form['email'], 
                        logradouro = request.form['endereco'], 
                        numero = request.form['numero'],
                        cep = request.form['cep'],
                        complemento = request.form['complemento'], 
                        senha = request.form['senha'])'''
        
        
        return redirect(url_for('inicio')) 






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