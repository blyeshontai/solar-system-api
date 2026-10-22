from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import db

#edited the previous code from before the database existed.

#inheriting from db.Model makes Planet a database table
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   #id is an int primary key, autoincrement so you don't have to send an id in a POST
    name: Mapped[str]                                                       #mapped str is required text column + color
    description: Mapped[str]
    color: Mapped[str]
    moons: Mapped[list["Moon"]] = relationship(back_populates="planet")      #relationship to moon, back_populates is the other side of the relationship

    def to_dict(self):                                                      # Wave 7: to_dict converts a Planet object into a dictionary to avoid repeating the same dictionary code. 
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "moons": [moon.to_dict() for moon in self.moons]              # Wave 7: include moons in the dictionary representation of a Planet
            
        }
    @classmethod
    def from_dict(cls, planet_data):                                         # Wave 7: creates a new Planet object from dictionary data. 
        new_planet = cls(                              
            name=planet_data["name"],
            description=planet_data["description"],
            color=planet_data["color"],
        )
        return new_planet