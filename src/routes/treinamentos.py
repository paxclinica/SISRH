from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from src.models import db
from src.models.treinamento import Treinamento
from src.models.pessoa import Pessoa
from src.models.participacao import Participacao
from src.routes.auth import login_required
from datetime import datetime
import os

treinamentos_bp = Blueprint('treinamentos', __name__)

@treinamentos_bp.route('/treinamentos')
@login_required
def listar_treinamentos():
    try:
        # Obter parâmetros de pesquisa
        nome_treinamento = request.args.get('nome', '')
        nome_instrutor = request.args.get('instrutor', '')
        
        # Construir a consulta base
        query = Treinamento.query
        
        # Aplicar filtros se fornecidos
        if nome_treinamento:
            query = query.filter(Treinamento.nome.ilike(f'%{nome_treinamento}%'))
        
        if nome_instrutor:
            # Join com a tabela de pessoas para filtrar pelo nome do instrutor
            # Modificado para usar left join e garantir que treinamentos sem instrutor também apareçam
            query = query.outerjoin(Pessoa, Treinamento.instrutor_id == Pessoa.id)
            if nome_instrutor.strip():  # Só aplica o filtro se houver texto
                query = query.filter(Pessoa.nome.ilike(f'%{nome_instrutor}%'))
        
        # Executar a consulta
        treinamentos = query.all()
        
        return render_template('treinamentos/listar.html', treinamentos=treinamentos)
    except Exception as e:
        # Log do erro para diagnóstico
        print(f"Erro ao listar treinamentos: {str(e)}")
        flash(f"Ocorreu um erro ao listar os treinamentos: {str(e)}", "danger")
        return redirect(url_for('main.dashboard'))

@treinamentos_bp.route('/treinamentos/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_treinamento():
    try:
        pessoas = Pessoa.query.filter_by(ativo=True).all()
        
        if request.method == 'POST':
            nome = request.form.get('nome')
            data_treinamento = request.form.get('data_treinamento')
            informacoes = request.form.get('informacoes')
            instrutor_id = request.form.get('instrutor_id')
            participantes_ids = request.form.getlist('participantes')
            ata_arquivo = request.files.get('ata_arquivo')
            
            # Validações
            if not nome or not data_treinamento:
                flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
                return render_template('treinamentos/cadastrar.html', pessoas=pessoas)
            
            if not participantes_ids:
                flash('Por favor, selecione pelo menos um participante.', 'danger')
                return render_template('treinamentos/cadastrar.html', pessoas=pessoas)
            
            # Converter string para objeto date
            try:
                data_treinamento = datetime.strptime(data_treinamento, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido. Use o formato YYYY-MM-DD.', 'danger')
                return render_template('treinamentos/cadastrar.html', pessoas=pessoas)
            
            # Criar novo treinamento
            novo_treinamento = Treinamento(
                nome=nome,
                data_treinamento=data_treinamento,
                informacoes=informacoes,
                instrutor_id=instrutor_id if instrutor_id and instrutor_id.strip() else None
            )
            
            db.session.add(novo_treinamento)
            db.session.commit()
            
            # Criar participações
            for participante_id in participantes_ids:
                participacao = Participacao(
                    pessoa_id=participante_id,
                    treinamento_id=novo_treinamento.id
                )
                db.session.add(participacao)
                
                # Se houver arquivo de ata, salvar apenas para a primeira participação
                if ata_arquivo and ata_arquivo.filename and participante_id == participantes_ids[0]:
                    # Garantir que a pasta de uploads/treinamentos exista
                    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'treinamentos')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Salvar o arquivo na pasta de treinamentos
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = f"{timestamp}_{ata_arquivo.filename}"
                    filepath = os.path.join(upload_folder, filename)
                    ata_arquivo.save(filepath)
                    
                    # Atualizar o caminho no banco de dados
                    participacao.ata_arquivo = f"uploads/treinamentos/{filename}"
            
            db.session.commit()
            
            flash('Treinamento cadastrado com sucesso!', 'success')
            return redirect(url_for('treinamentos.listar_treinamentos'))
        
        return render_template('treinamentos/cadastrar.html', pessoas=pessoas)
    except Exception as e:
        db.session.rollback()
        flash(f"Ocorreu um erro ao cadastrar o treinamento: {str(e)}", "danger")
        return redirect(url_for('treinamentos.listar_treinamentos'))

@treinamentos_bp.route('/treinamentos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_treinamento(id):
    try:
        treinamento = Treinamento.query.get_or_404(id)
        pessoas = Pessoa.query.filter_by(ativo=True).all()
        participantes_atuais = [p.pessoa_id for p in treinamento.participacoes.all()]
        
        if request.method == 'POST':
            nome = request.form.get('nome')
            data_treinamento = request.form.get('data_treinamento')
            informacoes = request.form.get('informacoes')
            instrutor_id = request.form.get('instrutor_id')
            participantes_ids = request.form.getlist('participantes')
            ata_arquivo = request.files.get('ata_arquivo')
            
            # Validações
            if not nome or not data_treinamento:
                flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
                return render_template('treinamentos/editar.html', treinamento=treinamento, pessoas=pessoas, participantes_atuais=participantes_atuais)
            
            if not participantes_ids:
                flash('Por favor, selecione pelo menos um participante.', 'danger')
                return render_template('treinamentos/editar.html', treinamento=treinamento, pessoas=pessoas, participantes_atuais=participantes_atuais)
            
            # Converter string para objeto date
            try:
                data_treinamento = datetime.strptime(data_treinamento, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido. Use o formato YYYY-MM-DD.', 'danger')
                return render_template('treinamentos/editar.html', treinamento=treinamento, pessoas=pessoas, participantes_atuais=participantes_atuais)
            
            # Atualizar treinamento
            treinamento.nome = nome
            treinamento.data_treinamento = data_treinamento
            treinamento.informacoes = informacoes
            treinamento.instrutor_id = instrutor_id if instrutor_id and instrutor_id.strip() else None
            
            # Remover participações antigas
            Participacao.query.filter_by(treinamento_id=treinamento.id).delete()
            
            # Criar novas participações
            for participante_id in participantes_ids:
                participacao = Participacao(
                    pessoa_id=participante_id,
                    treinamento_id=treinamento.id
                )
                db.session.add(participacao)
                
                # Se houver arquivo de ata, salvar apenas para a primeira participação
                if ata_arquivo and ata_arquivo.filename and participante_id == participantes_ids[0]:
                    # Garantir que a pasta de uploads/treinamentos exista
                    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'treinamentos')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Salvar o arquivo na pasta de treinamentos
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = f"{timestamp}_{ata_arquivo.filename}"
                    filepath = os.path.join(upload_folder, filename)
                    ata_arquivo.save(filepath)
                    
                    # Atualizar o caminho no banco de dados
                    participacao.ata_arquivo = f"uploads/treinamentos/{filename}"
            
            db.session.commit()
            
            flash('Treinamento atualizado com sucesso!', 'success')
            return redirect(url_for('treinamentos.listar_treinamentos'))
        
        return render_template('treinamentos/editar.html', treinamento=treinamento, pessoas=pessoas, participantes_atuais=participantes_atuais)
    except Exception as e:
        db.session.rollback()
        flash(f"Ocorreu um erro ao editar o treinamento: {str(e)}", "danger")
        return redirect(url_for('treinamentos.listar_treinamentos'))

@treinamentos_bp.route('/treinamentos/excluir/<int:id>')
@login_required
def excluir_treinamento(id):
    try:
        treinamento = Treinamento.query.get_or_404(id)
        
        # Remover participações
        Participacao.query.filter_by(treinamento_id=treinamento.id).delete()
        
        # Remover treinamento
        db.session.delete(treinamento)
        db.session.commit()
        
        flash('Treinamento excluído com sucesso!', 'success')
        return redirect(url_for('treinamentos.listar_treinamentos'))
    except Exception as e:
        db.session.rollback()
        flash(f"Ocorreu um erro ao excluir o treinamento: {str(e)}", "danger")
        return redirect(url_for('treinamentos.listar_treinamentos'))

@treinamentos_bp.route('/treinamentos/detalhes/<int:id>')
@login_required
def detalhes_treinamento(id):
    try:
        treinamento = Treinamento.query.get_or_404(id)
        participacoes = Participacao.query.filter_by(treinamento_id=id).all()
        
        return render_template('treinamentos/detalhes.html', treinamento=treinamento, participacoes=participacoes)
    except Exception as e:
        flash(f"Ocorreu um erro ao exibir os detalhes do treinamento: {str(e)}", "danger")
        return redirect(url_for('treinamentos.listar_treinamentos'))
