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


@app.route('/historico')
def historico():

    return render_template('historico.html')



@app.route('/cadastro_funcionario')
def cadastro_funcionario():
    lista = db_listar_cargo()
    lista2 = db_listar_servico()

    return render_template('cadastro_funcionario.html', cargos = lista, servicos = lista2)


@app.route('/servico')
def cadastro_servico():
    
    lista = db_listar_funcionarios()
    return render_template('servico.html', funcionarios = lista)
    
 


@app.route('/agendamento')
def agendamento():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return render_template("/login.html", erro="")

        # Faz o processamento.
    lista = db_listar_funcionarios()
    lista2 = db_listar_cliente()
    lista3 = db_listar_servico() 


        # Monta a resposta.
    return render_template("agendamento.html", logado = logado, mensagem = "", funcionarios = lista, cliente = lista2, servicos = lista3)
    




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
    
   
    # Monta a resposta.
    mensagem = f"O email já existe." if ja_existia else f"O login foi criada com sucesso."
    return render_template("login.html", mensagem = mensagem)



@app.route('/add_agendamento', methods=['GET', 'POST'])
def criar_agendamento_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    id_cliente = request.form["id_cliente"]
    data1 = request.form["data"]
    hora = request.form["hora"]
    id_servico = request.form["id_servico"]
    id_funcionario = request.form["id_funcionario"]
    

    # Faz o processamento.
    lista = db_listar_funcionarios()
    ja_existia, agendamento = criar_agendamento(data1, hora, id_cliente, id_servico, id_funcionario)


    # Monta a resposta.
    mensagem = f"o agendamento {data1}{hora} já existia com o id {agendamento['id_servico']}." if ja_existia else f"O agendamento {data1}{hora} foi criada."
    return render_template("agendamento.html", logado = logado, funcionarios = lista, mensagem = mensagem)



@app.route('/add_servico', methods=['GET', 'POST'])
def criar_servico_api():

    # Extrai os dados do formulário.
    nome_servico = request.form["nome"]
    preco_servico = request.form["preco"]
    duracao_servico = request.form["duracao"]
    status = request.form["status"]
    id_funcionario = request.form["id_funcionario"]

    id = db_trazer_ultimo_id_servico()
    if id is not None:
        i = id["id_servico"] + 1
    else:
        i = 1
    
    # Faz o processamento.
    
    ja_existia, servico = criar_servico(nome_servico, preco_servico, duracao_servico, status)
    
    if servico['id_servico'] == i:
        db_criar_servico_funcionario(i, id_funcionario)

    # Monta a resposta.
    mensagem = f"o serviço {nome_servico} já existe." if ja_existia else f"O serviço {nome_servico} foi criada com sucesso."
    return render_template("servico.html", mensagem = mensagem)



@app.route('/add_funcionario', methods=['GET', 'POST'])
def criar_funcionario_api():

    # Extrai os dados do formulário.
    nome = request.form["nome"]
    email = request.form["email"]
    endereco = request.form["endereco"]
    cpf = request.form["cpf"]
    telefone = request.form["telefone"]
    id_cargo = request.form["id_cargo"]
    status = request.form["status"]
    senha = request.form["senha"]



    # Faz o processamento.
    ja_existia, funcionario = criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status, senha)
    

    # Monta a resposta.
    mensagem = f"O Funcionario {nome} e {email} já existe." if ja_existia else f"O Funcionario {nome} foi criada com sucesso."
    return render_template("cadastro_funcionario.html", mensagem = mensagem)


@app.route('/add_cargo', methods=['GET', 'POST'])
def criar_cargo_api():

    # Extrai os dados do formulário.
    nome_cargo = request.form["nome"]
    

    # Faz o processamento.
    ja_existia, cargo = criar_cargo(nome_cargo)
    

    # Monta a resposta.
    mensagem = f"O Funcionario {nome_cargo} já existe." if ja_existia else f"O Funcionario {nome_cargo} foi criada com sucesso."
    return render_template("cadastro_funcionario.html", mensagem = mensagem)



@app.route('/buscar_cliente/<string:nome>', methods=['GET']) 
def buscar_cliente_api(nome):




    # Faz o processamento.
    h_cliente = db_listar_cliente()
    print(h_cliente,str(nome))
    if h_cliente['nome'] == nome:
        cliente = db_historico_cliente(h_cliente['id_cliente'])

    print(cliente, h_cliente)
 # Monta a resposta.
    if cliente is None:
        return render_template("historico.html", mensagem = f"Esse aluno não existe."), 404
    return render_template("historico.html", cliente = cliente)



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
    novo_cliente = db_criar_cliente(nome, email, data_nascimento, senha)
    return False, novo_cliente


def criar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario):
    serie_ja_existe = db_verificar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario)
    if serie_ja_existe is not None: return True, serie_ja_existe
    novo_agendamento = db_criar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario)
    return False, novo_agendamento


def criar_servico(nome_servico, preco_servico, duracao_servico, status):
    servico_ja_existe = db_verificar_servico(nome_servico, preco_servico, duracao_servico, status)
    if servico_ja_existe is not None: return True, servico_ja_existe
    novo_servico = db_criar_servico(nome_servico, preco_servico, duracao_servico, status)
    return False, novo_servico


def criar_servico_funcionario(i, id_funcionario):
    servico_ja_existe = db_verificar_servico_funcionario(i, id_funcionario)
    if servico_ja_existe is not None: return True, servico_ja_existe
    novo_servico = db_criar_servico_funcionario(i, id_funcionario)
    return False, novo_servico  


def criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status, senha):
    funcionario_ja_existe = db_verificar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status, senha)
    if funcionario_ja_existe is not None: return True, funcionario_ja_existe
    novo_funcionario = db_criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status, senha)
    return False, novo_funcionario   


def criar_cargo(nome_cargo):
    cargo_ja_existe = db_verificar_cargo(nome_cargo)
    if cargo_ja_existe is not None: return True, cargo_ja_existe
    novo_cargo = db_criar_cargo(nome_cargo)
    return False, novo_cargo


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

CREATE TABLE IF NOT EXISTS cargo (
    id_cargo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cargo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS servico (
    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_servico VARCHAR(50) NOT NULL,
    preco_servico REAL NOT NULL,
    duracao_servico TEXT NOT NULL,
    status VARCHAR(7) NOT NULL
);

CREATE TABLE IF NOT EXISTS funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cargo INTEGER NOT NULL,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    email VARCHAR(50) NOT NULL,
    endereco VARCHAR(50) NOT NULL,
    telefone VARCHAR(12) NOT NULL,
    status VARCHAR(7) NOT NULL,
    senha VARCHAR(8) NOT NULL,
    UNIQUE(email),
    FOREIGN KEY (id_cargo) REFERENCES cargo(id_cargo)
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
    data1 TEXT NOT NULL,
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


def db_verificar_cliente(nome, email, data_nascimento, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome, email, data_nascimento, senha FROM cliente WHERE nome = ? AND email = ? AND senha = ?", [nome, email, senha])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_agendamento(data1, hora, id_cliente, id_servico, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario FROM agendamento WHERE data1 = ? AND hora = ? AND id_funcionario = ?", [data1, hora, id_funcionario])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_servico_funcionario(i, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT sf.id_servico, sf.id_funcionario FROM servico_funcionario as sf INNER JOIN servico AS s ON s.id_servico = sf.id_servico WHERE s.id_servico = ? AND id_funcionario = ? ", [i - 1, id_funcionario])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_servico(nome_servico, preco_servico, duracao_servico, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_servico, nome_servico, preco_servico, duracao_servico, status FROM servico WHERE nome_servico = ? AND preco_servico = ? AND duracao_servico = ? AND status = ?", [nome_servico, preco_servico, duracao_servico, status])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_cargo(nome_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cargo, nome_cargo FROM cargo WHERE nome_cargo = ?", [nome_cargo])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_funcionario, id_cargo, nome, cpf, email, endereco, telefone, status, senha FROM funcionario WHERE id_cargo = ? AND nome = ? AND cpf = ? AND email = ? AND endereco = ? AND telefone = ? AND status = ? AND senha = ?", [id_cargo, nome, cpf, email, endereco, telefone, status, senha])
        return row_to_dict(cur.description, cur.fetchone())




def db_criar_cliente(nome, email, data_nascimento, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cliente (nome, email, data_nascimento, senha) VALUES (?, ?, ?, ?)", [nome, email, data_nascimento, senha])
        id_cliente = cur.lastrowid
        con.commit()
        return {'id_cliente': id_cliente, 'nome': nome, 'email': email, 'data_nascimento': data_nascimento, 'senha':senha}


def db_criar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO agendamento (data1,hora, id_cliente, id_servico, id_funcionario) VALUES (?, ?, ?, ?, ?)", [data1,hora, id_cliente, id_servico, id_funcionario])
        id_agendamento = cur.lastrowid
        con.commit()
        return {'id_agendamento':id_agendamento, 'data1':data1, 'hora':hora, 'id_cliente':id_cliente, 'id_servico':id_servico, 'id_funcionario':id_funcionario}


def db_criar_servico(nome_servico, preco_servico, duracao_servico, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO servico (nome_servico, preco_servico, duracao_servico, status) VALUES (?, ?, ?, ?)", [nome_servico, preco_servico, duracao_servico, status])
        id_servico = cur.lastrowid
        con.commit()
        return {'id_servico':id_servico, 'nome_servico':nome_servico, 'preco_servico':preco_servico, 'duracao_servico':duracao_servico, 'status':status}


def db_criar_servico_funcionario(i, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO servico_funcionario (id_servico, id_funcionario) VALUES (?, ?)", [i, id_funcionario])
        id_servico_funcionario = cur.lastrowid
        con.commit()
        return {'id_servico_funcionario':id_servico_funcionario, 'id_servico':i, 'id_funcinario':id_funcionario}


def db_criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO funcionario (id_cargo, nome, cpf, email, endereco, telefone, status, senha) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [id_cargo, nome, cpf, email, endereco, telefone, status, senha])
        id_funcionario = cur.lastrowid
        con.commit()
        return {'id_funcionario':id_funcionario, 'id_cargo':id_cargo, 'nome':nome, 'cpf':cpf, 'email':email, 'endereco':endereco, 'telefone':telefone, 'status':status, 'senha':senha}


def db_criar_cargo(nome_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cargo(nome_cargo) VALUES (?)", [nome_cargo])
        id_cargo = cur.lastrowid
        con.commit()
        return {'id_cargo':id_cargo,'nome_cargo':nome_cargo}





def db_fazer_login(email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.email, c.senha, c.nome FROM cliente c WHERE c.email = ? AND c.senha = ?", [email, senha])
        return row_to_dict(cur.description, cur.fetchone())


def db_fazer_login_funcionario(email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT email, senha, nome FROM cargo WHERE email = ? AND senha = ?", [email, senha])
        return row_to_dict(cur.description, cur.fetchone())


def db_listar_funcionarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_funcionario, id_cargo, nome, cpf, email, endereco FROM funcionario")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_cliente():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome, email, data_nascimento FROM cliente")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_servico():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_servico, nome_servico, preco_servico, duracao_servico, status FROM servico")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_cargo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cargo, nome_cargo FROM cargo")
        return rows_to_dict(cur.description, cur.fetchall())


def db_trazer_ultimo_id_servico():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM servico ORDER BY id_servico DESC LIMIT 1")
        return row_to_dict(cur.description, cur.fetchone())


def db_historico_cliente(id_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.nome AS nome_cliente, a.data1, a.hora, s.nome_servico, f.nome AS nome_funcionario, s.preco_servico FROM cliente AS c INNER JOIN agendamento AS a ON c.id_cliente = a.id_cliente inner join funcionario as f on a.id_funcionario = f.id_funcionario INNER join servico as s ON a.id_agendamento = s.id_servico where c.id_cliente = ?",[id_cliente])
        return row_to_dict(cur.description, cur.fetchone())



if __name__ == '__main__':
    db_inicializar()
    app.run(debug=True)    