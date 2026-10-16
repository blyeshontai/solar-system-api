from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

#edited the previous code from before the database existed.

#inheriting from db.Model makes Planet a database table
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   #id is an int primary key, autoincrement so you don't have to send an id in a POST
    name: Mapped[str]                                                       #mapped str is required text column + color
    description: Mapped[str]
    color: Mapped[str]

#consider creating a to_dict() method sos that the same four key dictionary isn't written out multiple times
