from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
#from app.models.planet import planets
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

#Wave 1: Get all planets
@planets_bp.get("")
def get_all_planets():
    planets = db.session.scalars(db.select(Planet).order_by(Planet.id))
    return [
        {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "color": planet.color,
        }
        for planet in planets
    ]

'''
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
'''

#Wave 2: Validate one planet
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)

    except ValueError:
        response = {"message": f"planet {planet_id} invalid"}
        abort(make_response(response,400))

    for planet in planets:
        if planet.id == planet_id:
            return planet

    response = {"message": f"planet{planet_id} not found"}
    abort(make_response(response, 404))

# Will rewrite these to query the database in the next wave
'''
#Wave 2: Get one planet

@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet_id,
        "name": planet.name,
        "description": planet.description,
        "color": planet.color,



    }
'''
#Wave 3
@planets_bp.post("")
def create_planet():
    request_body = request.get_json()

    new_planet = Planet(
        name = request_body["name"],
        description = request_body["description"],
        color = request_body["color"],
    )
    db.session.add(new_planet)
    db.session.commit()

    return {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "color": new_planet.color,
    }, 201
