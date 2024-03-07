from flask import Blueprint, render_template, redirect, url_for, request, jsonify
'''
En las dos líneas siguientes se debe colocar lo siguiente:
- El formulario de detalles
- El modelo de los detalles
'''
from app.forms import AgregarActivoForm, datetime, AgregarDetallesLaptop, AgregarDetallesMouse, AgregarDetallesMousepad, AgregarDetallesMonitor, AgregarDetallesSoporteLaptop, AgregarDetallesCamaraWeb
from app.models.userModels import db, Activo, ActivoGeneral, Personal, Departamento, HistorialActivo, LaptopDetalles, MouseDetalles, MousepadDetalles, MonitorDetalles, SoporteLatopDetalles, CamarasWebDetalles, Categoria, Marca
from flask_login import login_required

activo_bp = Blueprint('activo', __name__, url_prefix='/activo')

@activo_bp.route('/', methods=['GET'])
@login_required
def listar_activos():
    form = AgregarActivoForm()

    activos =  Activo.query.join(Departamento, Activo.ubicacion == Departamento.id) \
                          .order_by(Departamento.nombre_departamento) \
                          .all()

    usuarios_responsables = {}
    departamentos_responsable = {}
    activos_nombres = {}

    for activo in activos:
        dni_responsable = activo.responsable
        id_ubicacion = activo.ubicacion
        id_activo = activo.activo_id

        # obteniendo nombres de responsable y ubicación si aún no están en los diccionarios
        if dni_responsable not in usuarios_responsables:
            responsable = Personal.query.filter_by(id_dni=dni_responsable).first()
            if responsable:
                usuarios_responsables[dni_responsable] = responsable.nombres_completos
        
        if id_ubicacion not in departamentos_responsable:
            ubicacion = Departamento.query.filter_by(id=id_ubicacion).first()
            if ubicacion:
                departamentos_responsable[id_ubicacion] = ubicacion.nombre_departamento

        # obteniendo el nombre del activo general si aún no está en el diccionario
        if id_activo not in activos_nombres:
            activo_general = ActivoGeneral.query.filter_by(id=id_activo).first()
            if activo_general:
                activos_nombres[id_activo] = activo_general.nombre

    #categorias
    categorias = Categoria.query.all()
    #activos generales
    act_gemeral = ActivoGeneral.query.all()
    #marcas
    marcas = Marca.query.all()

    return render_template('activos.html', form=form, activos = activos, usuarios_responsables=usuarios_responsables, departamentos_responsable=departamentos_responsable, activos_nombres=activos_nombres, categorias=categorias, act_gemeral=act_gemeral, marcas=marcas)

@activo_bp.route('/agregar', methods=['POST'])
@login_required
def agregar_activo():
    # instancia del formulario para agregar un activo
    form = AgregarActivoForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            # Procesar el formulario
            #modelo = form.modelo.data
            nro_cargo = form.nro_cargo.data
            num_serie = form.num_serie.data
            activo_general = form.modelo.data
            ubicacion_id = form.ubicacion.data
            responsable = form.responsable.data
            estado = form.estado.data
            alquiler = form.alquiler.data
            #print(f"cargo: {nro_cargo}\nnum_serie:{num_serie}\nactivo_general:{activo_general}\nubicacion:{ubicacion_id}\nresponsable:{responsable}\nestado:{estado}\nalquiler:{alquiler}")

            # se crea un nuevo específico
            activo_especifico = Activo(
                num_serie=num_serie,
                activo_id=activo_general,
                nro_cargo=nro_cargo,
                ubicacion=ubicacion_id,
                responsable=responsable,
                estado=estado,
                alquiler=alquiler
            )

            # agregando el nuevo activo específico a la base de datos
            db.session.add(activo_especifico)
            db.session.commit()

            # logica para otra tabla, pero de suma importancia
            # registro en el historial
            nuevo_historial = HistorialActivo(
                activo_id=num_serie,  # se está usando el número de serie como activo_id
                evento='ingreso',
                fecha=datetime.now(),
                detalles='El activo ha ingresado y se encuentra en posesión del área de TI'
            )
            db.session.add(nuevo_historial)
            db.session.commit()

            #return redirect(url_for('activo.guardar_detalles', activo_id=activo_especifico.num_serie, categoria_id=activo_especifico.activo_general.categoria_id))

            return redirect(url_for('activo.listar_activos'))  # Redirigir a la página de inicio después de agregar el activo
        else:
            print(form.errors)

        if form.ubicacion.data:
            departamento_id = form.ubicacion.data
            personal_options = [(personal.id_dni, personal.nombres_completos) for personal in Personal.query.filter_by(departamento_id=departamento_id).all()]
            form.responsable.choices = personal_options

    return render_template('activos.html', form=form)   

@activo_bp.route('/get_personal/<int:departamento_id>', methods=['GET'])
@login_required
def get_personal(departamento_id):
    personal = Personal.query.filter_by(departamento_id=departamento_id).all()
    personal_data = [{'id_dni': p.id_dni, 'nombres_completos': p.nombres_completos} for p in personal]
    return jsonify(personal_data)

@activo_bp.route('/obtener_formulario_detalles/<int:categoria_id>', methods=['GET'])
@login_required
def obtener_formulario_detalles(categoria_id):

    #agregar los formularios, el codigo del diccionario debe ser igual al id de la categoria
    formularios_por_categoria = {
            1: 'formulario_detalles_laptop.html',
            2: 'formulario_detalles_monitor.html',
            3: 'formulario_detalles_mouse.html',
            4: 'formulario_detalles_mousepad.html',
            5: 'formulario_detalles_soporte_laptop.html',
            12: 'formulario_detalles_camara_web.html'
    }

    formulario = formularios_por_categoria.get(categoria_id)

    # en base al id de la categoría se elige que formulario se va a renderizar
    # validar que formulario es el que se va a retornar
    if formulario:
        form = None
        if(categoria_id==1):
            form = AgregarDetallesLaptop()
        elif(categoria_id==2):
            form = AgregarDetallesMonitor()
        elif(categoria_id==3):
            form = AgregarDetallesMouse()
        elif(categoria_id==4):
            form = AgregarDetallesMousepad()
        elif(categoria_id==5):
            form = AgregarDetallesSoporteLaptop()
        elif(categoria_id==12):
            form = AgregarDetallesCamaraWeb()
        #agregar un elif con la categoria creada

    if formulario:
        print(f'detalles/{formulario}')
        return render_template(f'detalles/{formulario}', form=form)
    else:
        # Si no se encontró ninguna plantilla para la categoría, puedes devolver una plantilla predeterminada
        return '<h1>Este activo no existe, deberá ser agregado siguiendo el archivo "anotaciones.txt"</h1>'
    
@activo_bp.route('/guardar_detalles/<string:activo_id>/<int:categoria_id>', methods=['POST'])
@login_required
def guardar_detalles(activo_id, categoria_id):
    print(activo_id)
    print("Se llegó a la ruta guardar detalles")
    # Aquí se determina qué formulario usar según la categoría del activo
    if categoria_id == 1:
        form = AgregarDetallesLaptop()
    elif categoria_id == 2:
        form = AgregarDetallesMonitor()
    elif categoria_id == 3:
        form = AgregarDetallesMouse()
    elif categoria_id == 4:
        form = AgregarDetallesMousepad()
    elif categoria_id == 5:
        form = AgregarDetallesSoporteLaptop()
    elif categoria_id == 12:
        form = AgregarDetallesCamaraWeb()

    if request.method == 'POST' and form.validate_on_submit():
        # Aquí se obtienen los datos del formulario y se guardan en la tabla correspondiente
        detalles = None

        if categoria_id == 1:
            detalles = LaptopDetalles(
                activo_id=activo_id,
                procesador=form.procesador.data,
                almacenamiento=form.almacenamiento.data,
                tarjeta_video=form.tarjeta_video.data,
                ram=form.ram.data,
                dimensiones=form.dimensiones.data,
                comentarios=form.comentarios.data
            )
        elif categoria_id == 2:
            detalles = MonitorDetalles(
                activo_id = activo_id,
                tipo_panel = form.tipo_panel.data,
                medidas_panel = form.medidas_panel.data,
                resolucion = form.resolucion.data,
                peso = form.peso.data,
                dimensiones = form.dimensiones.data,
                comentarios = form.comentarios.data
            )
            
        elif categoria_id == 3:
            detalles = MouseDetalles(
                activo_id=activo_id,
                conexion_tipo=form.conexion_tipo.data,
                comentarios=form.comentarios.data
            )
            
        elif categoria_id == 4:
            detalles = MousepadDetalles(
                activo_id=activo_id,
                dimensiones=form.dimensiones.data,
                comentarios=form.comentarios.data
            )
        elif categoria_id == 5:
            detalles = SoporteLatopDetalles(
                activo_id = activo_id,
                puertos_usb = form.puertos_usb.data,
                numero_ventiladores = form.numero_ventiladores.data,
                dimensiones = form.dimensiones.data,
                peso_maximo = form.peso_maximo.data,
                comentarios = form.comentarios.data
            )
        elif categoria_id == 12:
            detalles = CamarasWebDetalles(
                activo_id = activo_id,
                resolucion = form.resolucion.data,
                sensor = form.sensor.data,
                microfono = form.microfono.data,
                dimensiones = form.dimensiones.data,
                conector = form.conector.data,
                comentarios = form.comentarios.data
            )

        if detalles:
            print("Los detalles cargaron")
            db.session.add(detalles)
            db.session.commit()

        return redirect(url_for('activo.listar_activos'))
    return render_template('activos.html', form=form)