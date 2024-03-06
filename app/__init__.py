from flask import Flask, redirect, url_for
from flask_login import LoginManager

#se importa los blueprints de cada archivo de ruta
#se podría manejar de manera más ordenada y con varios import,
#pero eso implicaría usar solo un archivo de ruta
from .routes.auth import auth_bp
from .routes.departamento import departamentos_bp
from .routes.cargo import cargos_bp
from .routes.personal import personal_bp
from .routes.categoria import categorias_bp
from .routes.marca import marcas_bp
from .routes.activo_general import activos_bp
from .routes.activo import activo_bp
from .routes.grafico1 import grafico1_bp
from .routes.asignacion import asignacion_bp

from .models.userModels import db, User
from flask_migrate import Migrate

app = Flask(__name__)

#Configuración para MySQL en servidor local
#dentro del bloc de notas con las anotaciones de pythonanywhere
#se encuentran las anotaciones de como funcionaría en producción
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ti:jvteching9830@localhost/base_inventario_ti"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'aBX_146dF'

#Inicializando Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Se carga al usuario con su respectivo id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear las tablas en la base de datos
with app.app_context():
    db.init_app(app)
    db.create_all()
    # instancia de las migraciones
    migrate = Migrate(app, db)

#se registran los blueprints para que se pueda acceder a las rutas establecidas
app.register_blueprint(auth_bp)
app.register_blueprint(departamentos_bp)
app.register_blueprint(cargos_bp)
app.register_blueprint(personal_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(marcas_bp)
app.register_blueprint(activos_bp)
app.register_blueprint(activo_bp)
app.register_blueprint(asignacion_bp)
#graficos
app.register_blueprint(grafico1_bp)

# Manejador para la página no encontrada (404)
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('auth.login'))

# Manejador para la página no encontrada (404)
@app.errorhandler(401)
def page_not_found(error):
    return redirect(url_for('auth.login'))