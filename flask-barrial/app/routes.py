from flask import Blueprint, jsonify

item_bp = Blueprint('main', __name__)

@item_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})