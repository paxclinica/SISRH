from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.models import db
from src.models.usuario import Usuario
from src.routes.auth import login_required

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/usuarios/excluir/<int:id>')
@login_required
def excluir_usuario(id):
    # Não permitir excluir o próprio usuário logado
    if id == request.session.get('usuario_id'):
        flash('Não é possível excluir seu próprio usuário.', 'danger')
        return redirect(url_for('usuarios.listar_usuarios'))
    
    usuario = Usuario.query.get_or_404(id)
    
    db.session.delete(usuario)
    db.session.commit()
    
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))
