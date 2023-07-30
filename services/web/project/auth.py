from project.models import db, User
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


def create_user():
    data = request.json
    if request.method == "POST":
        username = data["username"]
        password = data["password"]

        error = None

        if error is None:
            try:
                if User.query.filter_by(username=username).first() is None:
                    user = User(username=username, password=password)
                    db.session.add(user)
                    db.session.commit()

                else:
                    raise Exception("user")

            except Exception:
                return {"message": "User already exist"}
    return {"message": "User created successfully"}


def login_user():
    data = request.json
    if request.method == "POST":
        username = data["username"]
        password = data["password"]

        error = None

        user = User.query.filter_by(username=username, password=password).first()
        if user is None:
            error = "Incorrect username or password"
            print(error)

        current_user = User.query.filter_by(username=username).first()
        if error is None:
            session["user_id"] = current_user.id

            # token = jwt.encode({'user_id': current_user.id}, app.config['SECRET_KEY'], 'HS256')

            payload = {
                "user_id": current_user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
            return make_response(jsonify({"token": token}), 201)
        return {"message": "Invalid username or password"}


# def login_required(redirect_url):
#     def decorator(view):
#         @wraps(view)
#         def wrapped_view(**kwargs):
#             user = session.get('user_id')
#             if user is None:
#                 return redirect(url_for(redirect_url))

#             return view(**kwargs)
#         return wrapped_view
#     return decorator


def token_required(view):
    @wraps(view)
    def decorator(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return make_response(
                jsonify({"message": "A valid token is missing !"}), 401
            )

        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user_id = session.get("user_id")

        except Exception:
            return make_response(jsonify({"message": "Invalid token!"}), 401)

        return view(current_user_id, *args, **kwargs)

    return decorator
