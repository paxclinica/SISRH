from datetime import datetime
from src.models import db

class AtaReuniao(db.Model):
    __tablename__ = 'atas_reuniao'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_reuniao = db.Column(db.Date, nullable=False)
    informacoes = db.Column(db.Text, nullable=False)
    arquivo_ata = db.Column(db.String(255), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com participações
    participacoes = db.relationship('ParticipacaoAta', back_populates='ata_reuniao', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AtaReuniao {self.nome}>'

class ParticipacaoAta(db.Model):
    __tablename__ = 'participacoes_ata'
    
    id = db.Column(db.Integer, primary_key=True)
    ata_reuniao_id = db.Column(db.Integer, db.ForeignKey('atas_reuniao.id'), nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    ata_reuniao = db.relationship('AtaReuniao', back_populates='participacoes')
    pessoa = db.relationship('Pessoa', backref=db.backref('participacoes_ata', lazy='dynamic'))
    
    def __repr__(self):
        return f'<ParticipacaoAta {self.id}>'
