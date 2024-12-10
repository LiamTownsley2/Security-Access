from flask import Flask, jsonify, request, abort
import logging
import os 
app = Flask(__name__)

# disable flask logging
logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

test_data = ["Alpha", "Bravo", "Charlie"]

def initialize_api():
    app.run('0.0.0.0', debug=False, use_reloader=False)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(test_data)), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = test_data[user_id]
    if user is None:
        abort(404, description="User not found")
    return jsonify(user), 200