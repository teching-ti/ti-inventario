from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField, IntegerField, BooleanField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo
from datetime import datetime

#es importante llamar a Departamento ya que se utilizará para que el SelectField de 
#wtforms pueda completarse con información solicitada
from app.models.userModels import Departamento, Cargo, Marca, Categoria, ActivoGeneral, Personal

#formulario para el login de los administradores
class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

#formulario para registrar un administrador
class AdminRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

#formulario para agregar departamentos de la empresa
class AgregarDepartamentoForm(FlaskForm):
    nombre_departamento = StringField('Nombre del Departamento', validators=[DataRequired()])
    submit = SubmitField('Agregar')

#formulario para agregar cargos
#para agregar cargo se depende de un departamento
class AgregarCargoForm(FlaskForm):
    nombre_cargo = StringField('Nombre del Cargo', validators=[DataRequired()])
    departamento_id = SelectField('Departamento', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Agregar')
    
    def __init__(self, *args, **kwargs):
        super(AgregarCargoForm, self).__init__(*args, **kwargs)
        #hace que en el campo de 'departamento_id' se carguen las opciones que lleguen de departamento, siguiendo el script presente
        self.departamento_id.choices = [(departamento.id, departamento.nombre_departamento) for departamento in Departamento.query.all()]

#formulario para agregar al personal
#para esto se depende del departamento y de los cargos
class AgregarPersonalForm(FlaskForm):
    id_dni = StringField('DNI', validators=[DataRequired()])
    departamento_id = SelectField('Departamento', coerce=int, validators=[DataRequired()])
    cargo_id = SelectField('Cargo', coerce=int, validators=[DataRequired()])
    apellido_p = StringField('Apellido Paterno', validators=[DataRequired()])
    apellido_m = StringField('Apellido Materno', validators=[DataRequired()])
    nombres = StringField('Nombres', validators=[DataRequired()])
    nombres_completos = StringField('Nombres Completos', validators=[DataRequired()])
    usuario = StringField('Usuario', validators=[DataRequired()])
    fecha_registro = DateField('Fecha de Registro', format='%Y-%m-%d', default=datetime.now())
    estado = StringField('Estado', validators=[DataRequired()], default="Activo")
    fecha_cese = DateField('Fecha de Cese', format='%Y-%m-%d')
    celular_personal = StringField('Celular', validators=[DataRequired()])
    
    submit = SubmitField('Agregar')

    def __init__(self, *args, **kwargs):
        super(AgregarPersonalForm, self).__init__(*args, **kwargs)
        #agrega una opción vacía al principio de las opciones del campo de departamentos
        #agrega las opciones de departamentos
        self.departamento_id.choices = [('0', 'Seleccionar departamento')] + \
                                       [(departamento.id, departamento.nombre_departamento)
                                        for departamento in Departamento.query.all()]
        #agrega las opciones de cargos
        self.cargo_id.choices = [(cargo.id, cargo.nombre_cargo) for cargo in Cargo.query.all()]

#formulario para agregar categorias
class AgregarCategoriaForm(FlaskForm):
    nombre_categoria = StringField('Nombre Categoría', validators=[DataRequired()])
    submit = SubmitField('Agregar')

#formulario para agregar las marca
class AgregarMarcaForm(FlaskForm):
    nombre_marca = StringField('Nombre de la Marca', validators=[DataRequired()])
    submit = SubmitField('Agregar')

#formulario para agregar activos de manera general
class AgregarActivoGeneralForm(FlaskForm):
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    marca_id = SelectField('Marca', coerce=int, validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()], default='-')
    cantidad_total = IntegerField('Cantidad Total', validators=[DataRequired()])
    cantidad_disponible = IntegerField('Cantidad Disponible', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(AgregarActivoGeneralForm, self).__init__(*args, **kwargs)
        self.categoria_id.choices = [(categoria.id, categoria.nombre_categoria) for categoria in Categoria.query.all()]
        self.marca_id.choices = [(marca.id, marca.nombre_marca) for marca in Marca.query.all()]

#formulario para agregar un activo
class AgregarActivoForm(FlaskForm):
    categoria = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    marca = SelectField('Marca', coerce=int, validators=[DataRequired()])
    modelo = SelectField('Modelo', coerce=int, validators=[DataRequired()])
    num_serie = StringField('Número de Serie', validators=[DataRequired()])
    nro_cargo = StringField('Número de Cargo', default='-')
    ubicacion = StringField('Ubicación', validators=[DataRequired()], default='1')
    responsable =  StringField('Responsable', validators=[DataRequired()], default='00000000')
    estado = SelectField('Estado', coerce=str, validators=[DataRequired()], choices=[])
    alquiler = BooleanField('Alquiler', default=False)
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(AgregarActivoForm, self).__init__(*args, **kwargs)
        # Cargar opciones para las selecciones
        self.categoria.choices = [('0', 'Seleccionar Categoría')] + \
            [(categoria.id, categoria.nombre_categoria) for categoria in Categoria.query.all()]
        self.marca.choices = [('0', 'Seleccionar Marca')] + \
            [(marca.id, marca.nombre_marca) for marca in Marca.query.all()]
        self.modelo.choices = [('0', 'Seleccionar Modelo')] + \
            [(activo.id, f"{activo.categoria.nombre_categoria} - {activo.marca.nombre_marca} - {activo.modelo}") for activo in ActivoGeneral.query.all()]
        #self.ubicacion.choices = [('0', 'Seleccionar Ubicación')] + \
        #    [(departamento.id, departamento.nombre_departamento) for departamento in Departamento.query.all()]
        #self.responsable.choices =  [('0', 'Seleccionar Responsable')] + \
        #    [(personal.id_dni, personal.nombres_completos) for personal in Personal.query.all()]
        self.estado.choices = [('Operativo', 'Operativo'), ('Averiado','Averiado'), ('Baja','Baja')]

'''
Seccion de formularios de detalles de activos
'''

#formulario para agregar los detalles de laptop
class AgregarDetallesLaptop(FlaskForm):
    activo_id = HiddenField('Activo ID')
    procesador = StringField('Procesador', validators=[DataRequired()], default='...')
    almacenamiento = StringField('Almacenamiento', validators=[DataRequired()], default='...')
    tarjeta_video = StringField('Tarjeta de Video', validators=[DataRequired()], default='...')
    ram = StringField('RAM', validators=[DataRequired()], default='...')
    dimensiones = StringField('Dimensiones', validators=[DataRequired()], default='...')
    comentarios = StringField('Comentarios', validators=[DataRequired()], default='...')

#formulario para agregar los detalles de mouse
class AgregarDetallesMouse(FlaskForm):
    activo_id = HiddenField('Activo ID')
    conexion_tipo = StringField('Tipo de Conexion', validators=[DataRequired()], default='...')
    comentarios = StringField('Comentarios', validators=[DataRequired()], default='...')

#formulario para agregar los detalles de mousepad
class AgregarDetallesMousepad(FlaskForm):
    activo_id = HiddenField('Activo ID')
    dimensiones = StringField('Dimensiones', validators=[DataRequired()], default='...')
    comentarios = StringField('Comentarios', validators=[DataRequired()], default='...')

#formulario para agregar los detalles de monitor
class AgregarDetallesMonitor(FlaskForm):
    activo_id = HiddenField('Activo ID')
    tipo_panel = StringField('Tipo de Panel', validators=[DataRequired()], default='...')
    medidas_panel = StringField('Medidas de Panel', validators=[DataRequired()], default='...')
    resolucion = StringField('Resolución', validators=[DataRequired()], default='...')
    peso = StringField('Peso', validators=[DataRequired()], default='...')
    dimensiones = StringField('Dimensiones', validators=[DataRequired()], default='...')
    comentarios = StringField('Comentarios', validators=[DataRequired()], default='...')

#formulario para agregar los detalles de soporte para laptop
class AgregarDetallesSoporteLaptop(FlaskForm):
    activo_id = HiddenField('Activo ID')
    puertos_usb = StringField('Puertos USB', validators=[DataRequired()], default='...')
    numero_ventiladores = StringField('Numero de Ventiladores', validators=[DataRequired()], default='...')
    dimensiones = StringField('Dimensiones', validators=[DataRequired()], default='...')
    peso_maximo = StringField('Peso Máxmimo', validators=[DataRequired()], default='...')
    comentarios = StringField('Comentarios', validators=[DataRequired()], default='...')

#formulario para agregar los detalles de cámaras web
class AgregarDetallesCamaraWeb(FlaskForm):
    activo_id = HiddenField('Activo ID')
    resolucion = StringField('Resolucion', validators=[DataRequired()], default='...')
    sensor = StringField('Sensor', validators=[DataRequired()], default='...')
    microfono = StringField('Microfono', validators=[DataRequired()], default='...')
    dimensiones = StringField('Dimensiones', validators=[DataRequired()], default='...')
    conector = StringField('Conector', validators=[DataRequired()], default='...')
    comentarios = TextAreaField('Comentarios', validators=[DataRequired()], default='...')

#formulario asignarle un activo al personal
class AsignarPersonalActivoForm(FlaskForm):
    activo_id = HiddenField('Activo ID')
    nro_cargo = StringField('N° de Cargo', validators=[DataRequired()])
    ubicacion = SelectField('Departamento', validators=[DataRequired()], default='...')
    responsable = SelectField('Responsable', validators=[DataRequired()])
    activos_seleccionados = StringField('Activos Seleccionados')

    def __init__(self, *args, **kwargs):
        super(AsignarPersonalActivoForm, self).__init__(*args, **kwargs)
        # Agregar una opción vacía al principio de las opciones del campo de ubicación
        # Agregar las opciones de departamentos
        self.ubicacion.choices = [('0', 'Seleccionar departamento')] + \
                                 [(departamento.id, departamento.nombre_departamento)
                                  for departamento in Departamento.query.all()]
        # Agregar las opciones de responsables
        self.responsable.choices = [('0', 'Seleccionar responsable')] + \
                                   [(usuario.id_dni, usuario.nombres_completos)
                                    for usuario in Personal.query.all()]

#formulario para asignar un activo
class AsignarActivoForm(FlaskForm):
    activo = SelectField('Activo', coerce=int, validators=[DataRequired()])
    submit = SubmitField('En proceso de asignación')

#para la asignación de activos al personal, se debe de regitrar pimero a los activos, una vez estos existan en la base de datos
#recién podrán ser cargados y estatrán  disponibles para poder ser seleccionados en el formulario de agregar ekemto