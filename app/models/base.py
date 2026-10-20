from sqlalchemy.orm import DeclarativeBase #the parent class every model is built from

#create an empty base class because SQLAlchemy requires every model to inherit from a shared base
class Base(DeclarativeBase):
    pass
