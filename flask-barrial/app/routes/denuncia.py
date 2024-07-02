from flask import Blueprint, request, jsonify
from app.controllers.denuncia_controller import DenunciaController

denuncias_bp = Blueprint("denuncias", __name__)


@denuncias_bp.route("/", methods=["GET"])
def get_denuncias():
    denuncias = DenunciaController.get_all_denuncias()
    return jsonify([denuncia.to_dict() for denuncia in denuncias]), 200


# traer denuncias por que ha hecho el vecino
@denuncias_bp.route("/created/<string:documento>", methods=["GET"])
def get_denuncias_by_vecino(documento):
    return  DenunciaController.get_denuncias_by_vecino(documento)
    


# traer denuncias recibidas por vecino
@denuncias_bp.route("/received/<string:documento>", methods=["GET"])
def get_denuncias_by_denunciado(documento):
    return DenunciaController.get_denuncias_by_denunciado(documento)


@denuncias_bp.route("/create", methods=["POST"])
def create_denuncia():
    new_denuncia = DenunciaController.create_denuncia()
    return new_denuncia


@denuncias_bp.route("/denuncias/<int:id>", methods=["PUT"])
def update_denuncia(id):
    data = request.get_json()
    updated_denuncia = DenunciaController.update_denuncia(id, data)
    if updated_denuncia:
        return jsonify(updated_denuncia.to_dict()), 200
    return jsonify({"message": "Denuncia not found"}), 404


@denuncias_bp.route("/denuncias/<int:id>", methods=["DELETE"])
def delete_denuncia(id):
    deleted_denuncia = DenunciaController.delete_denuncia(id)
    if deleted_denuncia:
        return jsonify({"message": "Denuncia deleted successfully"}), 200
    return jsonify({"message": "Denuncia not found"}), 404
