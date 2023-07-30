from flask import Flask, current_app, jsonify, render_template, request, abort
import os
from project.config_sw import swaggerui_blueprint
from flask_cors import CORS
from random import randrange
from datetime import datetime
from project.auth import create_user
from project.auth import login_user
from project.views import data
from project.views import update_note
from project.auth import token_required
from project.models import init_db

app = Flask(__name__)

app.config.from_object("project.config.Config")

init_db(app)


app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.json.sort_keys = False


app.permanent_session_lifetime = 600

app.register_blueprint(swaggerui_blueprint)
CORS(app)


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


user_data = [{"id": "", "username": "", "password": "", "created_at": ""}]


@app.route("/test-user", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    for i in range(len(user_data)):
        if user_data[i]["username"] == username:
            return {"message": "User already exist"}
    else:
        new_user = {
            "id": randrange(1, 10),
            "username": username,
            "password": password,
            "created_at": get_timestamp(),
        }

        user_data.append(new_user)
        print("User", user_data)

    return jsonify({"message": "User created successfully"})


@app.route("/test-user/login", methods=["POST"])
def log_in_user():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    for i in range(len(user_data)):
        if (
            username == user_data[i]["username"] and password == user_data[i]["password"]
        ):
            print("Username", user_data[i]["username"])
            return {"message": "token: "}
    else:
        return {"message": "Invalid username or password"}


test_data = [
    {
        "id": "",
        "creator_id": "",
        "is_organization": "",
        "name": "",
        "first_name": "",
        "last_name": "",
        "title": "",
        "email": "",
        "address": "",
        "description": "",
        "tags": "",
        "created_at": "",
        "updated_at": "",
    }
]


@app.route("/test-contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "GET":
        if len(test_data) <= 1:
            return {"message": "No contacts in database"}, 404

        return jsonify(test_data[1:]), 200

    elif request.method == "POST":
        content = request.get_json()
        is_organization = content.get("is_organization")
        name = content.get("name")
        first_name = content.get("first_name")
        last_name = content.get("last_name")
        title = content.get("title")
        email = content.get("email")
        address = content.get("address")
        description = content.get("description")
        tags = content.get("tags")

        new_contact = {
            "id": randrange(1, 10),
            "creator_id": randrange(1, 10),
            "is_organization": is_organization,
            "name": name,
            "first_name": first_name,
            "last_name": last_name,
            "title": title,
            "email": email,
            "address": address,
            "description": description,
            "tags": tags,
            "created_at": get_timestamp(),
            "updated_at": "null",
        }

        test_data.append(new_contact)

        return jsonify({"message": "Note created successfully"})


@app.route("/test-contacts/<int:id>", methods=["GET", "PUT", "DELETE"])
def update_contact(id):
    if request.method == "GET":
        get_contact = []
        for i in range(len(test_data)):
            if test_data[i]["id"] == id:
                get_contact.append(test_data[i])

                return get_contact
        else:
            abort(404, f"Contact with id {id} not found")

    elif request.method == "PUT":
        content = request.get_json()
        for i in range(len(test_data)):
            if test_data[i]["id"] == id:
                is_organization = content.get("is_organization")
                name = content.get("name")
                first_name = content.get("first_name")
                last_name = content.get("last_name")
                title = content.get("title")
                email = content.get("email")
                address = content.get("address")
                description = content.get("description")
                tags = content.get("tags")

                test_data[i] = {
                    "id": id,
                    "creator_id": test_data[i]["creator_id"],
                    "is_organization": is_organization,
                    "name": name,
                    "first_name": first_name,
                    "last_name": last_name,
                    "title": title,
                    "email": email,
                    "address": address,
                    "description": description,
                    "tags": tags,
                    "created_at": test_data[i]["created_at"],
                    "updated_at": get_timestamp(),
                }
                return jsonify({"message": "Note updated successfully"})

    elif request.method == "DELETE":
        for i in range(len(test_data)):
            if test_data[i]["id"] == id:
                del test_data[i]

                return {"message": "Contact has been deleted"}

        else:
            abort(404, f"Contact with id {id} exist")


@app.route("/user", methods=["GET", "POST"])
def new_user():

    user = create_user()

    return user


@app.route("/", methods=["GET", "POST"])
def main_page():
    return render_template("index.html")


@app.route("/user/login", methods=["GET", "POST"])
def log_user():

    user = login_user()
    return user


@app.route("/contacts", methods=["GET", "POST", "DELETE"])
@token_required
def get_notes(token):

    notes = data()
    return notes


@app.route("/contacts/<id>", methods=["GET", "DELETE", "PUT"])
@token_required
def update_data(token, id="id"):

    note = update_note(id)
    return note
