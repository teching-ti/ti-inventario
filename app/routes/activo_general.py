from flask import Blueprint, render_template, redirect, url_for, request
from app.models.userModels import db, ActivoGeneral, Categoria, Marca
from app.forms import AgregarActivoGeneralForm
from flask_login import login_required

activos_bp = Blueprint('activos', __name__, url_prefix='/activos')

@activos_bp.route('/', methods=['GET'])
@login_required
def listar_activos():
    form = AgregarActivoGeneralForm()
    #la variable personal tiene una consulta que trae de manera conjunta el departemento y cargo de cada personal
    activo_general = ActivoGeneral.query.all()
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    return render_template('activos_generales.html', form=form, activo_general=activo_general, marcas=marcas, categorias=categorias)

@activos_bp.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar_activo_general():
    form = AgregarActivoGeneralForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Aquí procesas los datos del formulario y creas un nuevo activo general
            # Puedes usar form.<campo>.data para acceder a los datos del formulario

            categoria_nombre = Categoria.query.get(form.categoria_id.data).nombre_categoria
            marca_nombre = Marca.query.get(form.marca_id.data).nombre_marca

            nuevo_activo = ActivoGeneral(
                categoria_id=form.categoria_id.data,
                marca_id=form.marca_id.data,
                modelo=form.modelo.data,
                nombre = f"{categoria_nombre} - {marca_nombre} - {form.modelo.data}",
                cantidad_total=form.cantidad_total.data,
                cantidad_disponible=form.cantidad_disponible.data
            )
            db.session.add(nuevo_activo)
            db.session.commit()
        else:
            print("El formulario NO ES VALIDO")
        return redirect(url_for('activos.listar_activos'))  # Redirecciona después de agregar
    
    return render_template('activos_generales.html', form=form)