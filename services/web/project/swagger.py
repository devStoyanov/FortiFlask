from flask import Blueprint, request, jsonify
from random import randrange
from datetime import datetime
from project.schemas import UserData, ContactsData
from pydantic import ValidationError
import json


swagger = Blueprint("swagger", __name__)


# Return current  year/mounth/day and time in hours/minutes/seconds
def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# User test data as list containing dictionaries
# for swagger documentation.
user_data = [{"id": " ", "username": " ", "password": " ", "created_at": " "}]


# Function which create user with given information as json request.
@swagger.route("/test-user", methods=["POST"])
def add_user():
    data = request.get_json()

    # Use of defined schema for User to validate  json request data
    try:
        user = UserData(**data)

    except ValidationError as e:
        return (json.dumps(e.errors(), indent=4)), 400

    for i in range(len(user_data)):
        if user_data[i]["username"] == user.username:
            return {"message": "User already exist"}, 401

    else:
        # Create a new user as a dictionary(new_user)
        new_user = {
            "id": randrange(1, 10),
            "username": user.username,
            "password": user.password,
            "created_at": get_timestamp(),
        }

        # Append a new_user dicitionary to existing user_data
        user_data.append(new_user)
        print("User", user_data)

    return jsonify({"message": "User created successfully"}), 200


# Login existing users
@swagger.route("/test-user/login", methods=["POST"])
def log_in_user():
    data = request.get_json()

    try:
        user = UserData(**data)

    except ValidationError as e:
        return json.dumps(e.errors(), indent=4)

    # For loop which check if the user already persists in user_data
    # if user exist the return message contain access token.
    for i in range(len(user_data)):
        if (
            user.username == user_data[i]["username"] and user.password == user_data[i]["password"]
        ):
            print("Username", user_data[i]["username"])
            return {"message": "token: "}, 200
    else:
        return {"message": "Invalid username or password"}, 404


# Test data in form of a list of dictionaries for swagger documentation.
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
        "mobile": "",
        "address": "",
        "description": "",
        "tags": "",
        "created_at": "",
        "updated_at": "",
    }
]


# Return contacts from test_data or
# create a new ones.
@swagger.route("/test-contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "GET":
        # This check statement is to prevent returning of blank test_data.
        if len(test_data) <= 1:
            return {"message": "No contacts in database"}, 404

        return jsonify(test_data[1:]), 200

    # Values with incoming JSON request
    elif request.method == "POST":
        content = request.get_json()

        # User of defined schema for Contacts to validate json request data
        try:
            contact = ContactsData(**content)
        except ValidationError as e:
            return (json.dumps(e.errors(), indent=4)), 400

        # Store data in  a new dictionary as key:value pairs
        new_contact = {
            "id": randrange(1, 10),
            "creator_id": randrange(1, 10),
            "is_organization": contact.is_organization,
            "name": contact.name,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "title": contact.title,
            "email": contact.email,
            "mobile": contact.mobile,
            "address": contact.address,
            "description": contact.description,
            "tags": contact.tags,
            "created_at": get_timestamp(),
            "updated_at": "null",
        }

        test_data.append(new_contact)

        return jsonify({"message": "Note created successfully"}), 200


# Return contact by id or update and delete it.
@swagger.route("/test-contacts/<int:id>", methods=["GET", "PUT", "DELETE"])
def update_contact(id):
    if request.method == "GET":
        get_contact = []

        # Check if contact is in test_data by id
        # append it to blank list (get_contact)
        for i in range(len(test_data)):
            if test_data[i]["id"] == id:
                get_contact.append(test_data[i])

                return get_contact, 200
        else:
            return {"message": f"Contact with id: {id} not found"}, 404

    elif request.method == "PUT":
        content = request.get_json()

        # For loop which check if dictionary in test_data
        # contain "id" key with id which is introduced as а parameter
        for i in range(len(test_data)):
            if test_data[i]["id"] == id:
                try:
                    contact = ContactsData(**content)
                except ValidationError as e:
                    return (json.dumps(e.errors(), indent=4)), 400

                test_data[i] = {
                    "id": id,
                    "creator_id": test_data[i]["creator_id"],
                    "is_organization": contact.is_organization,
                    "name": contact.name,
                    "first_name": contact.first_name,
                    "last_name": contact.last_name,
                    "title": contact.title,
                    "email": contact.email,
                    "mobile": contact.mobile,
                    "address": contact.address,
                    "description": contact.description,
                    "tags": contact.tags,
                    "created_at": test_data[i]["created_at"],
                    "updated_at": get_timestamp(),
                }
                return jsonify({"message": "Note updated successfully"}), 200
        else:
            return {"message": f"Contact with id {id} not found"}, 404

    elif request.method == "DELETE":
        for i in range(len(test_data)):
            if test_data[i]["id"] == id:
                del test_data[i]

                return {"message": "Contact has been deleted"}, 200

        else:
            return {"message": f"Contact with id: {id} not exist"}, 404
