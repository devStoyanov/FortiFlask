import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Configure the database DATABASE_URL as environment variable
    # which is defined in env.prod
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
