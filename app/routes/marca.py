from flask import Blueprint, render_template, redirect, url_for
from app.models.userModels import db, Marca, Categoria
from app.forms import AgregarMarcaForm
from flask_login import login_required

#se usa para obtener información de dos tablas relacionadas
from sqlalchemy.orm import joinedload
#se usa para obtener los resultados de una consulta de manera ordenada
from sqlalchemy import asc

marcas_bp = Blueprint('marcas', __name__, url_prefix='/marcas')

@marcas_bp.route('/', methods=['GET', 'POST'])
@login_required
def listar_marcas():
    form = AgregarMarcaForm()
    if form.validate_on_submit():
        nombre_marca = form.nombre_marca.data
        marca = Marca(nombre_marca=nombre_marca)
        db.session.add(marca)
        db.session.commit()
        return redirect(url_for('marcas.listar_marcas'))

    marcas = Marca.query.all()
    return render_template('marcas.html', form=form, marcas=marcas)