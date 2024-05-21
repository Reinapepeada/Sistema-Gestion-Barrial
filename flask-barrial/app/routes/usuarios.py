from flask import Blueprint, jsonify
from app import db
from app.models.models import Vecino
from sqlalchemy import select

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

    