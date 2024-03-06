from flask import Blueprint, render_template, redirect, url_for, request
from app.forms import AsignarPersonalActivoForm
from app.models.userModels import db, Personal
from flask_login import login_required

asignacion_bp = Blueprint('asignacion', __name__, url_prefix='/asignacion')

@asignacion_bp.route('/asignar_activo/<string:num_serie>', methods=['GET', 'POST'])
@login_required
def asignar_activo(num_serie):

    form = AsignarPersonalActivoForm()

    activo_seleccionado = num_serie
    usuarios = Personal.query.all()  # Obtener todos los usuarios disponibles
    return render_template('asignar_activo_personal.html', usuarios=usuarios, activo_seleccionado=activo_seleccionado, form=form)