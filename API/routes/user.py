from flask import Blueprint, jsonify, request, abort
from AWS import db 

bp_user = Blueprint('users', __name__)

@bp_user.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        response = db.register_user(data['name'])
        return jsonify({"message": "User created.", "response": response}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp_user.route('/user', methods=['GET'])
def get_users():
    return jsonify(list(db.get_all_users())), 200

@bp_user.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.get_user(user_id)
    if user is None:
        abort(404, description="User not found")
    return jsonify(user), 200

@bp_user.route('/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.get_json()
    user = db.get_user(user_id)
    if user is None:
        abort(404, description="User not found")
    name = data['name'] if data['name'] else None
    card_id = data['card_id'] if data['card_id'] else None
    last_scanned = data['last_scanned'] if data['last_scanned'] else None
    edited_user = db.edit_user(user_id, name, card_id, last_scanned)
    return jsonify(edited_user), 200

@bp_user.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.delete_user(user_id)
    if user is None:
        abort(404, description="User not found")
    return jsonify(user), 200