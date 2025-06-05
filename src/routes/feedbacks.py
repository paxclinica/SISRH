from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from src.models import db
from src.models.feedback import Feedback, ParticipacaoFeedback
from src.models.pessoa import Pessoa
from src.routes.auth import login_required
from datetime import datetime
import os
from werkzeug.utils import secure_filename

feedbacks_bp = Blueprint('feedbacks', __name__)

@feedbacks_bp.route('/feedbacks')
@login_required
def listar_feedbacks():
    feedbacks = Feedback.query.all()
    return render_template('feedbacks/listar.html', feedbacks=feedbacks)

@feedbacks_bp.route('/feedbacks/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_feedback():
    pessoas = Pessoa.query.filter_by(ativo=True).all()
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_feedback = request.form.get('data_feedback')
        informacoes = request.form.get('informacoes')
        participantes = request.form.getlist('participantes')
        
        # Validações
        if not nome or not data_feedback or not informacoes or not participantes:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('feedbacks/cadastrar.html', pessoas=pessoas)
        
        # Converter string para objeto date
        try:
            data_feedback = datetime.strptime(data_feedback, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use o formato YYYY-MM-DD.', 'danger')
            return render_template('feedbacks/cadastrar.html', pessoas=pessoas)
        
        # Criar novo feedback
        novo_feedback = Feedback(
            nome=nome,
            data_feedback=data_feedback,
            informacoes=informacoes
        )
        
        db.session.add(novo_feedback)
        db.session.flush()  # Para obter o ID do feedback antes do commit
        
        # Processar arquivo de feedback
        if 'arquivo_feedback' in request.files:
            arquivo = request.files['arquivo_feedback']
            if arquivo and arquivo.filename:
                filename = secure_filename(arquivo.filename)
                # Garantir que o nome do arquivo seja único
                filename = f"{novo_feedback.id}_{filename}"
                # Salvar o arquivo
                arquivo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'feedbacks', filename)
                arquivo.save(arquivo_path)
                novo_feedback.arquivo_feedback = filename
        
        # Adicionar participantes
        for pessoa_id in participantes:
            participacao = ParticipacaoFeedback(
                feedback_id=novo_feedback.id,
                pessoa_id=int(pessoa_id)
            )
            db.session.add(participacao)
        
        db.session.commit()
        
        flash('Feedback cadastrado com sucesso!', 'success')
        return redirect(url_for('feedbacks.listar_feedbacks'))
    
    return render_template('feedbacks/cadastrar.html', pessoas=pessoas)

@feedbacks_bp.route('/feedbacks/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    pessoas = Pessoa.query.all()
    participantes_atuais = [p.pessoa_id for p in feedback.participacoes]
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_feedback = request.form.get('data_feedback')
        informacoes = request.form.get('informacoes')
        participantes = request.form.getlist('participantes')
        
        # Validações
        if not nome or not data_feedback or not informacoes or not participantes:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('feedbacks/editar.html', feedback=feedback, pessoas=pessoas, participantes_atuais=participantes_atuais)
        
        # Converter string para objeto date
        try:
            data_feedback = datetime.strptime(data_feedback, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use o formato YYYY-MM-DD.', 'danger')
            return render_template('feedbacks/editar.html', feedback=feedback, pessoas=pessoas, participantes_atuais=participantes_atuais)
        
        # Atualizar feedback
        feedback.nome = nome
        feedback.data_feedback = data_feedback
        feedback.informacoes = informacoes
        
        # Processar arquivo de feedback
        if 'arquivo_feedback' in request.files:
            arquivo = request.files['arquivo_feedback']
            if arquivo and arquivo.filename:
                # Remover arquivo antigo se existir
                if feedback.arquivo_feedback:
                    try:
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'feedbacks', feedback.arquivo_feedback))
                    except:
                        pass  # Ignora se o arquivo não existir
                
                filename = secure_filename(arquivo.filename)
                # Garantir que o nome do arquivo seja único
                filename = f"{feedback.id}_{filename}"
                # Salvar o novo arquivo
                arquivo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'feedbacks', filename)
                arquivo.save(arquivo_path)
                feedback.arquivo_feedback = filename
        
        # Atualizar participantes
        # Remover todos os participantes atuais
        for participacao in feedback.participacoes:
            db.session.delete(participacao)
        
        # Adicionar novos participantes
        for pessoa_id in participantes:
            participacao = ParticipacaoFeedback(
                feedback_id=feedback.id,
                pessoa_id=int(pessoa_id)
            )
            db.session.add(participacao)
        
        db.session.commit()
        
        flash('Feedback atualizado com sucesso!', 'success')
        return redirect(url_for('feedbacks.listar_feedbacks'))
    
    return render_template('feedbacks/editar.html', feedback=feedback, pessoas=pessoas, participantes_atuais=participantes_atuais)

@feedbacks_bp.route('/feedbacks/detalhes/<int:id>')
@login_required
def detalhes_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    return render_template('feedbacks/detalhes.html', feedback=feedback)

@feedbacks_bp.route('/feedbacks/excluir/<int:id>')
@login_required
def excluir_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    
    # Remover arquivo se existir
    if feedback.arquivo_feedback:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'feedbacks', feedback.arquivo_feedback))
        except:
            pass  # Ignora se o arquivo não existir
    
    db.session.delete(feedback)
    db.session.commit()
    
    flash('Feedback excluído com sucesso!', 'success')
    return redirect(url_for('feedbacks.listar_feedbacks'))
