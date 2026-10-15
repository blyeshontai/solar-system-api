from flask import Flask
from .routes.planet_routes import planets_bp

# connect flask to the database
from .db import db, migrate
from .models import planet
from .routes.planet_routes import planets_bp
import os

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(planets_bp)
    return app
