from flask import Blueprint, render_template, redirect, url_for, flash, session
from src.routes.auth import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')
