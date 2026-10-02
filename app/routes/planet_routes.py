from flask import Blueprint
from app.models.planet import planets

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")
#Wave 1: Get all planets
@planets_bp.get("")
def get_all_planets():
    planets_response = []

    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "color": planet.color,
            }
        )
    return planets_response

#Wave2: Get one planet and handle errors