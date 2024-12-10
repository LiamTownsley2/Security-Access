from flask import Blueprint, jsonify, request, abort
from AWS import db 

bp_cards = Blueprint('cards', __name__)

@bp_cards.route('/card/<int:card_id>', methods=['GET'])
def read_card():
    data = request.get_json()
    try:
        user = db.get_user_by_card(data['CardID'])
        if user is None:
            abort(404, description="This keycard is not linked to an Employee.")
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400