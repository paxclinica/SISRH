import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import db
from src.models.ata_reuniao import AtaReuniao, ParticipacaoAta
from src.models.feedback import Feedback, ParticipacaoFeedback
from src.main import app

# Função para criar as tabelas dos novos módulos
def criar_tabelas():
    with app.app_context():
        # Criar tabelas para Atas de Reunião
        db.create_all()
        print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
