from flask import Blueprint, request, jsonify
from app.controllers.denuncia_controller import DenunciaController

denuncias_bp = Blueprint('denuncias', __name__)

@denuncias_bp.route('/', methods=['GET'])
def get_denuncias():
    denuncias = DenunciaController.get_all_denuncias()
    return jsonify([denuncia.to_dict() for denuncia in denuncias]), 200

@denuncias_bp.route('/denuncias/<int:id>', methods=['GET'])
def get_denuncia(id):
    denuncia = DenunciaController.get_denuncia_by_id(id)
    if denuncia:
        return jsonify(denuncia.to_dict()), 200
    return jsonify({'message': 'Denuncia not found'}), 404

@denuncias_bp.route('/denuncias', methods=['POST'])
def create_denuncia():
    data = request.get_json()
    new_denuncia = DenunciaController.create_denuncia(data)
    return jsonify(new_denuncia.to_dict()), 201

@denuncias_bp.route('/denuncias/<int:id>', methods=['PUT'])
def update_denuncia(id):
    data = request.get_json()
    updated_denuncia = DenunciaController.update_denuncia(id, data)
    if updated_denuncia:
        return jsonify(updated_denuncia.to_dict()), 200
    return jsonify({'message': 'Denuncia not found'}), 404

@denuncias_bp.route('/denuncias/<int:id>', methods=['DELETE'])
def delete_denuncia(id):
    deleted_denuncia = DenunciaController.delete_denuncia(id)
    if deleted_denuncia:
        return jsonify({'message': 'Denuncia deleted successfully'}), 200
    return jsonify({'message': 'Denuncia not found'}), 404