from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

db = SQLAlchemy()


# Use to initialize the database.
# def init_db(app):
#     db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    data_added = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)
    is_organization = db.Column(db.Boolean, default=False, nullable=True)
    name = db.Column(db.String(50), default=None, nullable=True)
    first_name = db.Column(db.String(50), default=None, nullable=True)
    last_name = db.Column(db.String(50), default=None, nullable=True)
    title = db.Column(db.String(50), default=None, nullable=True)
    email = db.Column(db.String(50), default=None, nullable=True)
    mobile = db.Column(db.Integer, default=None, nullable=True)
    address = db.Column(db.String(100), default=None, nullable=True)
    description = db.Column(db.String(200), default=None, nullable=True)
    tags = db.Column(db.String(50), default=None, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Notes {self.title}>"
