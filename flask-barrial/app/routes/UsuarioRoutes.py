from flask import Blueprint, jsonify
from app import db
from app.models.models import Vecinos
from sqlalchemy import select

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to users api!"})

@usuario_bp.route('/all', methods=['GET'])
def all():
    vecinosAll = db.session.execute(db.select(Vecinos)).scalars()
    vecinos = []
    for vecino in vecinosAll:
        vecinos.append({
            "documento": vecino.documento,
            "nombre": vecino.nombre,
            "apellido": vecino.apellido,
            "direccion": vecino.direccion,
            "codigoBarrio": vecino.codigoBarrio
        })
    return jsonify(vecinos)

    