from datetime import datetime
from src.models import db

class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    data_demissao = db.Column(db.Date, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamento com participações em treinamentos
    participacoes = db.relationship('Participacao', back_populates='pessoa', lazy='dynamic')
    
    def __repr__(self):
        return f'<Pessoa {self.nome}>'
