from aws import S3
from flask import Blueprint, abort, jsonify
import logging

bp_cameras = Blueprint("camera", __name__, url_prefix="/camera")


@bp_cameras.route("/", methods=["GET"])
def view_camera():
    try:
        return abort(404, description="Not implemented.")
        # return jsonify(response), 200
    except Exception as e:
        logging.error("Error creating user: %s", str(e))
        return jsonify({"error": "An internal error has occurred."}), 400


@bp_cameras.route("/history/unidentified", methods=["GET"])
def view_unidentified_footage():
    try:
        response = S3.get_videos_by_folder("non-identified")
        if response is None or len(response) == 0:
            return abort(404, "No footage found.")
        return jsonify(response), 200
    except Exception as e:
        logging.error("Error creating user: %s", str(e))
        return jsonify({"error": "An internal error has occurred."}), 400


@bp_cameras.route("/history/<int:user_id>", methods=["GET"])
def view_employee_footage(user_id):
    try:
        response = S3.get_videos_by_folder(user_id)
        if response is None or len(response) == 0:
            return abort(404, "No footage found.")
        return jsonify(response), 200
    except Exception as e:
        logging.error("Error creating user: %s", str(e))
        return jsonify({"error": "An internal error has occurred."}), 400
