from flask import Flask                         #import flask
from .routes.planet_routes import planets_bp    #blueprint that holds the planet routes
from .db import db, migrate                     #brings in the shared db and migrage objects
from .models import planet                      #imports models module so Flask-Migrate can see the table
import os                                       #read environment variables

#BUILD THE APP
def create_app(test_config=None):
    app = Flask(__name__)                       #creates flask app

    '''Before Wave 6
    #tells sql alchemy which database to connect to
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/solar_system_development"
    '''

    #Wave 6
    if test_config is not None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')




    #attach the database and migration tools to this specific app
    db.init_app(app)
    migrate.init_app(app, db)

    #registers the planet routes to the app knows about /planets
    app.register_blueprint(planets_bp)

    #returns the finished app
    return app
