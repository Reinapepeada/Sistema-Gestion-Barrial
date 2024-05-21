from flask import Blueprint, request, jsonify
from app.controllers.reclamo_controller import ReclamoController

reclamos_bp = Blueprint('reclamos', __name__)

@reclamos_bp.route('/', methods=['GET'])
def get_reclamos():
    reclamos = ReclamoController.get_all_reclamos()
    return jsonify([reclamo.to_dict() for reclamo in reclamos]), 200

@reclamos_bp.route('/<int:id>', methods=['GET'])
def get_reclamo(id):
    reclamo, status = ReclamoController.get_reclamo_by_id(id)
    if status == 200:
        return jsonify(reclamo.to_dict()), 200
    return jsonify({'message': 'Reclamo not found'}), 404

@reclamos_bp.route('/', methods=['POST'])
def create_reclamo():
    data = request.get_json()
    new_reclamo, status = ReclamoController.create_reclamo(data)
    if status == 201:
        return jsonify(new_reclamo.to_dict()), 201
    return jsonify({'message': 'No se ha podido crear el reclamo'}), 400

@reclamos_bp.route('/<int:id>', methods=['PUT'])
def update_reclamo(id):
    data = request.get_json()
    updated_reclamo, status = ReclamoController.update_reclamo(id, data)
    if status == 200:
        return jsonify(updated_reclamo.to_dict()), 200
    return jsonify({'message': 'Reclamo not found'}), 404

@reclamos_bp.route('/<int:id>', methods=['DELETE'])
def delete_reclamo(id):
    deleted_reclamo, status = ReclamoController.delete_reclamo(id)
    if status == 200:
        return jsonify({'message': 'Reclamo deleted successfully'}), 200
    return jsonify({'message': 'Reclamo not found'}), 404