from flask import Blueprint, jsonify, request, abort
from AWS import db 

bp_access_log = Blueprint('log', __name__, url_prefix='/log')

@bp_access_log.route('/', methods=['GET'])
def read_logs():
    try:
        response = db.get_all_logs()
        if response is None:
            abort(404, description="No logs found.")
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@bp_access_log.route('/<int:user_id>', methods=['GET'])
def read_logs_by_employee(user_id):
    try:
        response = db.get_all_logs(user_id)
        if response is None:
            abort(404, description="No logs found.")
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@bp_access_log.route('/<int:user_id>', methods=['POST'])
def register_entry(user_id):
    data = request.get_json()
    try:
        if not data["TagID"]:
            abort(400, "Missing required TagID variable.")
        db.register_entry(data["TagID"], user_id)
        return jsonify("Success"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400