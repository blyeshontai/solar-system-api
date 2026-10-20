#import the three tools
from flask_sqlalchemy import SQLAlchemy #talks to Postgres
from flask_migrate import Migrate       #tracks changes to the database's table structure
from sqlalchemy.orm import DeclarativeBase #the parent class every model is built from
from .models.base import Base

#db is the single shared database object for the entire app
#models use db.model to read and write
#routes use db.session to read and write
#migrate handles schema changes like when we upgrade
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
