from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.models import db
from src.models.pessoa import Pessoa
from src.routes.auth import login_required
from datetime import datetime

pessoas_bp = Blueprint('pessoas', __name__)

@pessoas_bp.route('/pessoas')
@login_required
def listar_pessoas():
    pessoas = Pessoa.query.all()
    return render_template('pessoas/listar.html', pessoas=pessoas)

@pessoas_bp.route('/pessoas/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_pessoa():
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        data_admissao = request.form.get('data_admissao')
        data_demissao = request.form.get('data_demissao')
        
        # Validações
        if not nome or not data_nascimento or not data_admissao:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('pessoas/cadastrar.html')
        
        # Converter strings para objetos date
        try:
            data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            data_admissao = datetime.strptime(data_admissao, '%Y-%m-%d').date()
            if data_demissao:
                data_demissao = datetime.strptime(data_demissao, '%Y-%m-%d').date()
            else:
                data_demissao = None
        except ValueError:
            flash('Formato de data inválido. Use o formato YYYY-MM-DD.', 'danger')
            return render_template('pessoas/cadastrar.html')
        
        # Criar nova pessoa
        nova_pessoa = Pessoa(
            nome=nome,
            data_nascimento=data_nascimento,
            data_admissao=data_admissao,
            data_demissao=data_demissao,
            ativo=(data_demissao is None)  # Define como ativo apenas se não tiver data de demissão
        )
        
        db.session.add(nova_pessoa)
        db.session.commit()
        
        flash('Pessoa cadastrada com sucesso!', 'success')
        return redirect(url_for('pessoas.listar_pessoas'))
    
    return render_template('pessoas/cadastrar.html')

@pessoas_bp.route('/pessoas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        data_admissao = request.form.get('data_admissao')
        data_demissao = request.form.get('data_demissao')
        
        # Validações
        if not nome or not data_nascimento or not data_admissao:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('pessoas/editar.html', pessoa=pessoa)
        
        # Converter strings para objetos date
        try:
            data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            data_admissao = datetime.strptime(data_admissao, '%Y-%m-%d').date()
            if data_demissao:
                data_demissao = datetime.strptime(data_demissao, '%Y-%m-%d').date()
            else:
                data_demissao = None
        except ValueError:
            flash('Formato de data inválido. Use o formato YYYY-MM-DD.', 'danger')
            return render_template('pessoas/editar.html', pessoa=pessoa)
        
        # Atualizar pessoa
        pessoa.nome = nome
        pessoa.data_nascimento = data_nascimento
        pessoa.data_admissao = data_admissao
        pessoa.data_demissao = data_demissao
        
        # Atualizar status ativo com base na data de demissão
        pessoa.ativo = data_demissao is None
        
        db.session.commit()
        
        flash('Pessoa atualizada com sucesso!', 'success')
        return redirect(url_for('pessoas.listar_pessoas'))
    
    return render_template('pessoas/editar.html', pessoa=pessoa)

@pessoas_bp.route('/pessoas/excluir/<int:id>')
@login_required
def excluir_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    
    # Verificar se a pessoa está vinculada a algum treinamento
    if pessoa.participacoes.count() > 0:
        treinamentos = [p.treinamento.nome for p in pessoa.participacoes]
        flash(f'Não é possível excluir esta pessoa pois está vinculada aos seguintes treinamentos: {", ".join(treinamentos)}', 'danger')
        return redirect(url_for('pessoas.listar_pessoas'))
    
    db.session.delete(pessoa)
    db.session.commit()
    
    flash('Pessoa excluída com sucesso!', 'success')
    return redirect(url_for('pessoas.listar_pessoas'))
