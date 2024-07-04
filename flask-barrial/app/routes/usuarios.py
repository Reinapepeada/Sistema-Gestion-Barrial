from flask import Blueprint, jsonify
from app import db
from flask import request
from app.models.models import Vecino
from app.controllers.usuario_controller import UsuarioController


usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to users api!"})

@usuarios_bp.route('/all', methods=['GET'])
def all():
    vecinos_select = db.session.execute(db.select(Vecino).order_by(Vecino.codigoBarrio)).scalars()
    vecinos = []
    for vecino in vecinos_select:  
        vecinos.append({
            "documento": vecino.documento,
            "nombre": vecino.nombre,
            "apellido": vecino.apellido,
            "direccion": vecino.direccion,
            "codigoBarrio": vecino.codigoBarrio
        })
    return jsonify(vecinos)

@usuarios_bp.route('/first-login', methods=['post'])
def first_login():
    data = request.get_json()
    print(data)
    return UsuarioController.first_login(data)

@usuarios_bp.route('/login', methods=['post'])
def login():
    data = request.get_json()
    return UsuarioController.login(data)

@usuarios_bp.route('/forgot-password', methods=['post'])
def forgot_password():
    data = request.get_json()
    return UsuarioController.forgot_password(data)

@usuarios_bp.route('/change-password/', methods=['post'])
def change_password():
    data = request.get_json()
    return UsuarioController.change_password(data)

@usuarios_bp.route('/<string:documento>', methods=['GET'])
def get_usuario_by_documento(documento):
    usuario = UsuarioController.get_usuario_by_documento(documento)
    return jsonify(usuario)
    