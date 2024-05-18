from flask import Blueprint, jsonify

reclamo_bp = Blueprint('reclamo', __name__)

@reclamo_bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "welcome to reclamos api!"})