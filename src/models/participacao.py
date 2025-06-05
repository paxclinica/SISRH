from datetime import datetime
import os
from src.models import db

class Participacao(db.Model):
    __tablename__ = 'participacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    treinamento_id = db.Column(db.Integer, db.ForeignKey('treinamentos.id'), nullable=False)
    data_participacao = db.Column(db.DateTime, default=datetime.utcnow)
    ata_arquivo = db.Column(db.String(255), nullable=True)
    
    # Relacionamentos
    pessoa = db.relationship('Pessoa', back_populates='participacoes')
    treinamento = db.relationship('Treinamento', back_populates='participacoes')
    
    def __repr__(self):
        return f'<Participacao: {self.pessoa.nome} em {self.treinamento.nome}>'
    
    def salvar_ata(self, arquivo):
        """
        Salva o arquivo de ata e atualiza o caminho no banco de dados
        """
        if arquivo:
            # Gera um nome de arquivo único baseado no timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{arquivo.filename}"
            
            # Define o caminho para salvar o arquivo
            upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'atas')
            
            # Cria o diretório se não existir
            os.makedirs(upload_folder, exist_ok=True)
            
            # Salva o arquivo
            filepath = os.path.join(upload_folder, filename)
            arquivo.save(filepath)
            
            # Atualiza o caminho no banco de dados
            self.ata_arquivo = f"uploads/atas/{filename}"
            
            return True
        return False
