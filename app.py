from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response, send_from_directory
from contextlib import closing
import sqlite3
import os
import werkzeug


app = Flask(__name__)





@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/calendario')
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
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return render_template("/login.html", erro="")
        # Monta a resposta.
    return render_template("agendamento.html", logado = logado, mensagem = "")
    


@app.route("/login", methods = ["POST"])
def login():
    # Extrai os dados do formulário.
    f = request.form
    if "email" not in f or "senha" not in f:
        return ":(", 422
    login = f["email"]
    senha = f["senha"]

    # Faz o processamento.
    logado = db_fazer_login(login, senha)

    # Monta a resposta.
    if logado is None:
        return render_template("login.html", erro = "Ops. A senha estava errada.")
    resposta = make_response(redirect("/agendamento"))

    # Armazena o login realizado com sucesso em cookies (autenticação).
    resposta.set_cookie("login", login, samesite = "Strict")
    resposta.set_cookie("senha", senha, samesite = "Strict")
    return resposta

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # Monta a resposta.
    resposta = make_response(render_template("index.html", mensagem = "Tchau."))

    # Limpa os cookies com os dados de login (autenticação).
    resposta.set_cookie("login", "", samesite = "Strict")
    resposta.set_cookie("senha", "", samesite = "Strict")
    return resposta



@app.route('/users', methods=['GET', 'POST'])
def criar_cliente():
    
    # Extrai os dados do formulário.
    nome = request.form["nome"]
    email = request.form["email"]
    data_nascimento = request.form["data_nascimento"]
    senha = request.form["confirmar-senha"]
    
    # Faz o processamento.
    ja_existia, cliente = criar_cliente(nome, email, data_nascimento, senha)
    
    print(ja_existia)
    # Monta a resposta.
    mensagem = f"O email já existe." if ja_existia else f"O login foi criada com sucesso."
    return render_template("login.html", mensagem = mensagem)



@app.route('/add', methods=['GET', 'POST'])
def criar_agendamento():
    
    # Extrai os dados do formulário.
    data = request.form["data"]
    hora = request.form["hora"]
    servico = request.form["servico"]
    funcionario = request.form["funcionario"]
    


    # Faz o processamento.
    ja_existia, agendamento = criar_agendamento(data, hora, servico, funcionario)

    # Monta a resposta.
    mensagem = f"o agendamento {data}{hora}{funcionario} já existia com o id {agendamento['id_agendamento']}." if ja_existia else f"O agendamento {data}{hora}{funcionario} foi criada com id {agendamento['id_agendameto']}."
    return render_template("agendamento.html", logado = logado, mensagem = mensagem, funcionarios = funcionarios)


@app.route('/historico')
def historico():
    return render_template('historico.html')



###############################################
#### Coisas internas da controller da API. ####
###############################################

def extensao_arquivo(filename):
    if '.' not in filename: return ''
    return filename.rsplit('.', 1)[1].lower()

def salvar_arquivo_upload():
    import uuid
    if "foto" in request.files:
        foto = request.files["foto"]
        e = extensao_arquivo(foto.filename)
        if e in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
            u = uuid.uuid1()
            n = f"{u}.{e}"
            foto.save(os.path.join("alunos_fotos", n))
            return n
    return ""

def deletar_foto(id_foto):
    if id_foto == '': return
    p = os.path.join("alunos_fotos", id_foto)
    if os.path.exists(p):
        os.remove(p)

def autenticar_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    return db_fazer_login(login, senha)


##########################################
#### Definições de regras de negócio. ####
##########################################

def criar_cliente(nome, email, data_nascimento, senha):
    cliente_ja_existe = db_verificar_cliente(nome, email, data_nascimento, senha)
    if cliente_ja_existe is not None: return True, cliente_ja_existe
    serie_nova = db_criar_cliente(nome, email, data_nascimento, senha)
    return False, serie_nova


def criar_agendamento(data, hora, id_cliente, servico, funcionario):
    serie_ja_existe = db_verificar_agendamento(data, hora, id_cliente, servico, funcionario)
    if serie_ja_existe is not None: return True, serie_ja_existe
    novo_agendamento = db_criar_agendamento(data, hora, id_cliente, servico, funcionario)
    return False, novo_agendamento


###############################################
#### Funções auxiliares de banco de dados. ####
###############################################

# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

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


    REPLACE INTO funcionario (id_funcao,nome,cpf,email,endereco,telefone,status,senha) VALUES ('1','Tony Stark', '31737797895', 'spveiok@hotmail.com','rua das camelis', '235645', 'ativo', '123456');


"""


def conectar():
    return sqlite3.connect('agenda.db')


def db_inicializar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit()


def db_verificar_cliente(nome, email, data_nascimento, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome, email, data_nascimento, senha FROM cliente WHERE nome = ? AND email = ? AND senha = ?", [nome, email, senha])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_agendamento(data, hora, id_cliente, servico, funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_agendamento, data, hora, id_cliente, servico, funcionario FROM agendamento WHERE data = ? AND hora = ? AND funcionario = ?", [data, hora, funcionario])
        return row_to_dict(cur.description, cur.fetchone())


def db_criar_cliente(nome, email, data_nascimento, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cliente (nome, email, data_nascimento, senha) VALUES (?, ?, ?, ?)", [nome, email, data_nascimento, senha])
        id_cliente = cur.lastrowid
        con.commit()
        return {'id_cliente': id_cliente, 'nome': nome, 'email': email, 'data_nascimento': data_nascimento, 'senha':senha}


def db_criar_agendamento(data, hora, servico, funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO agendamento (data, hora, servico, funcionario) VALUES (?, ?, ?, ?, ?)", [data, hora, servico, funcionario])
        id_cliente = cur.lastrowid
        con.commit()
        return {'id_agendamento':id_agendamento, 'data':data, 'hora':hora, 'id_cliente':id_cliente,'servico':servico, 'funcionario':funcionario}


def db_fazer_login(email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.email, c.senha, c.nome FROM cliente c WHERE c.email = ? AND c.senha = ?", [email, senha])
        return row_to_dict(cur.description, cur.fetchone())


if __name__ == '__main__':
    db_inicializar()
    app.run(debug=True)    