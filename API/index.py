import logging

from flask import Flask, jsonify
from .routes import accessLog, camera, card, user
import os
import multiprocessing

os.environ["FLASK_RUN_FROM_CLI"] = "false"

app = Flask(__name__)

# disable flask logging
# logging.getLogger('werkzeug').disabled = True
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("flask_app.log"),
    ],
)

app.logger.handlers = logging.getLogger().handlers

app.register_blueprint(accessLog.bp_access_log)
app.register_blueprint(camera.bp_cameras)
app.register_blueprint(card.bp_cards)
app.register_blueprint(user.bp_user)


def run_app():
    app.run("0.0.0.0", debug=False, use_reloader=False)


api_process = multiprocessing.Process(target=run_app, daemon=False)
api_status = False


def initialize_api():
    global api_status
    api_process.start()
    api_status = api_process.is_alive()


def toggle_api_status():
    if get_api_status():
        destroy_api()
    else:
        initialize_api()


def get_api_status():
    global api_status
    return api_status


def destroy_api():
    global api_status
    api_process.terminate()
    api_process.join()
    api_status = api_process.is_alive()


@app.route("/")
def hello_world():
    return jsonify("Hello World"), 200
