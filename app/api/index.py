import logging

from flask import Flask, jsonify
from .routes import accessLog, camera, card, user
import os
import multiprocessing
from classes.RFID_Reader import door_controller
import traceback

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
    api_status = True


def toggle_api_status(stdscr):
    if get_api_status():
        destroy_api()
    else:
        initialize_api()
    stdscr.refresh()
    return


def get_api_status():
    global api_status
    return api_status


def destroy_api():
    global api_status
    api_process.terminate()
    api_process.join()
    api_status = False


@app.route("/")
def hello_world():
    return jsonify("Hello World"), 200

@app.route("/lockout", methods=["POST"])
def set_lockout():
    try:
        state = door_controller.get_state()
        door_controller.set_lockout(not state)
    
        return jsonify({{"locked_out": str(not state)}}), 200
    except Exception as e:
        return jsonify({"error": e, "stack": traceback.format_exc()}), 400