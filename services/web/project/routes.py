from flask import render_template, Blueprint
from project.auth import create_user
from project.auth import login_user
from project.views import data
from project.views import update_note
from project.auth import token_required


main = Blueprint("main", __name__)


@main.route("/user", methods=["GET", "POST"])
def new_user():
    user = create_user()

    return user


@main.route("/", methods=["GET", "POST"])
def main_page():
    return render_template("index.html")


@main.route("/user/login", methods=["GET", "POST"])
def log_user():
    user = login_user()
    return user


@main.route("/contacts", methods=["GET", "POST", "DELETE"])
@token_required
def get_contact(token):
    notes = data()
    return notes


@main.route("/contacts/<id>", methods=["GET", "DELETE", "PUT"])
@token_required
def update_data(token, id="id"):
    note = update_note(id)
    return note
