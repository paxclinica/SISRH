from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
        
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'
