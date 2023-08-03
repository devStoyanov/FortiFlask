from flask import jsonify, request
from flask import current_app as app
from project.models import db, Contacts
from collections import OrderedDict
from project.schemas import ContactsData
from pydantic import ValidationError
import jwt


def data():
    token = request.headers.get("x-access-token")
    decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = decoded_token["user_id"]

    # Decode the JWT token, by extracting the user_id, use it to query the database table.
    if request.method == "GET":
        contacts = Contacts.query.filter(Contacts.creator_id == user_id).all()

        if contacts == []:
            return {"message": f"No contacts for user with id {user_id}"}, 404

        # Take contact parameter and use OrderedDict to qurantee the returned order
        def convert_to_note(contact):
            contact_data = OrderedDict()
            contact_data["id"] = contact.id
            contact_data["creator_id"] = contact.creator_id
            contact_data["is_organization"] = contact.is_organization
            contact_data["name"] = contact.name
            contact_data["first_name"] = contact.first_name
            contact_data["last_name"] = contact.last_name
            contact_data["title"] = contact.title
            contact_data["email"] = contact.email
            contact_data["mobile"] = contact.mobile
            contact_data["address"] = contact.address
            contact_data["description"] = contact.description
            contact_data["tags"] = contact.tags
            contact_data["created_at"] = contact.created_at
            contact_data["updated_at"] = contact.updated_at
            return contact_data

        # Comprehension list and for cycle with map function to return the data.
        result = [
            ({"data": contact_data}) for contact_data in map(convert_to_note, contacts)
        ]
        print(result)
        return jsonify(result), 200

    elif request.method == "POST":
        contacts = request.json

        try:
            contact = ContactsData(**contacts)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        new_contact = Contacts(
            creator_id=user_id,
            is_organization=contacts["is_organization"],
            name=contacts["name"],
            first_name=contacts["first_name"],
            last_name=contacts["last_name"],
            title=contacts["title"],
            email=contacts["email"],
            address=contacts["address"],
            description=contacts["description"],
            tags=contacts["tags"],
        )

        db.session.add(new_contact)
        db.session.commit()

        return {"message": "Contact created successfully"}, 200

    # method to DELETE all data for current user currently
    # disabled uncomment it to enable it back.

    # elif request.method == "DELETE":
    #     contacts = Contacts.query.filter(Contacts.creator_id == user_id).all()

    #     for contact in contacts:
    #         db.session.delete(contact)

    #     db.session.commit()

    #     return {"message": "All data has been deleted"}, 200


def update_note(id):
    token = request.headers.get("x-access-token")
    decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = decoded_token["user_id"]

    if request.method == "GET":
        contacts = Contacts.query.filter(
            db.and_(Contacts.creator_id == user_id, Contacts.id == id)
        ).first()

        if contacts is None:
            return {"message": f"No contact with id: {id}"}, 404

        # Return the data as dictionary as key: "" and a
        # value: "the corresponding column from contacts table"
        result = {
            "id": contacts.id,
            "creator_id": contacts.id,
            "is_organizaiton": contacts.is_organization,
            "name": contacts.name,
            "first_name": contacts.first_name,
            "last_name": contacts.last_name,
            "title": contacts.title,
            "email": contacts.email,
            "mobile": contacts.mobile,
            "address": contacts.address,
            "description": contacts.description,
            "tags": contacts.tags,
            "created_at": contacts.created_at,
            "updated_at": contacts.updated_at,
        }
        return jsonify(result), 200

    elif request.method == "DELETE":
        # Delete contact by id by checking current user id
        # which corresponding to creators_id in Contacts table
        contact = Contacts.query.filter(
            db.and_(Contacts.creator_id == user_id, Contacts.id == id)
        ).first()

        if contact is None:
            return {"message": f"No contact with id: {id}"}, 404

        db.session.delete(contact)
        db.session.commit()

        return {"message": f"Contact with id: {id} is successfully deleted"}, 200

    elif request.method == "PUT":
        data = request.json

        try:
            contact_data = ContactsData(**data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        contact = Contacts.query.filter(
            db.and_(Contacts.creator_id == user_id, Contacts.id == id)
        ).first()

        if contact is None:
            return {"message": f"No contact with id: {id}"}, 404

        # Update the existing contact with given information as json request
        contact.is_organization = data["is_organization"]
        contact.name = data["name"]
        contact.first_name = data["first_name"]
        contact.last_name = data["last_name"]
        contact.title = data["title"]
        contact.email = data["email"]
        contact.mobile = data["mobile"]
        contact.address = data["address"]
        contact.description = data["description"]
        contact.tags = data["tags"]

        db.session.commit()

        return {"message": "Contact has been updated"}, 200
