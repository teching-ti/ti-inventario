from flask import jsonify, Blueprint, render_template
from flask_login import login_required
from app.models.userModels import Categoria, Activo, ActivoGeneral

# Crear el blueprint
grafico1_bp = Blueprint('grafico1', __name__, url_prefix='/grafico1')

@grafico1_bp.route('/')
@login_required
def mostrar_grafico():
    return render_template('index.html')

# Definir la ruta para obtener los datos de los activos por categoría
@grafico1_bp.route('/datos_activos_por_categoria', methods=['GET'])
@login_required
def datos_activos_por_categoria():
    # Consultar la base de datos para obtener la cantidad de activos por categoría
    categorias = Categoria.query.all()
    cantidad_activos_por_categoria = []

    # Iterar sobre las categorías y contar la cantidad de activos para cada una
    for categoria in categorias:
        cantidad_activos = Activo.query.join(ActivoGeneral).filter(ActivoGeneral.categoria_id == categoria.id).count()
        cantidad_activos_por_categoria.append({'categoria': categoria.nombre_categoria, 'cantidad': cantidad_activos})
    
    # Devolver los datos en formato JSON
    return jsonify(cantidad_activos_por_categoria)