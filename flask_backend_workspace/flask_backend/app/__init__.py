from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from .routes.health import blp as health_blp
from .routes.users import blp as users_blp
from .routes.tasks import blp as tasks_blp
from .models import db

app = Flask(__name__)

# Configuration
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "My Flask API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
api = Api(app)

# Register Blueprints
api.register_blueprint(health_blp)
api.register_blueprint(users_blp)
api.register_blueprint(tasks_blp)
