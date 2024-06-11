from flask import Blueprint, jsonify, request
from app.controllers.servicio_controller import ServicioController

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to services api!"})

@servicios_bp.route('/all', methods=['GET'])
def get_all_servicios():
    servicios = ServicioController.get_all_servicios()
    return servicios

@servicios_bp.route('/<string:idUser>', methods=['GET'])
def get_servicios_by_user(idUser):
    servicios = ServicioController.get_servicios_by_user(idUser)
    return servicios

@servicios_bp.route('/create', methods=['POST'])
def create_servicio():
    data = request.form.to_dict()
    servicios = ServicioController.create_servicio(data)
    return servicios