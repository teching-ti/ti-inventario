from flask import Blueprint, render_template, redirect, url_for, jsonify, flash, request
from app.models.userModels import Personal, Cargo, ActivoGeneral, Categoria, Marca, Activo
from app.forms import AgregarPersonalForm, AsignarActivoForm
from app.models.userModels import db
from sqlalchemy.orm import joinedload
from flask_login import login_required

#el blueprint consta con un url y un prefijo, lo que hace es convertir a su ruta '/' en la de /personal
#de esa forma se puede manejar una navegación más ordenada
personal_bp = Blueprint('personal', __name__, url_prefix='/personal')

@personal_bp.route('/', methods=['GET'])
@login_required
def listar_personal():
    form = AgregarPersonalForm()
    #la variable personal tiene una consulta que trae de manera conjunta el departemento y cargo de cada personal
    personal = Personal.query.options(joinedload(Personal.departamento), joinedload(Personal.cargo)).all()
    return render_template('personal.html', form=form, personal=personal)

@personal_bp.route('/agregar', methods=['POST'])
@login_required
def agregar_personal():
    #instancia del formulario
    form = AgregarPersonalForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            #print("El formulario es validado")
            #El formulario se ha validado correctamente, proceder con la creación del personal
            personal = Personal(
                id_dni=form.id_dni.data,
                departamento_id=form.departamento_id.data,
                cargo_id=form.cargo_id.data,
                apellido_p=form.apellido_p.data,
                apellido_m=form.apellido_m.data,
                nombres=form.nombres.data,
                nombres_completos=form.nombres_completos.data,
                usuario=form.usuario.data,
                fecha_registro=form.fecha_registro.data,
                estado=form.estado.data,
                fecha_cese=form.fecha_cese.data,
                celular_personal=form.celular_personal.data
            )

            db.session.add(personal)
            db.session.commit()
        else:
            print("El formulario NO ES VÁLIDO")
        return redirect(url_for('personal.listar_personal'))

    return render_template('personal.html', form=form)

#ruta en donde se realizará la consulta json para obtener información
@personal_bp.route('/cargos/<int:departamento_id>', methods=['GET'])
@login_required
def obtener_cargos(departamento_id):
    #se desea obtener información respecto a los cargos
    cargos = Cargo.query.filter_by(departamento_id=departamento_id).all() # Filtra los cargos por el departamento seleccionado
    cargos_json = [{'id': cargo.id, 'nombre_cargo': cargo.nombre_cargo} for cargo in cargos]
    return jsonify(cargos_json)

#vista de personal para poder asignar activos
#probando
@personal_bp.route('/asignar-activo/<int:empleado_id>', methods=['GET', 'POST'])
@login_required
def asignar_activo(empleado_id):
    empleado = Personal.query.get_or_404(empleado_id)
    form = AsignarActivoForm()

    # Obtener activos disponibles para asignar
    activos_disponibles = Activo.query.filter_by(responsable=None).all()
    categorias = Categoria.query.all()
    marcas = Marca.query.all()

    print(activos_disponibles)
    return render_template('asignar-activo.html', empleado=empleado, form=form, activos_disponibles=activos_disponibles, categorias=categorias, marcas=marcas)

@personal_bp.route('/api/marcas/<int:categoria_id>', methods=['GET'])
@login_required
def obtener_marcas(categoria_id):
    marcas = Marca.query.filter_by(categoria_id=categoria_id).all()
    marcas_json = [{'id': marca.id, 'nombre_marca': marca.nombre_marca} for marca in marcas]
    return jsonify(marcas_json)

@personal_bp.route('/api/activos-disponibles/<int:empleado_id>/<int:categoria_id>/<int:marca_id>', methods=['GET'])
@login_required
def obtener_activos_disponibles(empleado_id, categoria_id, marca_id):
    activos_disponibles = ActivoGeneral.query.filter(ActivoGeneral.categoria_id==categoria_id, ActivoGeneral.marca_id==marca_id, ActivoGeneral.cantidad_disponible > 0).all()
    activos_json = [{'modelo': activo.modelo} for activo in activos_disponibles]

    return jsonify(activos_json)