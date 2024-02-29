from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.models.userModels import Departamento, db
from app.forms import AgregarDepartamentoForm

departamentos_bp = Blueprint('departamentos', __name__, url_prefix='/departamentos')

@departamentos_bp.route('/', methods=['GET', 'POST'])
@login_required
def listar_departamentos():
    #instancia del formulario
    form = AgregarDepartamentoForm()
    #se valida que cuando este sea recibido a través del método post
    if form.validate_on_submit():
        nombre_departamento = form.nombre_departamento.data
        departamento = Departamento(nombre_departamento=nombre_departamento)
        db.session.add(departamento)
        db.session.commit()
        #después de realizar el respectivo commit se redirecciona a la misma ruta para listar los departamnetos
        return redirect(url_for('departamentos.listar_departamentos'))
    departamentos = Departamento.query.all()
    return render_template('departamentos.html', departamentos=departamentos, form=form)