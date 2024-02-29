from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

#auth
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
#personal
class Personal(db.Model):
    id_dni = db.Column(db.String(20), primary_key=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'))
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))
    apellido_p = db.Column(db.String(50))
    apellido_m = db.Column(db.String(50))
    nombres = db.Column(db.String(50))
    nombres_completos = db.Column(db.String(150))
    usuario = db.Column(db.String(50))
    fecha_registro = db.Column(db.DateTime)
    estado = db.Column(db.String(20))
    fecha_cese = db.Column(db.DateTime)
    celular_personal = db.Column(db.String(20))

    personal_departamento = db.relationship('Departamento', backref='empleados', lazy=True, overlaps="empleados,personal_departamento")
    personal_cargo = db.relationship('Cargo', backref='personal', lazy=True, overlaps="personal,personal_cargo")

#departamento
class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_departamento = db.Column(db.String(100))
    empleados_departamento = db.relationship('Personal', backref='departamento', lazy=True, overlaps="empleados,personal_departamento")

#cargo
class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cargo = db.Column(db.String(100))
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'))

    cargo_departamento = db.relationship('Departamento', backref='cargos', lazy=True)
    cargo_empleado = db.relationship('Personal', backref='cargo', lazy=True, overlaps="personal,personal_cargo")

#Generar Relaciones entre las tablas de las bases de datos
#categoria
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre_categoria = db.Column(db.String(100))

#marca
class Marca(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre_marca = db.Column(db.String(100))

#activo_general
class ActivoGeneral(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))
    modelo = db.Column(db.String(50))
    nombre = db.Column(db.String(255))
    cantidad_total = db.Column(db.Integer)
    cantidad_disponible = db.Column(db.Integer)
    
    #definiendo relaciones
    categoria = db.relationship('Categoria', backref='activos_generales')
    marca = db.relationship('Marca', backref='activos_generales')

#activo, tabla en donde se encuentra información de un activo específico
class Activo(db.Model):
    num_serie = db.Column(db.String(50), primary_key=True)
    activo_id = db.Column(db.Integer, db.ForeignKey('activo_general.id'))
    nro_cargo = db.Column(db.String(50))
    ubicacion = db.Column(db.Integer)
    responsable = db.Column(db.String(50)) #será el id del personal responsable
    estado = db.Column(db.String(50))
    alquiler = db.Column(db.Boolean)

    activo_general = db.relationship('ActivoGeneral', backref='activos', lazy=True)

#historial, tabla en donde se registrarán los eventos que le ocurran a cada activo
class HistorialActivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activo_id = db.Column(db.String(50), db.ForeignKey('activo.num_serie'), nullable=False)
    evento = db.Column(db.String(50), nullable=False)  # Por ejemplo: ingreso, salida, mantenimiento, etc.
    fecha = db.Column(db.DateTime, nullable=False)
    detalles = db.Column(db.String(200))  # Opcional: para cualquier detalle adicional del evento
    
    # Definir una relación con el activo asociado
    activo = db.relationship('Activo', backref='historial')

class LaptopDetalles(db.Model):
    activo_id = db.Column(db.String(50), db.ForeignKey('activo.num_serie'), primary_key=True)
    procesador = db.Column(db.String(50))
    almacenamiento = db.Column(db.String(50))
    tarjeta_video = db.Column(db.String(50))
    ram = db.Column(db.String(50))
    dimensiones = db.Column(db.String(50))
    comentarios = db.Column(db.String(100))

class MouseDetalles(db.Model):
    activo_id = db.Column(db.String(50), db.ForeignKey('activo.num_serie'), primary_key=True)
    conexion_tipo = db.Column(db.String(50))
    comentarios = db.Column(db.String(100))

class MousepadDetalles(db.Model):
    activo_id = db.Column(db.String(50), db.ForeignKey('activo.num_serie'), primary_key = True)
    dimensiones = db.Column(db.String(50))
    comentarios = db.Column(db.String(100))

class MonitorDetalles(db.Model):
    activo_id = db.Column(db.String(50), db.ForeignKey('activo.num_serie'), primary_key = True)
    tipo_panel = db.Column(db.String(50))
    medidas_panel = db.Column(db.String(50))
    resolucion = db.Column(db.String(30))
    peso = db.Column(db.String(30))
    dimensiones = db.Column(db.String(30))
    comentarios = db.Column(db.String(100))

class SoporteLatopDetalles(db.Model):
    activo_id = db.Column(db.String(50), db.ForeignKey('activo.num_serie'), primary_key = True)
    puertos_usb = db.Column(db.String(50))
    numero_ventiladores = db.Column(db.String(10))
    dimensiones = db.Column(db.String(20))
    peso_maximo = db.Column(db.String(20))
    comentarios = db.Column(db.String(100))

#información editable desde después del momento de suregistro
    
'''
Se deben colocar más tablas de detalles para cada categoría de los activos que vayan a ser registrados en la base de datos
'''