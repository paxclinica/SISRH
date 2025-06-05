from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.models import db
from src.models.pessoa import Pessoa
from src.routes.auth import login_required
from datetime import datetime
import traceback

pessoas_bp = Blueprint('pessoas', __name__)

@pessoas_bp.route('/pessoas')
@login_required
def listar_pessoas():
    try:
        pessoas = Pessoa.query.all()
        return render_template('pessoas/listar.html', pessoas=pessoas)
    except Exception as e:
        print(f"ERRO AO LISTAR PESSOAS: {str(e)}")
        print(traceback.format_exc())
        flash(f"Ocorreu um erro ao listar as pessoas: {str(e)}", "danger")
        return redirect(url_for('main.dashboard'))

@pessoas_bp.route('/pessoas/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_pessoa():
    try:
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
    except Exception as e:
        db.session.rollback()
        print(f"ERRO AO CADASTRAR PESSOA: {str(e)}")
        print(traceback.format_exc())
        flash(f"Ocorreu um erro ao cadastrar a pessoa: {str(e)}", "danger")
        return redirect(url_for('pessoas.listar_pessoas'))

@pessoas_bp.route('/pessoas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_pessoa(id):
    try:
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
    except Exception as e:
        db.session.rollback()
        print(f"ERRO AO EDITAR PESSOA: {str(e)}")
        print(traceback.format_exc())
        flash(f"Ocorreu um erro ao editar a pessoa: {str(e)}", "danger")
        return redirect(url_for('pessoas.listar_pessoas'))

@pessoas_bp.route('/pessoas/excluir/<int:id>')
@login_required
def excluir_pessoa(id):
    try:
        pessoa = Pessoa.query.get_or_404(id)
        
        # Lista para armazenar as vinculações encontradas
        vinculacoes = []
        
        # Verificar se a pessoa está vinculada a algum treinamento
        if hasattr(pessoa, 'participacoes') and pessoa.participacoes.count() > 0:
            treinamentos = [p.treinamento.nome for p in pessoa.participacoes]
            vinculacoes.append(f"Treinamentos: {', '.join(treinamentos)}")
        
        # Verificar se a pessoa está vinculada a algum feedback
        if hasattr(pessoa, 'participacoes_feedback') and pessoa.participacoes_feedback.count() > 0:
            feedbacks = [p.feedback.nome for p in pessoa.participacoes_feedback]
            vinculacoes.append(f"Feedbacks: {', '.join(feedbacks)}")
        
        # Verificar se a pessoa está vinculada a alguma ata de reunião
        if hasattr(pessoa, 'participacoes_ata') and pessoa.participacoes_ata.count() > 0:
            atas = [p.ata_reuniao.nome for p in pessoa.participacoes_ata]
            vinculacoes.append(f"Atas de Reunião: {', '.join(atas)}")
        
        # Se houver vinculações, não permitir a exclusão
        if vinculacoes:
            mensagem = "Não é possível excluir esta pessoa pois está vinculada aos seguintes módulos:\n"
            mensagem += "\n".join(vinculacoes)
            flash(mensagem, 'danger')
            return redirect(url_for('pessoas.listar_pessoas'))
        
        # Se não houver vinculações, excluir a pessoa
        db.session.delete(pessoa)
        db.session.commit()
        
        flash('Pessoa excluída com sucesso!', 'success')
        return redirect(url_for('pessoas.listar_pessoas'))
    except Exception as e:
        db.session.rollback()
        print(f"ERRO AO EXCLUIR PESSOA: {str(e)}")
        print(traceback.format_exc())
        flash(f"Ocorreu um erro ao excluir a pessoa: {str(e)}", "danger")
        return redirect(url_for('pessoas.listar_pessoas'))
