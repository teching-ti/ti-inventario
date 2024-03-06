from flask import Blueprint, render_template, redirect, url_for, request
from app.models.userModels import db, ActivoGeneral, Categoria, Marca
from app.forms import AgregarActivoGeneralForm, AgregarCategoriaForm, AgregarMarcaForm
from flask_login import login_required

activos_bp = Blueprint('activos', __name__, url_prefix='/activos')

@activos_bp.route('/', methods=['GET'])
@login_required
def listar_activos():
    form = AgregarActivoGeneralForm()
    form2 = AgregarCategoriaForm()
    form3 = AgregarMarcaForm()
    #la variable personal tiene una consulta que trae de manera conjunta el departemento y cargo de cada personal
    activo_general = ActivoGeneral.query.all()
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    return render_template('activos_generales.html', form=form, form2=form2, form3=form3, activo_general=activo_general, marcas=marcas, categorias=categorias)

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

@activos_bp.route('/agregar-categoria', methods=['GET', 'POST'])
@login_required
def agregar_categorias():
    form = AgregarCategoriaForm()
    if form.validate_on_submit():
        nombre_categoria = form.nombre_categoria.data
        categoria = Categoria(nombre_categoria = nombre_categoria)
        db.session.add(categoria)
        db.session.commit()
        #después de realizar el respectivo commit se redirecciona a la misma ruta para listar las categorias
        return redirect(url_for('activos.listar_activos'))
    #categorias = Categoria.query.all()
    return render_template('activos_generales.html')

@activos_bp.route('/agregar-marca', methods=['GET', 'POST'])
@login_required
def agregar_marcas():
    form = AgregarMarcaForm()
    if form.validate_on_submit():
        nombre_marca = form.nombre_marca.data
        marca = Marca(nombre_marca=nombre_marca)
        db.session.add(marca)
        db.session.commit()
        #después de realizar el respectivo commit se redirecciona a la misma ruta para listar las categorias
        return redirect(url_for('activos.listar_activos'))
    #marcas = Marca.query.all()
    return render_template('activos_generales.html') 