from flask import Blueprint, jsonify

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to services api!"})