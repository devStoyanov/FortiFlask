from flask import Flask
import os
from project.config_sw import swaggerui_blueprint
from flask_cors import CORS
from project.models import init_db
from project.routes import main
from project.swagger import swagger


app = Flask(__name__)

app.config.from_object("project.config.Config")

# initialize the database
init_db(app)

# Configure app SECRET_KEY to be taken as an env variable
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Set sort_keys to False in order to return
# the json data in the order you submit it
app.json.sort_keys = False

# Set session lifetime to be 10 minutes.
app.permanent_session_lifetime = 600

app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(main)
app.register_blueprint(swagger)
CORS(app)
