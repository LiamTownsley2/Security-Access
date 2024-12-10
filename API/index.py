import logging

from flask import Flask
from .routes import _routes

app = Flask(__name__)

# disable flask logging
logging.getLogger('werkzeug').disabled = True

_routes.initilize_routes(app)

def initialize_api():
    app.run('0.0.0.0', debug=False, use_reloader=False)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"