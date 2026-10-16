#import the three tools
from flask_sqlalchemy import SQLAlchemy #talks to Postgres
from flask_migrate import Migrate       #tracks changes to the database's table structure
from sqlalchemy.orm import DeclarativeBase #the parent class every model is built from

#create an empty base class because SQLAlchemy requires every model to inherit from a shared base
class Base(DeclarativeBase):
    pass

#db is the single shared database object for the entire app
#models use db.model to read and write
#routes use db.session to read and write
#migrate handles schema changes like when we upgrade
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
