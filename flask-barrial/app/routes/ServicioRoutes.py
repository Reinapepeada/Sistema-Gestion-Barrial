from flask import Blueprint, jsonify

servicio_bp = Blueprint('servicio', __name__)

@servicio_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to services api!"})