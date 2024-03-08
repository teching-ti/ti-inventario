from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from app.forms import AsignarPersonalActivoForm, datetime
from app.models.userModels import db, Personal, Activo, Departamento, HistorialActivo, ActivoGeneral, Categoria
from flask_login import login_required

asignacion_bp = Blueprint('asignacion', __name__, url_prefix='/asignacion')

@asignacion_bp.route('/usuarios/<int:departamento_id>', methods=['GET'])
@login_required
def obtener_usuarios(departamento_id):
    usuarios = Personal.query.filter_by(departamento_id=departamento_id).all()  # Filtrar usuarios por departamento
    usuarios_json = [{'id': usuario.id_dni, 'nombre_completo': usuario.nombres_completos} for usuario in usuarios]
    return jsonify(usuarios_json)

@asignacion_bp.route('/asignar_activos', methods=['GET', 'POST'])
@login_required
def asignar_activos():
    activos_seleccionados = request.args.get('activos').split(',')
    #si se ingresa a la página sin un activo seleccionado o colocado en la url, se devuelve a la página de activos
    if(activos_seleccionados[0]==''):
        return redirect(url_for('activo.listar_activos'))
    else:
        form = AsignarPersonalActivoForm(request.form)  # Pasar los datos del formulario al crear la instancia
        # Traer los datos de todos los departamentos
        departamentos = Departamento.query.all() 
        # Cargar las opciones de departamentos en el campo ubicacion
        form.ubicacion.choices = [(d.id, d.nombre_departamento) for d in departamentos]

    return render_template('asignar_activos_un_personal.html', activos_seleccionados=activos_seleccionados, form=form)

@asignacion_bp.route('/guardar_asignacion', methods=['POST'])
@login_required
def guardar_asignacion():
    form = AsignarPersonalActivoForm(request.form)  # Pasar los datos del formulario al crear la instancia

    if form.validate_on_submit():
        activos_seleccionados = form.activos_seleccionados.data.split(',')
        nro_cargo = form.nro_cargo.data
        ubicacion = form.ubicacion.data
        responsable = form.responsable.data

        fecha_actual = datetime.now()
        
        # se modifican los activos individuales y se registran en el historial
        for num_serie in activos_seleccionados:
            activo = Activo.query.get(num_serie)
            if activo:
                activo.nro_cargo = nro_cargo
                activo.ubicacion = ubicacion
                activo.responsable = responsable

                # Registrar en el historial de activos
                
                historial = HistorialActivo(
                    activo_id=num_serie,
                    evento='salida',
                    fecha=fecha_actual,
                    detalles = f'Se ha asignado este activo al personal (DNI: {responsable})'
                    )
                db.session.add(historial)
                db.session.commit()

                # Actualizar la cantidad disponible en la tabla de activos generales
                activo_general = activo.activo_general
                if activo_general:
                    activo_general.cantidad_disponible -= 1
                    db.session.commit()

    return redirect(url_for('activo.listar_activos'))