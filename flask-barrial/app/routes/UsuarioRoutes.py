from flask import Blueprint, jsonify

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to users api!"})