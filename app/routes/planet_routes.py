#Flask helpers:
    #Blueprint groups related routes together
    #request reads the incoming JSON
    #abort and make_response send error messages
    #Response builds an empty 204 response
from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db
from .route_utilities import validate_model
from app.models.moon import Moon
from app.models.planet import Planet

#create the blueprint, start every route with /planets
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

# WAVE 3 + WAVE 5 - GET ALL PLANETS
# Wave 3 retrieved all planets from the database
# Wave 5 adds optional description and color filters
@planets_bp.get("")
def get_all_planets():

    query = db.select(Planet)

    # WAVE 5
    description_param = request.args.get("description")

    if description_param:
        query = query.where(
            Planet.description.ilike(f"%{description_param}%")
        )

    # WAVE 5
    color_param = request.args.get("color")

    if color_param:
        query = query.where(
            Planet.color.ilike(f"%{color_param}%")
        )

    #wave 5 optional - sorting
    sort_param = request.args.get("sort_by", "id")

    # Dictionary of attributes
    sort_columns = {
    "id": Planet.id,
    "name": Planet.name,
    "description": Planet.description,
    "color": Planet.color,
    }

    # Get column that matches sort_param, or use Planet.id if there's no match
    sort_column = sort_columns.get(sort_param, Planet.id)

    query = query.order_by(sort_column)

    planets = db.session.scalars(query)

    #turn each planet object into a dictionary and converted to JSON automatically with status 200
    return [planet.to_dict() for planet in planets]                 # Wave 7: use to_dict() for each planet

# WAVE 4 - GET ONE PLANET (from Wave 2)
@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)                      # Wave 7: use validate_model for Planet

    return planet.to_dict()                                         # Wave 7: use to_dict() to avoid reapeating code

#PUT/UPDATE ONE PLANET - WAVE 4
@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)                     # Wave 7: use validate_model for Planet
    request_body = request.get_json()


    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.color = request_body["color"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

#DELETE ONE PLANET - WAVE 4
@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):

    planet = validate_model(Planet, planet_id)                      #Wave 7: use validate_model for Planet
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")



#POST A PLANET - WAVE 3
@planets_bp.post("")
def create_planet():
    request_body = request.get_json()

    new_planet = Planet.from_dict(request_body)                     # Wave 7: creates a Planet from the request data and keep the routes clean
    db.session.add(new_planet)
    db.session.commit()

    #return new planet
    return new_planet.to_dict(), 201                                # Wave 7: use to_dict() to avoid reapeating the dictionary code


@planets_bp.post("/<planet_id>/moons")
def create_moon_for_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    new_moon = Moon.from_dict(request_body)
    new_moon.planet = planet
    db.session.add(new_moon)
    db.session.commit()

    #return new planet
    return new_moon.to_dict(), 201


@planets_bp.get("/<planet_id>/moons")
def get_moons_for_planet(planet_id):
    planet = validate_model(Planet, planet_id)                      # Wave 7: use validate_model for Planet

    return [moon.to_dict() for moon in planet.moons], 200
