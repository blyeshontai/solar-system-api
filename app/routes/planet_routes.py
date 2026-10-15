from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
#from app.models.planet import planets
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

#GET PLANET
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

#GET ONE PLANET
@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "color": planet.color,
    }

#UPDATE ONE PLANET
@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.color = request_body["color"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

#DELETE ONE PLANET
@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

#POST A PLANET
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

#VALIDATE PLANET
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        response = {"message": f"planet {planet_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)

    if not planet:
        response = {"message": f"planet {planet_id} not found"}
        abort(make_response(response, 404))

    return planet
