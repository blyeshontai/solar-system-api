from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

#edited the previous code from before the database existed.

#inheriting from db.Model makes Planet a database table
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   #id is an int primary key, autoincrement so you don't have to send an id in a POST
    name: Mapped[str]                                                       #mapped str is required text column + color
    description: Mapped[str]
    color: Mapped[str]

    def to_dict(self):                                                      # Wave 7: to_dict converts a Planet object into a dictionary to avoid repeating the same dictionary code. 
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
        }
    @classmethod
    def from_dict(cls, planet_data):                                         # Wave 7: creates a new Planet object from dictionary data. 
        new_planet = cls(                              
            name=planet_data["name"],
            description=planet_data["description"],
            color=planet_data["color"],
        )
        return new_planet