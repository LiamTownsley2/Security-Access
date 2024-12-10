from flask import Blueprint, jsonify, request, abort
from AWS import S3

bp_cameras = Blueprint('cameras', __name__)

@bp_cameras.route('/camera', methods=['GET'])
def view_camera():
    try:
        return abort(404, description="Not implemented.")
        # return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@bp_cameras.route('/camera/history/unidentified', methods=['GET'])
def view_unidentified_footage():
    try:
        response = S3.get_videos_by_folder("non-identified")
        if response is None or len(response) == 0:
            return abort(404, "No footage found.")
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@bp_cameras.route('/camera/history/<int:user_id>', methods=['GET'])
def view_employee_footage(user_id):
    try:
        response = S3.get_videos_by_folder(user_id)
        if response is None or len(response) == 0:
            return abort(404, "No footage found.")
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400