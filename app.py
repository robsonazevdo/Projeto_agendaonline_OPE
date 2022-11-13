from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response, send_from_directory
from contextlib import closing
import sqlite3
import os
import werkzeug




app = Flask(__name__)





@app.route('/')
def inicio():
    return render_template('index.html')



@app.route('/inicio_admin')
def inicio_admin():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:

        return render_template("/login.html", erro="")

    return render_template('admin.html')
    

@app.route('/admin')
def cadastro_admin():
    return render_template('cadastro_admin.html')


@app.route('/add_admin', methods=['GET', 'POST'])
def criar_admin_api():

    # Extrai os dados do formulário.
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["confirmar-senha"]
    

    # Faz o processamento.
    db_criar_admin(nome, email, senha)
    
    return render_template('login.html')


@app.route('/calendario')
def agenda():

    color = ['Brown', 'Navy blue', 'Orange', 'Gray', 'Gold', 'Orange', 'Silver', 'Pink','Purple', 'Green', 'Red', 'Violet']

    resources = db_listar_funcionarios()
    events = db_listar_agendamentos()
    servico = db_listar_servico()
    cliente = db_listar_cliente()
    
     
    return render_template('agenda.html',resources = resources, events = events, color = color, servico = servico, cliente = cliente)





@app.route('/cadastro')
def cadastro():
    cliente = db_listar_cliente()
   
    return render_template('cadastro_cliente.html',cliente = cliente)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/receber_contato', methods=['POST'])
def criar_contato_api():

    # Extrai os dados do formulário.
    nome = request.form.get("nome")
    sobrenome = request.form.get("sobrenome")
    email = request.form.get("email").replace(' ', '').lower()
    telefone = request.form.get("telefone")
    mensagem = request.form.get("mensagem")


    return redirect("https://api.whatsapp.com/send?phone=5511980795796&text=" + nome +  "%20" + sobrenome + "%0D%20" + email + "%0D%20" + telefone + "%0D%20" + mensagem ,code=302)
    # Faz o processamento.
    #contato = criar_contato(nome, sobrenome, email, telefone, mensagem)

    #return render_template('agradecimento.html', nome=nome, sobrenome=sobrenome)  


@app.route('/historico')
def historico():

    lista = db_listar_cliente()
    
    return render_template('historico.html', listar=lista)


@app.route('/addItems')
def addItems():

    cliente = db_listar_cliente()
    funcionario = db_listar_funcionarios()
    servico = db_listar_servico()
    #num = db_verificar_num_comanda(45)
    

    return render_template('add_items.html', cliente=cliente, funcionario=funcionario, servico=servico, num='')


@app.route('/add_items', methods=['POST','GET'])
def add_items_api():

    # Extrai os dados do formulário.
    
    id_comanda = request.form.get("id_comanda")
    quantidade = request.form.get("quantidade")
    id_servico = request.form.get("id_servico")
    id_funcionario = request.form.get("id_funcionario")
    

    # Faz o processamento.
    ja_existia, additems = criar_additems(id_comanda, id_servico, quantidade, id_funcionario)
    
   
    # Monta a resposta.
    mensagem = f"Serviço já foi adicionado." if ja_existia else f"Item adicionado com sucesso."
   

    return render_template('add_items.html', mensagem = mensagem)



@app.route('/verefica_id_comanda',methods=['GET',"POST"])
def verifica_id_comanda():

    numero_comanda = request.form.get("numero_comanda")
    num = db_verificar_num_comanda(numero_comanda)
   
    if num is None:
        mensagem = 'Não existe'
        number = ''
    else:
        mensagem = ''
        number = num
        
    
    lista = db_listar_cliente()
    servico = db_listar_servico()
    funcionario = db_listar_funcionarios()
    
    return render_template('add_items.html', cliente=lista, servico=servico, funcionario=funcionario, num=number, mensagem=mensagem)





@app.route('/comanda')
def comanda():

    lista = db_listar_cliente()
    lista2 = db_listar_operacao()
    lista3 = db_listar_situacao()
    num = {'numero_comanda': 0}
    return render_template('comanda.html', cliente=lista, operacao=lista2, situacao=lista3,num='')



@app.route('/verefica_comanda',methods=['GET',"POST"])
def verifica_comanda():

    numero_comanda = request.form.get("numero_comanda")
    num = db_verificar_num_comanda(numero_comanda)
    
    if num is None:
        mensagem = 'Comanda Pode ser aberta'
        number = numero_comanda
    else:
        mensagem = 'Comanda está sendo usada'
        number = ''
   
    return render_template('admin.html',   num=number, mensagem=mensagem)



@app.route('/use/<num>')
def use_num(num):

    cliente = db_listar_cliente()
    situacao = db_listar_situacao()
    operacao = db_listar_operacao()
    
    return render_template('comanda.html', num = num, cliente=cliente, situacao=situacao, operacao=operacao)




@app.route('/criar_comanda', methods=['GET', 'POST'])
def criar_comando_api():
    
    # Extrai os dados do formulário.
    id_cliente = request.form.get("id_cliente")
    numero_comanda = request.form.get("numero_comanda")
    data_venda = request.form.get("data")
    id_operacao = request.form.get("id_operacao")
    id_situacao = request.form.get("id_situacao")
    id_funcionario = 1


    # Faz o processamento.
    ja_existia, comanda = criar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario)
    
   
    # Monta a resposta.
    mensagem = f"Comanda já está em uso." if ja_existia else f"Comanda criada com sucesso."
   

    return render_template('admin.html', mensagem = mensagem)

   

@app.route('/cadastro_funcionario')
def cadastro_funcionario():
    lista = db_listar_cargo()
    lista2 = db_historico_funcionario()

    funcionario = {'id_funcionario': "novo", 'id_cargo':'', 'nome': "", 'cpf':'', 'email':'', 'endereco':'', 'telefone':'' }

    

    return render_template('cadastro_funcionario.html', cargos = lista, funci = lista2, lista3 = funcionario)


@app.route('/servico')
def cadastro_servico():
    
    lista = db_listar_cargo()
    lista2 = db_listar_servico_cargo()
    return render_template('servico.html', cargo = lista, servico = lista2)
    
 
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
    agendamento = {'id_agendamento': "novo", 'id_cliente': "", 'id_servico':'', 'id_funcionario':''}


        # Monta a resposta.
    return render_template("agendamento.html", logado = logado, mensagem = "", funcionarios = lista, cliente = lista2, servicos = lista3, agendamento = agendamento)
    

@app.route("/meus_agendamentos", methods = ["GET"])
def meus_agendamentos():
    
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return render_template("/login.html", erro="")

    
        # Monta a resposta.
    return render_template("meu_agendamento.html", logado = logado, mensagem = "")


# Processa o botão de excluir um agendamento.
@app.route("/apagar_agendamento/<int:id_agendamento>/<string:data_agendamento>",  methods = ["DELETE"])
def deletar_agendamento_api(id_agendamento, data_agendamento):
    # Autenticação.
    logado = autenticar_login()
 
    if logado is None:
        return redirect("/")
        
   
    # Faz o processamento.
    agendamento = apagar_agendamento(id_agendamento, data_agendamento)
    

    # Monta a resposta.
    if agendamento is None:
        return render_template("meu_agendamento.html", mensagem = "Esse agendamento nem mesmo existia mais."), 404
    mensagem = f"O agendamento foi excluído."
    return render_template("meu_agendamento.html", mensagem = mensagem)


@app.route("/login", methods = ["POST"])
def login():
    # Extrai os dados do formulário.
    f = request.form
    if "email" not in f or "senha" not in f:
        return ":(", 422
    login = f["email"]
    senha = f["senha"]

    # Faz o processamento.
    logado = db_fazer_login_admin(login, senha)

    # Monta a resposta.
    if logado is None:
        return render_template("login.html", erro = "Ops. A senha ou o email deve está errado.")
    resposta = make_response(redirect("/inicio_admin"))

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
    senha = request.form["telefone"]
    
    # Faz o processamento.
    ja_existia, cliente = criar_cliente(nome, email, data_nascimento, senha)
    
   
    # Monta a resposta.
    mensagem = f"O email já existe." if ja_existia else f"O Cadastro foi criada com sucesso."
    lista = db_listar_cliente()
    return render_template("cadastro_cliente.html", mensagem = mensagem, cliente = lista)



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
    lista2 = db_listar_cliente()
    lista3 = db_listar_servico() 

    lista4 = {'id_agendamento': "novo", 'id_cliente': "", 'id_servico':'', 'id_funcionario':''}
    
    ja_existia, agendamento = criar_agendamento(data1, hora, id_cliente, id_servico, id_funcionario)


    # Monta a resposta.
    mensagem = f"o agendamento {data1}{hora} já existia com o id {agendamento['id_servico']}." if ja_existia else f"O Agendamento foi criada."
    return render_template("agendamento.html", mensagem = mensagem, funcionarios = lista, cliente = lista2, servicos = lista3, agendamento = lista4)




@app.route('/add_servico', methods=['GET', 'POST'])
def criar_servico_api():

    # Extrai os dados do formulário.
    nome_servico = request.form["nome"]
    preco_servico = request.form["preco"]
    duracao_servico = request.form["duracao"]
    status = request.form["status"]
    id_cargo = request.form["id_cargo"]

    
    
    # Faz o processamento.
    
    ja_existia, servico = criar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo)
    

    # Monta a resposta.
    mensagem = f"o serviço {nome_servico} já existe." if ja_existia else f"O serviço {nome_servico} foi criada com sucesso."
    lista = db_listar_servico_cargo()
    print(lista)
    return render_template("servico.html", mensagem = mensagem, servico = lista)



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
    



    # Faz o processamento.
    ja_existia, funcionario = criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status)
    
    lista = db_listar_funcionarios()
    # Monta a resposta.
    mensagem = f"O Funcionario {nome} e {email} já existe." if ja_existia else f"O Funcionario {nome} foi criada com sucesso."
    return render_template("cadastro_funcionario.html", mensagem = mensagem, funci = lista)


@app.route('/add_cargo', methods=['GET', 'POST'])
def criar_cargo_api():

    # Extrai os dados do formulário.
    nome_cargo = request.form["nome"]
    

    # Faz o processamento.
    ja_existia, cargo = criar_cargo(nome_cargo)
    

    # Monta a resposta.
    mensagem = f"O Cargo {nome_cargo} já existe." if ja_existia else f"O Cargo {nome_cargo} foi criada com sucesso."
    return render_template("cadastro_funcionario.html", mensagem = mensagem)




@app.route('/editar_funcionario') 
def editar_funcionario_api():
    lista = db_listar_funcionarios()

    return render_template("editar_funcionario.html",funcionarios = lista)




@app.route('/buscar_funcionario', methods=['POST'])
def buscar_funcionario_api():

# Faz o processamento.
      

    funcionario = db_historico_funcionario()
    lista = db_listar_funcionarios()

   
    
 # Monta a resposta.
    if funcionario is None:
        return render_template("editar_funcionario.html", mensagem = f"Esse cliente não existe.", funcionario = funcionario), 404
    return render_template("cadastro_funcionario.html", funcionario = funcionario, funcionarios = lista)



@app.route('/buscar_cliente/<string:nome>', methods=['GET']) 
def buscar_cliente_api(nome):

# Faz o processamento.
    nome_cliente = request.args.get('nome')
    
    clientes = db_historico_cliente(nome_cliente)
    lista = db_listar_cliente()
    
 # Monta a resposta.
    if clientes is None:
        return render_template("historico.html", mensagem = f"Esse cliente não existe.", cliente = clientes), 404
    return render_template("historico.html", cliente = clientes, listar = lista)








@app.route('/buscar_cliente_editar', methods=['GET', 'POST']) 
def buscar_cliente_editar_api():

    # Faz o processamento.
    nome_cliente = request.form["nome"]
    data_agendamento = request.form['data']
    
    apagar_agendamentos = db_meu_agendamento(nome_cliente, data_agendamento)
    
    # Monta a resposta.
    if apagar_agendamento is None:
        return render_template("meu_agendamento.html", mensagem = f"Esse cliente não existe.", cliente = apagar_agendamentos), 404
    return render_template("meu_agendamento.html", cliente = apagar_agendamentos)


@app.route("/alterar_agendamentos/<int:id_agendamento>", methods = ["GET"])
def alterar_agendamento_api(id_agendamento):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    
    agendamento = db_consultar_agendamento(id_agendamento)
    clientes = db_listar_cliente()
    servico = db_listar_servico()
    funcionario = db_listar_funcionarios()

    # Monta a resposta.
    if agendamento is None:
        return render_template("meu_agendamento.html", mensagem = f"Esse cliente não existe."), 404
    return render_template("agendamento.html",  agendamento = agendamento, funcionarios = funcionario, servicos = servico,  cliente = clientes)


@app.route("/alterar_funcionario/<int:id_funcionario>", methods = ["GET"])
def alterar_funcionario_api(id_funcionario):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    
    funcionario = db_consultar_funcionario(id_funcionario)
    cargos = db_listar_cargo()
    lista2 = db_historico_funcionario()

    

    # Monta a resposta.
    if agendamento is None:
        return render_template("meu_agendamento.html", mensagem = f"Esse cliente não existe."), 404
    return render_template("alterar-funcionario.html",  funcionario = funcionario, cargos = cargos, funci = lista2)
    


@app.route("/edicao_funcionario/<int:id_funcionario>", methods = ["POST"])
def edicao_funcionario_api(id_funcionario):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome = request.form["nome"]
    email = request.form["email"]
    endereco = request.form["endereco"]
    cpf = request.form["cpf"]
    telefone = request.form["telefone"]
    id_cargo = request.form["id_cargo"]
    status = request.form["status"]
    

    # Faz o processamento.
    status, funcionario = editar_funcionario(id_funcionario, nome, email, endereco, cpf, telefone, id_cargo, status)

    # Monta a resposta.
    if status == 'não existe':
        mensagem = "Esse Funcionário não existia mais." 
        return render_template("meu_agendamento.html", mensagem = mensagem), 404
    mensagem = f"O Funcionário foi editado." 
    lista = db_listar_cargo()
    lista2 = db_historico_funcionario()

    funcionario = {'id_funcionario': "novo", 'id_cargo':'', 'nome': "", 'cpf':'', 'email':'', 'endereco':'', 'telefone':'' }


    return render_template("cadastro_funcionario.html", mensagem = mensagem, cargos = lista, funci = lista2, lista3 = funcionario)



@app.route("/editar_agendamentos/<int:id_agendamento>", methods = ["POST"])
def editar_agendamento_api(id_agendamento):
    # Autenticação.
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
    status, agendamento = editar_agendamento(id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario)

    # Monta a resposta.
    if status == 'não existe':
        mensagem = "Esse cliente não existia mais." 
        return render_template("meu_agendamento.html", mensagem = mensagem), 404
    mensagem = f"O Cliente foi editado." 
    return render_template("meu_agendamento.html", mensagem = mensagem)






############################################### 
#### Coisas internas do API. ####
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
            foto.save(os.path.join("funcionario_fotos", n))
            return n
    return ""

def deletar_foto(id_foto):
    if id_foto == '': return
    p = os.path.join("funcionario_fotos", id_foto)
    if os.path.exists(p):
        os.remove(p)

def autenticar_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    return db_fazer_login_admin(login, senha)


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


def criar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo):
    servico_ja_existe = db_verificar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo)
    if servico_ja_existe is not None: return True, servico_ja_existe
    novo_servico = db_criar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo)
    return False, novo_servico


def criar_servico_funcionario(i, id_funcionario):
    servico_ja_existe = db_verificar_servico_funcionario(i, id_funcionario)
    if servico_ja_existe is not None: return True, servico_ja_existe
    novo_servico = db_criar_servico_funcionario(i, id_funcionario)
    return False, novo_servico  


def criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status):
    funcionario_ja_existe = db_verificar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status)
    if funcionario_ja_existe is not None: return True, funcionario_ja_existe
    novo_funcionario = db_criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status)
    return False, novo_funcionario


def criar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario):
    comanda_ja_existe = db_verificar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario)
    if comanda_ja_existe is not None: return True, comanda_ja_existe
    nova_comanda = db_criar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario)
    return False, nova_comanda   



def criar_additems(id_comanda, id_servico, quantidade, id_funcionario):
    additems_ja_existe = db_verificar_additems(id_comanda, id_servico, quantidade, id_funcionario)
    if additems_ja_existe is not None: return True, additems_ja_existe
    nova_add = db_criar_additems(id_comanda, id_servico, quantidade, id_funcionario)
    return False, nova_add



def criar_cargo(nome_cargo):
    cargo_ja_existe = db_verificar_cargo(nome_cargo)
    if cargo_ja_existe is not None: return True, cargo_ja_existe
    novo_cargo = db_criar_cargo(nome_cargo)
    return False, novo_cargo


def apagar_agendamento(id_agendamento, data_agendamento):
    agendamento = db_meu_agendamento(id_agendamento, data_agendamento)
    if agendamento is not None: db_deletar_agendamento(id_agendamento)
    return agendamento


def editar_agendamento(id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario):
    agendamento = db_consultar_agendamento(id_agendamento)
    
    if agendamento is None:
        return 'não existe', None
    
    db_editar_agendamento(id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario)
    return 'alterado', agendamento


def editar_funcionario(id_funcionario, nome, email, endereco, cpf, telefone, id_cargo, status):
    funcionario = db_consultar_funcionario(id_funcionario)

    if funcionario is None:
        return 'não existe', None

    db_editar_funcionario(id_funcionario, nome, email, endereco, cpf, telefone, id_cargo, status)
    return 'alterado', funcionario

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
    data_nascimento TEXT NOT NULL,
    tefone VARCHAR(10) NOT NULL,
    UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS tb_admin (
    id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(10) NOT NULL,
    UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS cargo (
    id_cargo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cargo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS situacao (
    id_situacao INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS operacao (
    id_operacao INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS forma_pagamento (
    id_forma_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS servico (
    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_servico VARCHAR(50) NOT NULL,
    preco_servico REAL NOT NULL,
    duracao_servico INTEGER NOT NULL,
    status VARCHAR(7) NOT NULL,
    id_cargo INTEGER NOT NULL,
    FOREIGN KEY (id_cargo) REFERENCES cargo(id_cargo)
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
    data1 date NOT NULL,
    hora time NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)

);

CREATE TABLE IF NOT EXISTS comanda (
    id_comanda INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_comanda INTEGER NOT NULL,
    data_venda Date NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_operacao INTEGER NOT NULL,
    id_situacao INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_situacao) REFERENCES situacao(id_situacao),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario),
    FOREIGN KEY (id_operacao) REFERENCES operacao(id_operacao)

);

CREATE TABLE IF NOT EXISTS addItems (
    id_comanda INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_comanda) REFERENCES comanda(id_comanda),
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario),
    PRIMARY KEY (id_comanda,id_servico)
    

);

CREATE TABLE IF NOT EXISTS comandaFechada (
    id_comanda_fechada INTEGER PRIMARY KEY,
    id_comanda INTEGER NOT NULL,
    valor_unitario REAL NOT NULL,
    desconto REAL NOT NULL,
    valor_total REAL NOT NULL,
    id_forma_pagamento INTERGER NOT NULL,
    FOREIGN KEY (id_forma_pagamento) REFERENCES forma_pagamento(id_forma_pagamento),
    FOREIGN KEY (id_comanda) REFERENCES comanda(id_comanda)

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


def db_verificar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_servico, nome_servico, preco_servico, duracao_servico, status, id_cargo FROM servico WHERE nome_servico = ? AND preco_servico = ? AND duracao_servico = ? AND status = ? AND id_cargo = ?", [nome_servico, preco_servico, duracao_servico, status, id_cargo])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_cargo(nome_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cargo, nome_cargo FROM cargo WHERE nome_cargo = ?", [nome_cargo])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_funcionario, id_cargo, nome, cpf, email, endereco, telefone, status FROM funcionario WHERE id_cargo = ? AND nome = ? AND cpf = ? AND email = ? AND endereco = ? AND telefone = ? AND status = ?", [id_cargo, nome, cpf, email, endereco, telefone, status])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, nome):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_comanda,id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario FROM comanda WHERE id_cliente = ? and numero_comanda = ? and data_venda = ? and id_operacao = ? and id_situacao = ? and id_funcionario = ?", [id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, nome])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_additems(id_comanda, id_servico, quantidade, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_comanda, id_servico, quantidade, id_funcionario FROM addItems WHERE id_comanda = ? and id_servico = ? and quantidade = ? and id_funcionario = ?", [id_comanda, id_servico, quantidade, id_funcionario])
        return row_to_dict(cur.description, cur.fetchone())


def db_verificar_num_comanda(numero_comanda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, id_comanda, numero_comanda FROM comanda WHERE id_situacao = 1 AND numero_comanda = ?",[numero_comanda])
        return row_to_dict(cur.description, cur.fetchone())


####################################################################################################

def db_criar_cliente(nome, email, data_nascimento, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cliente (nome, email, data_nascimento, senha) VALUES (?, ?, ?, ?)", [nome, email, data_nascimento, senha])
        id_cliente = cur.lastrowid
        con.commit()
        return {'id_cliente': id_cliente, 'nome': nome, 'email': email, 'data_nascimento': data_nascimento, 'senha':senha}


def db_criar_admin(nome, email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO tb_admin (nome, email, senha) VALUES (?, ?, ?)", [nome, email, senha])
        id_cliente = cur.lastrowid
        con.commit()
        return {'id_admin': id_cliente, 'nome': nome, 'email': email, 'senha':senha}


def db_criar_agendamento(data1,hora, id_cliente, id_servico, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO agendamento (data1,hora, id_cliente, id_servico, id_funcionario) VALUES (?, ?, ?, ?, ?)", [data1,hora, id_cliente, id_servico, id_funcionario])
        id_agendamento = cur.lastrowid
        con.commit()
        return {'id_agendamento':id_agendamento, 'data1':data1, 'hora':hora, 'id_cliente':id_cliente, 'id_servico':id_servico, 'id_funcionario':id_funcionario}


def db_criar_servico(nome_servico, preco_servico, duracao_servico, status, id_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO servico (nome_servico, preco_servico, duracao_servico, status, id_cargo) VALUES (?, ?, ?, ?,?)", [nome_servico, preco_servico, duracao_servico, status, id_cargo])
        id_servico = cur.lastrowid
        con.commit()
        return {'id_servico':id_servico, 'nome_servico':nome_servico, 'preco_servico':preco_servico, 'duracao_servico':duracao_servico, 'status':status, 'id_cargo':id_cargo}


def db_criar_servico_funcionario(i, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO servico_funcionario (id_servico, id_funcionario) VALUES (?, ?)", [i, id_funcionario])
        id_servico_funcionario = cur.lastrowid
        con.commit()
        return {'id_servico_funcionario':id_servico_funcionario, 'id_servico':i, 'id_funcinario':id_funcionario}


def db_criar_funcionario(id_cargo, nome, cpf, email, endereco, telefone, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO funcionario (id_cargo, nome, cpf, email, endereco, telefone, status) VALUES (?, ?, ?, ?, ?, ?, ?)", [id_cargo, nome, cpf, email, endereco, telefone, status])
        id_funcionario = cur.lastrowid
        con.commit()
        return {'id_funcionario':id_funcionario, 'id_cargo':id_cargo, 'nome':nome, 'cpf':cpf, 'email':email, 'endereco':endereco, 'telefone':telefone}


def db_criar_cargo(nome_cargo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cargo(nome_cargo) VALUES (?)", [nome_cargo])
        id_cargo = cur.lastrowid
        con.commit()
        return {'id_cargo':id_cargo,'nome_cargo':nome_cargo}


def db_criar_comanda(id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO comanda (id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario) VALUES (?, ?, ?, ?, ?, ?)", [id_cliente, numero_comanda, data_venda, id_operacao, id_situacao, id_funcionario])
        id_comanda = cur.lastrowid
        con.commit()
        return {'id_comanda':id_comanda, 'id_cliente':id_cliente, 'numero_comanda':numero_comanda, 'data_venda':data_venda, 'id_operacao':id_operacao, 'id_situacao':id_situacao, 'id_funcionario':id_funcionario}





def db_criar_additems(id_comanda, id_servico, quantidade, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO addItems (id_comanda, id_servico, quantidade, id_funcionario) VALUES (?, ?, ?, ?)", [id_comanda, id_servico, quantidade, id_funcionario])
        con.commit()
        return {'id_comanda':id_comanda, 'id_servico':id_servico, 'quantidade':quantidade, 'id_funcionario':id_funcionario}





def db_fazer_login_admin(email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT email, senha, nome FROM tb_admin WHERE email = ? AND senha = ?", [email, senha])
        return row_to_dict(cur.description, cur.fetchone())


def db_fazer_login_funcionario(email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT email, senha, nome FROM cargo WHERE email = ? AND senha = ?", [email, senha])
        return row_to_dict(cur.description, cur.fetchone())



def db_consultar_agendamento(id_agendamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT a.id_agendamento, c.nome AS nome_cliente, c.id_cliente, a.data1, a.hora, s.nome_servico, s.id_servico, s.preco_servico, f.id_funcionario, f.nome AS nome_funcionario FROM cliente AS c LEFT JOIN agendamento AS a ON c.id_cliente = a.id_cliente LEFT join servico as s ON a.id_servico = s.id_servico LEFT join funcionario as f on f.id_funcionario = a.id_funcionario where a.id_agendamento = ?",[id_agendamento])
        return row_to_dict(cur.description, cur.fetchone())


def db_consultar_funcionario(id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT f.id_funcionario, f.nome, f.email, f.endereco, f.telefone, f.cpf, cg.nome_cargo, f.status, cg.id_cargo FROM funcionario AS f inner join cargo As cg ON f.id_cargo = cg.id_cargo  where f.id_funcionario = ?",[id_funcionario])
        return row_to_dict(cur.description, cur.fetchone())


def db_historico_cliente(nome_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.nome AS nome_cliente, a.data1, a.hora, s.nome_servico, s.preco_servico, f.nome AS nome_funcionario FROM cliente AS c LEFT JOIN agendamento AS a ON c.id_cliente = a.id_cliente LEFT join servico as s ON a.id_servico = s.id_servico LEFT join funcionario as f on f.id_funcionario = a.id_funcionario where c.nome = ? ORDER BY a.data1 desc",[nome_cliente])
        return rows_to_dict(cur.description, cur.fetchall())


def db_historico_funcionario():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT f.id_funcionario, f.nome, f.email, f.endereco, f.telefone, f.cpf, cg.nome_cargo, f.status FROM funcionario AS f inner join cargo As cg ON f.id_cargo = cg.id_cargo")
        return rows_to_dict(cur.description, cur.fetchall())



def db_meu_agendamento(nome_cliente, data_agendamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.nome AS nome_cliente, a.data1, a.hora, s.nome_servico, s.preco_servico, f.nome AS nome_funcionario, a.id_agendamento FROM cliente AS c INNER JOIN agendamento AS a ON c.id_cliente = a.id_cliente LEFT join servico as s ON a.id_servico = s.id_servico LEFT join funcionario as f on f.id_funcionario = a.id_funcionario where nome_cliente = ? AND a.data1 = ?",[nome_cliente, data_agendamento])
        return rows_to_dict(cur.description, cur.fetchall())



def db_listar_funcionarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_funcionario, id_cargo, nome, cpf, email, endereco, telefone FROM funcionario")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_agendamentos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario FROM agendamento")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_cliente():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome, email, data_nascimento, telefone FROM cliente")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_servico():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_servico, nome_servico, preco_servico, duracao_servico, status FROM servico")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_servico_cargo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT s.nome_servico, s.preco_servico, s.duracao_servico, c.nome_cargo, s.status FROM servico as s INNER join cargo as c ON c.id_cargo = s.id_cargo")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_cargo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cargo, nome_cargo FROM cargo")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_operacao():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_operacao, nome FROM operacao")
        return rows_to_dict(cur.description, cur.fetchall())

def db_listar_situacao():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_situacao, nome FROM situacao")
        return rows_to_dict(cur.description, cur.fetchall())


def db_trazer_ultimo_id_servico():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM servico ORDER BY id_servico DESC LIMIT 1")
        return row_to_dict(cur.description, cur.fetchone())


def db_deletar_agendamento(id_agendamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM agendamento WHERE id_agendamento = ?", [id_agendamento])
        con.commit()

    

def db_deletar_operacao(id_operacao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM operacao WHERE id_operacao = ?", [id_operacao])
        con.commit()

def db_alterar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("ALTER TABLE addItems ADD CONSTRAINT PK_add_items PRIMARY KEY(id_comanda,id_servico)")
        con.commit()



def db_editar_agendamento(id_agendamento, data1, hora, id_cliente, id_servico, id_funcionario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE agendamento SET data1 = ?, hora = ?, id_cliente = ?, id_servico = ?, id_funcionario = ? WHERE id_agendamento = ?", [data1, hora, id_cliente, id_servico, id_funcionario, id_agendamento])
        con.commit()
        return {'id_agendamento':id_agendamento, 'data1': data1, 'hora': hora, 'id_cliente': id_cliente, 'id_servico': id_servico, 'id_funcionario': id_funcionario}

def db_editar_funcionario(id_funcionario, nome, email, endereco, cpf, telefone, id_cargo, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE funcionario SET id_cargo = ?, nome = ?, cpf = ?, email = ?, endereco = ?, telefone = ?, status = ? WHERE id_funcionario = ?", [id_cargo, nome, cpf, email, endereco, telefone, status, id_funcionario])
        id_funcionario = cur.lastrowid
        con.commit()
        return {'id_funcionario':id_funcionario, 'id_cargo':id_cargo, 'nome':nome, 'cpf':cpf, 'email':email, 'endereco':endereco, 'telefone':telefone, 'status':status}


def db_atualizar_comanda(id_situacao, numero_comanda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE comanda SET id_situacao = ? WHERE numero_comanda = ?", [id_situacao, numero_comanda])
        con.commit()
        return {'id_situacao':id_situacao, 'numero_comanda':numero_comanda}





if __name__ == '__main__':
    db_inicializar()
    app.run(debug=True) 
     