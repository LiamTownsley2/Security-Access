import logging

from flask import Flask, jsonify
from routes import accessLog, camera, card, user

app = Flask(__name__)

# disable flask logging
logging.getLogger('werkzeug').disabled = True

app.register_blueprint(accessLog.bp_access_log)
app.register_blueprint(camera.bp_cameras)
app.register_blueprint(card.bp_cards)
app.register_blueprint(user.bp_user)

def initialize_api():
    app.run('0.0.0.0', debug=False, use_reloader=False)

@app.route("/")
def hello_world():
    return jsonify("Hello World"), 200