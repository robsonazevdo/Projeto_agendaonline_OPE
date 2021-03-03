from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# configurar o banco de dados

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Impacta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your secret key'
db = SQLAlchemy(app)


class Cliente (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    logradouro = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(5), nullable=False)
    cep = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(20))
    senha = db.Column(db.String(128), nullable=False)

    def __init__(self, nome, email, logradouro, numero, cep, complemento, senha ):
           
        self.nome = nome
        self.email = email
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.complemento = complemento
        self.senha = senha


 

@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def cliente():
    if request.method == "POST":
        cliente = Cliente(nome = request.form['nome'],
                        email = request.form['email'], 
                        logradouro = request.form['endereco'], 
                        numero = request.form['numero'],
                        cep = request.form['cep'],
                        complemento = request.form['complemento'], 
                        senha = request.form['senha'])
        
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('inicio')) 



db.create_all()

if __name__ == '__main__':
    app.run(debug=True)    