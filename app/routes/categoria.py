from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from app.models.userModels import Categoria, db
from app.forms import AgregarCategoriaForm

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('/', methods=['GET', 'POST'])
@login_required
def listar_categorias():
    form = AgregarCategoriaForm()
    if form.validate_on_submit():
        nombre_categoria = form.nombre_categoria.data
        categoria = Categoria(nombre_categoria = nombre_categoria)
        db.session.add(categoria)
        db.session.commit()
        #después de realizar el respectivo commit se redirecciona a la misma ruta para listar las categorias
        return redirect(url_for('categorias.listar_categorias'))
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias, form=form) 