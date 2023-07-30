from flask import Blueprint, jsonify, json
from flask_swagger_ui import get_swaggerui_blueprint


swagger_bp = Blueprint("swagger", __name__, url_prefix="/")

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.yml"
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={"app_name": "Test API"},  # Swagger UI config overrides
)
swagger_bp.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@swagger_bp.route("/swagger.yml")
def swagger():
    with open("swagger.yml", "r") as f:
        return jsonify(json.load(f))


app_blueprint = swagger_bp
