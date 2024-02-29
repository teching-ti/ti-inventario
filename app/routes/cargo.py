from flask import Blueprint, render_template, redirect, url_for
from app.models.userModels import db, Cargo, Departamento
from app.forms import AgregarCargoForm
from flask_login import login_required

#se usa para obtener información de dos tablas relacionadas
from sqlalchemy.orm import joinedload
#se usa para obtener los resultados de una consulta de manera ordenada
from sqlalchemy import asc

cargos_bp = Blueprint('cargos', __name__, url_prefix='/cargos')

@cargos_bp.route('/', methods=['GET', 'POST'])
@login_required
def listar_cargos():
    form = AgregarCargoForm()
    if form.validate_on_submit():
        nombre_cargo = form.nombre_cargo.data
        id_departamento = form.departamento_id.data
        departamento = Departamento.query.get(id_departamento)
        if departamento:
            cargo = Cargo(nombre_cargo=nombre_cargo, departamento_id=departamento.id)
            db.session.add(cargo)
            db.session.commit()
            return redirect(url_for('cargos.listar_cargos'))

    cargos = Cargo.query.options(joinedload(Cargo.cargo_departamento)).order_by(asc(Cargo.departamento_id)).all()
    return render_template('cargos.html', form=form, cargos=cargos)