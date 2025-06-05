from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from src.models import db
from src.models.usuario import Usuario
from werkzeug.security import check_password_hash, generate_password_hash
import functools

auth_bp = Blueprint('auth', __name__)

# Primeiro definimos a função login_required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Depois usamos o decorador nas rotas
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Validações
        if not email or not senha:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('auth/login.html')
        
        # Verificar usuário
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario or not check_password_hash(usuario.senha_hash, senha):
            flash('Email ou senha inválidos.', 'danger')
            return render_template('auth/login.html')
        
        # Criar sessão
        session.clear()
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session.permanent = True
        
        flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('auth/listar_usuarios.html', usuarios=usuarios)

@auth_bp.route('/usuarios/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Validações
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Este email já está em uso. Por favor, use outro email.', 'danger')
            return render_template('auth/cadastro.html')
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem. Por favor, tente novamente.', 'danger')
            return render_template('auth/cadastro.html')
        
        # Criar novo usuário
        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('auth.listar_usuarios'))
    
    return render_template('auth/cadastro.html')

@auth_bp.route('/usuarios/excluir/<int:id>')
@login_required
def excluir_usuario(id):
    # Não permitir excluir o próprio usuário logado
    if id == session.get('usuario_id'):
        flash('Não é possível excluir seu próprio usuário.', 'danger')
        return redirect(url_for('auth.listar_usuarios'))
    
    usuario = Usuario.query.get_or_404(id)
    
    db.session.delete(usuario)
    db.session.commit()
    
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('auth.listar_usuarios'))

@auth_bp.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

# Função para verificar se o usuário está logado
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
