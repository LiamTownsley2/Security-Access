from flask import Blueprint, render_template
from aws import db
import os

template_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
bp_dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard", template_folder=template_folder)

@bp_dashboard.route("/", methods=["GET"])
def dashboard_index():
    return render_template("dashboard.html")

@bp_dashboard.route("/users", methods=["GET"])
def dashboard_users():
    users = db.get_all_users()
    return render_template("users.html", users=users)