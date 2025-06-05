import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuração do caminho do sistema
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Criar aplicação Flask simples
app = Flask(__name__)

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://pax_user:Pax##50@localhost:3305/pax_clinica_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Importar modelos
from src.models.pessoa import Pessoa
from src.models.usuario import Usuario
from src.models.treinamento import Treinamento
from src.models.participacao import Participacao
from src.models.ata_reuniao import AtaReuniao, ParticipacaoAta
from src.models.feedback import Feedback, ParticipacaoFeedback

# Função para criar as tabelas
def criar_tabelas():
    with app.app_context():
        db.create_all()
        print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
