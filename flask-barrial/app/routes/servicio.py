from flask import Blueprint, jsonify, request
from app.controllers.servicio_controller import ServicioController

from app.models.models import Servicio, Foto

from app import db

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to services api!"})

@servicios_bp.route('/all', methods=['GET'])
def get_all_servicios():
    servicios = ServicioController.get_all_servicios()
    print(servicios)
    return servicios

@servicios_bp.route('/<string:idUser>', methods=['GET'])
def get_servicios_by_user(idUser):
    servicios = ServicioController.get_servicios_by_user(idUser)
    return servicios

@servicios_bp.route('/create', methods=['POST'])
def create_servicio():
    data = request.form
    print(data)
    servicios = ServicioController.create_servicio(data)
    print(servicios)
    return servicios