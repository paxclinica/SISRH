"""
Script para criar o usuário padrão no sistema Pax Clínica
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import db
from src.models.usuario import Usuario
from src.main import app

# Dados do usuário padrão
email = "paxclinica@paxclinica.com.br"
nome = "Administrador Pax Clínica"
senha = "Pax##50"

# Função para criar o usuário
def criar_usuario_padrao():
    with app.app_context():
        # Verificar se o usuário já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        
        if usuario_existente:
            print(f"Usuário {email} já existe no sistema.")
            return
        
        # Criar novo usuário
        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        
        # Adicionar ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()
        
        print(f"Usuário padrão criado com sucesso: {email}")

if __name__ == "__main__":
    criar_usuario_padrao()
