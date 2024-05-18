from flask import Blueprint, jsonify

denuncia_bp = Blueprint('denuncia', __name__)

@denuncia_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to denuncias api!"})