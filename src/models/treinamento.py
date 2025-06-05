from datetime import datetime
from src.models import db

class Treinamento(db.Model):
    __tablename__ = 'treinamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_treinamento = db.Column(db.Date, nullable=False)
    informacoes = db.Column(db.Text, nullable=True)
    instrutor_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com participações
    participacoes = db.relationship('Participacao', back_populates='treinamento', lazy='dynamic')
    
    # Relacionamento com instrutor
    instrutor = db.relationship('Pessoa', foreign_keys=[instrutor_id])
    
    def __repr__(self):
        return f'<Treinamento {self.nome}>'
