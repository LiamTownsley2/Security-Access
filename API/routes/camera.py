from flask import jsonify, request, abort
from AWS import db 

def initialize_camera_route(app):
    @app.route('/camera', methods=['GET'])
    def view_camera():
        try:
            return abort(404, description="Not implemented.")
            # return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400