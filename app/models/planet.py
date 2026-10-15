from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
'''
class Planet:
    def __init__(self, id, name, description, color):
        self.id = id
        self.name = name
        self.description = description
        self.color = color

planets = [
    Planet(1,"Earth","Our planet", "blue"),
    Planet(2, "Mars", "The red planet", "red"),
    Planet(3, "Venus", "A hot planet", "yellow")
]
'''

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    color: Mapped[str]
