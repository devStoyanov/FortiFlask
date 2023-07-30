from typing import Any
from flask import jsonify, request
from flask import current_app as app
from project.models import db, Contacts
from collections import OrderedDict

import jwt


def data():
    token = request.headers.get("x-access-token")
    decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = decoded_token["user_id"]

    if request.method == "GET":
        notes = Contacts.query.filter(Contacts.creator_id == user_id).all()

        if notes == []:
            return {"message": "No notes in database"}, 404

        def convert_to_note(note):
            note_data = OrderedDict()
            note_data["id"] = note.id
            note_data["creator_id"] = note.creator_id
            note_data["is_organization"] = note.is_organization
            note_data["name"] = note.name
            note_data["first_name"] = note.first_name
            note_data["last_name"] = note.last_name
            note_data["title"] = note.title
            note_data["email"] = note.email
            note_data["mobile"] = note.mobile
            note_data["address"] = note.address
            note_data["description"] = note.description
            note_data["tags"] = note.tags
            note_data["created_at"] = note.created_at
            note_data["updated_at"] = note.updated_at
            return note_data

        result = [({"data": note_data}) for note_data in map(convert_to_note, notes)]
        print(result)
        return jsonify(result)

    elif request.method == "POST":
        notes = request.json
        new_note = Contacts(
            creator_id=user_id,
            is_organization=notes["is_organization"],
            name=notes["name"],
            first_name=notes["first_name"],
            last_name=notes["last_name"],
            title=notes["title"],
            email=notes["email"],
            address=notes["address"],
            description=notes["description"],
            tags=notes["tags"],
        )

        db.session.add(new_note)
        db.session.commit()

        return {"message": "Note created successfully"}, 200

    elif request.method == "DELETE":
        notes = Contacts.query.filter(Contacts.creator_id == user_id).all()

        for note in notes:
            db.session.delete(note)

        db.session.commit()

        return {"message": "All data has been deleted"}, 200


def update_note(id):
    token = request.headers.get("x-access-token")
    decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = decoded_token["user_id"]

    if request.method == "GET":
        notes = Contacts.query.filter(
            db.and_(Contacts.creator_id == user_id, Contacts.id == id)
        ).first()

        if notes is None:
            return {"message": f"No note with id: {id}"}, 404

        result = {
            "id": notes.id,
            "creator_id": notes.id,
            "is_organizaiton": notes.is_organization,
            "name": notes.name,
            "first_name": notes.first_name,
            "last_name": notes.last_name,
            "title": notes.title,
            "email": notes.email,
            "mobile": notes.mobile,
            "address": notes.address,
            "description": notes.description,
            "tags": notes.tags,
            "created_at": notes.created_at,
            "updated_at": notes.updated_at,
        }
        return jsonify(result)

    elif request.method == "DELETE":
        note = Contacts.query.filter(
            db.and_(Contacts.creator_id == user_id, Contacts.id == id)
        ).first()

        if note is None:
            return {"message": f"No note with id: {id}"}, 404

        db.session.delete(note)
        db.session.commit()

        return {"message": "Note is successfully deleted"}, 200

    elif request.method == "PUT":
        data = request.json
        note = Contacts.query.filter(
            db.and_(Contacts.creator_id == user_id, Contacts.id == id)
        ).first()

        if note is None:
            return {"message": f"No note with id: {id}"}, 404

        note.is_organization = data["is_organization"]
        note.name = data["name"]
        note.first_name = data["first_name"]
        note.last_name = data["last_name"]
        note.title = data["title"]
        note.email = data["email"]
        note.mobile = data["mobile"]
        note.address = data["address"]
        note.description = data["description"]
        note.tags = data["tags"]

        db.session.commit()

        return {"message": "Note has been updated"}, 200


# def get_resource(resource):
#     token = request.headers.get('x-access-token')
#     decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#     user_id = decoded_token['user_id']

#     if request.method == 'GET':

#         notes = Notes.query.filter(db.and_(Notes.creator_id == user_id,
#                                     Notes.resource_type == resource)).first()

#         if notes is None:
#             return {'message': f'No resource of this type: {resource}'}, 404

#         result = {"id": notes.id,
#             "creator_id": notes.id,
#             "is_organizaiton": notes.is_organization,
#             "name": notes.name,
#             "first_name": notes.first_name,
#             "last_name": notes.last_name,
#             "title": notes.title,
#             "email": notes.email,
#             "mobile": notes.mobile,
#             "address": notes.address,
#             "description": notes.description,
#             "tags": notes.tags,
#             "created_at": notes.created_at,
#             "updated_at": notes.updated_at
#             }
#         return jsonify(result)
