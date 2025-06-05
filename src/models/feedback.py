from datetime import datetime
from src.models import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_feedback = db.Column(db.Date, nullable=False)
    informacoes = db.Column(db.Text, nullable=False)
    arquivo_feedback = db.Column(db.String(255), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com participações
    participacoes = db.relationship('ParticipacaoFeedback', back_populates='feedback', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Feedback {self.nome}>'

class ParticipacaoFeedback(db.Model):
    __tablename__ = 'participacoes_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedbacks.id'), nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    feedback = db.relationship('Feedback', back_populates='participacoes')
    pessoa = db.relationship('Pessoa', backref=db.backref('participacoes_feedback', lazy='dynamic'))
    
    def __repr__(self):
        return f'<ParticipacaoFeedback {self.id}>'
