from flask import Blueprint, render_template
from aws import db

bp_dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

users = []
@bp_dashboard.route("/", methods=["GET"])
def dashboard_index():
    global users
    users = db.get_all_users()
    return render_template("dashboard.html", users=users)