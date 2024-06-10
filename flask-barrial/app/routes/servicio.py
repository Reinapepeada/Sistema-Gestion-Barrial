from flask import Blueprint, jsonify
from app.controllers.servicio_controller import ServicioController

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to services api!"})

@servicios_bp.route('/all', methods=['GET'])
def get_all_servicios():
    servicios = ServicioController.get_all_servicios()
    return jsonify([servicio.to_dict() for servicio in servicios])

@servicios_bp.route('/<string:idUser>', methods=['GET'])
def get_servicios_by_user(idUser):
    return jsonify({"message": f"get services by user {idUser}"})

@servicios_bp.route('/create', methods=['POST'])
def create_servicio():
    return jsonify({"message": "create service"})