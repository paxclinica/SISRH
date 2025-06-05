import os
import sys
from flask import Flask, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

# Configuração do caminho do sistema
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importação dos modelos e blueprints
from src.models import db
from src.routes.auth import auth_bp
from src.routes.main import main_bp
from src.routes.pessoas import pessoas_bp
from src.routes.treinamentos import treinamentos_bp
from src.routes.consultas import consultas_bp
from src.routes.atas import atas_bp
from src.routes.feedbacks import feedbacks_bp

def create_app():
    app = Flask(__name__)
    
    # Configuração do Flask
    app.config['SECRET_KEY'] = 'b7839ec8f4a2d5e6c9f1b3a7d0e8c5f2a4b6d9e7c3a1f5b8d2e6c9f3'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    
    # Configuração do SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://pax_user:Pax##50@localhost:3305/pax_clinica_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuração de uploads
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    
    # Inicialização do SQLAlchemy
    db.init_app(app)
    
    # Registro dos blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(pessoas_bp)
    app.register_blueprint(treinamentos_bp)
    app.register_blueprint(consultas_bp)
    app.register_blueprint(atas_bp)
    app.register_blueprint(feedbacks_bp)
    
    # Criação das tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
