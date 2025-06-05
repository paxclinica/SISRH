from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from src.models import db
from src.models.ata_reuniao import AtaReuniao, ParticipacaoAta
from src.models.pessoa import Pessoa
from src.routes.auth import login_required
from datetime import datetime
import os
from werkzeug.utils import secure_filename

atas_bp = Blueprint('atas', __name__)

@atas_bp.route('/atas')
@login_required
def listar_atas():
    atas = AtaReuniao.query.all()
    return render_template('atas/listar.html', atas=atas)

@atas_bp.route('/atas/nova', methods=['GET', 'POST'])
@login_required
def cadastrar_ata():
    pessoas = Pessoa.query.filter_by(ativo=True).all()
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_reuniao = request.form.get('data_reuniao')
        informacoes = request.form.get('informacoes')
        participantes = request.form.getlist('participantes')
        
        # Validações
        if not nome or not data_reuniao or not informacoes or not participantes:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('atas/cadastrar.html', pessoas=pessoas)
        
        # Converter string para objeto date
        try:
            data_reuniao = datetime.strptime(data_reuniao, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use o formato YYYY-MM-DD.', 'danger')
            return render_template('atas/cadastrar.html', pessoas=pessoas)
        
        # Criar nova ata de reunião
        nova_ata = AtaReuniao(
            nome=nome,
            data_reuniao=data_reuniao,
            informacoes=informacoes
        )
        
        db.session.add(nova_ata)
        db.session.flush()  # Para obter o ID da ata antes do commit
        
        # Processar arquivo de ata
        if 'arquivo_ata' in request.files:
            arquivo = request.files['arquivo_ata']
            if arquivo and arquivo.filename:
                filename = secure_filename(arquivo.filename)
                # Garantir que o nome do arquivo seja único
                filename = f"{nova_ata.id}_{filename}"
                # Salvar o arquivo
                arquivo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'atas', filename)
                arquivo.save(arquivo_path)
                nova_ata.arquivo_ata = filename
        
        # Adicionar participantes
        for pessoa_id in participantes:
            participacao = ParticipacaoAta(
                ata_reuniao_id=nova_ata.id,
                pessoa_id=int(pessoa_id)
            )
            db.session.add(participacao)
        
        db.session.commit()
        
        flash('Ata de reunião cadastrada com sucesso!', 'success')
        return redirect(url_for('atas.listar_atas'))
    
    return render_template('atas/cadastrar.html', pessoas=pessoas)

@atas_bp.route('/atas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_ata(id):
    ata = AtaReuniao.query.get_or_404(id)
    pessoas = Pessoa.query.all()
    participantes_atuais = [p.pessoa_id for p in ata.participacoes]
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_reuniao = request.form.get('data_reuniao')
        informacoes = request.form.get('informacoes')
        participantes = request.form.getlist('participantes')
        
        # Validações
        if not nome or not data_reuniao or not informacoes or not participantes:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('atas/editar.html', ata=ata, pessoas=pessoas, participantes_atuais=participantes_atuais)
        
        # Converter string para objeto date
        try:
            data_reuniao = datetime.strptime(data_reuniao, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use o formato YYYY-MM-DD.', 'danger')
            return render_template('atas/editar.html', ata=ata, pessoas=pessoas, participantes_atuais=participantes_atuais)
        
        # Atualizar ata
        ata.nome = nome
        ata.data_reuniao = data_reuniao
        ata.informacoes = informacoes
        
        # Processar arquivo de ata
        if 'arquivo_ata' in request.files:
            arquivo = request.files['arquivo_ata']
            if arquivo and arquivo.filename:
                # Remover arquivo antigo se existir
                if ata.arquivo_ata:
                    try:
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'atas', ata.arquivo_ata))
                    except:
                        pass  # Ignora se o arquivo não existir
                
                filename = secure_filename(arquivo.filename)
                # Garantir que o nome do arquivo seja único
                filename = f"{ata.id}_{filename}"
                # Salvar o novo arquivo
                arquivo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'atas', filename)
                arquivo.save(arquivo_path)
                ata.arquivo_ata = filename
        
        # Atualizar participantes
        # Remover todos os participantes atuais
        for participacao in ata.participacoes:
            db.session.delete(participacao)
        
        # Adicionar novos participantes
        for pessoa_id in participantes:
            participacao = ParticipacaoAta(
                ata_reuniao_id=ata.id,
                pessoa_id=int(pessoa_id)
            )
            db.session.add(participacao)
        
        db.session.commit()
        
        flash('Ata de reunião atualizada com sucesso!', 'success')
        return redirect(url_for('atas.listar_atas'))
    
    return render_template('atas/editar.html', ata=ata, pessoas=pessoas, participantes_atuais=participantes_atuais)

@atas_bp.route('/atas/detalhes/<int:id>')
@login_required
def detalhes_ata(id):
    ata = AtaReuniao.query.get_or_404(id)
    return render_template('atas/detalhes.html', ata=ata)

@atas_bp.route('/atas/excluir/<int:id>')
@login_required
def excluir_ata(id):
    ata = AtaReuniao.query.get_or_404(id)
    
    # Remover arquivo se existir
    if ata.arquivo_ata:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'atas', ata.arquivo_ata))
        except:
            pass  # Ignora se o arquivo não existir
    
    db.session.delete(ata)
    db.session.commit()
    
    flash('Ata de reunião excluída com sucesso!', 'success')
    return redirect(url_for('atas.listar_atas'))
