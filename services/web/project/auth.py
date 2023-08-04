from project.models import db, User
from project.schemas import UserData
from pydantic import ValidationError
from flask import (
    request,
    session,
    jsonify,
    make_response,
    current_app as app,
)
from functools import wraps
import jwt
import datetime


# Create a new user
def create_user():
    data = request.json
    if request.method == "POST":
        try:
            user_data = UserData(**data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        error = None

        if error is None:
            try:
                # Check if the username is present in database
                # if it is not, use the username and password from request.method
                # to create  a new user
                if User.query.filter_by(username=user_data.username).first() is None:
                    user = User(
                        username=user_data.username, password=user_data.password
                    )
                    db.session.add(user)
                    db.session.commit()

                else:
                    raise Exception("user")
            # Return exception if username already in use
            except Exception:
                return {"message": "User already exist"}
    return {"message": "User created successfully"}


# Login existing users
def login_user():
    data = request.json
    if request.method == "POST":
        try:
            user_data = UserData(**data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        error = None

        # Check if username and password are present in database
        user = User.query.filter_by(
            username=user_data.username, password=user_data.password
        ).first()
        if user is None:
            error = "Incorrect username or password"
            print(error)

        # Take the current (logged in) user and save the user.id in session["user_id"]
        current_user = User.query.filter_by(username=user_data.username).first()
        if error is None:
            session["user_id"] = current_user.id

            # Create token payload which will contain the user_id
            # set token expiration time of 1 hour.
            payload = {
                "user_id": current_user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            # Encode the payload  in jwt token
            token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
            return make_response(jsonify({"token": token}), 201)
        return {"message": "Invalid username or password"}


def token_required(view):
    @wraps(view)
    # Decorate function which will replace the
    # view function when the decorator is used
    def decorator(*args, **kwargs):
        token = None
        # Check if "x-access-token" is present in the request headers
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return make_response(
                jsonify({"message": "A valid token is missing !"}), 401
            )

        try:
            # Decode the jwt token using the app's 'SECRET_KEY'
            # and HS256 algorithm for token validation
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user_id = session.get("user_id")

        except Exception:
            return make_response(jsonify({"message": "Invalid token!"}), 401)
        # Return original view function with user.id obtained from the token.
        return view(current_user_id, *args, **kwargs)

    return decorator
