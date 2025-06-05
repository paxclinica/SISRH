from flask import Blueprint, render_template, request
from src.models.pessoa import Pessoa
from src.models.participacao import Participacao
from src.models.treinamento import Treinamento
from src.models.ata_reuniao import AtaReuniao, ParticipacaoAta
from src.models.feedback import Feedback, ParticipacaoFeedback
from src.routes.auth import login_required

consultas_bp = Blueprint('consultas', __name__)

@consultas_bp.route('/consultas/treinamentos-por-pessoa', methods=['GET', 'POST'])
@login_required
def treinamentos_por_pessoa():
    pessoas = Pessoa.query.all()
    resultados_treinamentos = []
    resultados_atas = []
    resultados_feedbacks = []
    pessoa_selecionada = None
    
    if request.method == 'POST':
        pessoa_id = request.form.get('pessoa_id')
        
        if pessoa_id:
            pessoa_selecionada = Pessoa.query.get(pessoa_id)
            
            # Buscar treinamentos
            participacoes = Participacao.query.filter_by(pessoa_id=pessoa_id).all()
            for participacao in participacoes:
                treinamento = Treinamento.query.get(participacao.treinamento_id)
                resultados_treinamentos.append({
                    'treinamento': treinamento,
                    'participacao': participacao,
                    'data': treinamento.data_treinamento,
                    'tipo': 'Treinamento'
                })
            
            # Buscar atas de reunião
            participacoes_ata = ParticipacaoAta.query.filter_by(pessoa_id=pessoa_id).all()
            for participacao in participacoes_ata:
                ata = AtaReuniao.query.get(participacao.ata_reuniao_id)
                resultados_atas.append({
                    'ata': ata,
                    'participacao': participacao,
                    'data': ata.data_reuniao,
                    'tipo': 'Ata de Reunião'
                })
            
            # Buscar feedbacks
            participacoes_feedback = ParticipacaoFeedback.query.filter_by(pessoa_id=pessoa_id).all()
            for participacao in participacoes_feedback:
                feedback = Feedback.query.get(participacao.feedback_id)
                resultados_feedbacks.append({
                    'feedback': feedback,
                    'participacao': participacao,
                    'data': feedback.data_feedback,
                    'tipo': 'Feedback'
                })
    
    return render_template('consultas/treinamentos_por_pessoa.html', 
                          pessoas=pessoas, 
                          resultados_treinamentos=resultados_treinamentos,
                          resultados_atas=resultados_atas,
                          resultados_feedbacks=resultados_feedbacks,
                          pessoa_selecionada=pessoa_selecionada)
