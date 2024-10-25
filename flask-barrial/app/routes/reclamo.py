from flask import Blueprint, request, jsonify
from app.controllers.reclamo_controller import ReclamoController

reclamos_bp = Blueprint('reclamos', __name__)

@reclamos_bp.route('/', methods=['GET'])
def get_reclamos():
    return ReclamoController.get_all_reclamos()

@reclamos_bp.route('/<int:id>', methods=['GET'])
def get_reclamo(id):
    reclamo, status = ReclamoController.get_reclamo_by_id(id)
    if status == 200:
        return jsonify(reclamo.to_dict()), 200
    return jsonify({'message': 'Reclamo not found'}), 404

@reclamos_bp.route('/create', methods=['POST'])
def create_reclamo():
    data = request.form
    print(data)
    servicios = ReclamoController.create_reclamo()
    print(servicios)
    return servicios

@reclamos_bp.route('/por-usuario/<string:documento>', methods=['GET'])
def get_reclamos_by_usuario(documento):
    return ReclamoController.get_reclamos_by_usuario(documento)

@reclamos_bp.route('/<int:id>', methods=['PUT'])
def update_reclamo(id):
    data = request.get_json()
    updated_reclamo, status = ReclamoController.update_reclamo(id, data)
    if status == 200:
        return jsonify(updated_reclamo.to_dict()), 200
    return jsonify({'message': 'Reclamo not found'}), 404

# traer sitios en los que se puede iniciar reclamo
@reclamos_bp.route('/sitios', methods=['GET'])
def get_sitios():
    return ReclamoController.get_all_sitios()

# traer sitios en los que un inspector puede iniciar reclamo
@reclamos_bp.route('/sitios-inspector/<string:legajo>', methods=['GET'])
def get_sitios_by_inspector(legajo):
    return ReclamoController.get_sitios_by_inspector(legajo)

# traer desperfectos que se pueden reportar
@reclamos_bp.route('/desperfectos', methods=['GET'])
def get_desperfectos():
    return ReclamoController.get_all_desperfectos()

@reclamos_bp.route('/inspector/<string:documento>', methods=['GET'])
def get_reclamos_by_inspector(documento):
    return ReclamoController.get_reclamos_by_inspector(documento)
