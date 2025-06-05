import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# Configuração do caminho do sistema
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Criar aplicação Flask simples
app = Flask(__name__)

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://pax_user:Pax##50@localhost:3305/pax_clinica_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Definir modelo de usuário simplificado
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

# Função para criar usuário padrão
def criar_usuario_padrao():
    with app.app_context():
        # Verificar se o usuário já existe
        usuario_existente = Usuario.query.filter_by(email='paxclinica@paxclinica.com.br').first()
        
        if usuario_existente:
            print("Usuário padrão já existe!")
            return
        
        # Criar novo usuário
        novo_usuario = Usuario(
            nome='Pax Clínica',
            email='paxclinica@paxclinica.com.br',
            senha_hash=generate_password_hash('Pax##50')
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        print("Usuário padrão criado com sucesso!")

if __name__ == "__main__":
    criar_usuario_padrao()
