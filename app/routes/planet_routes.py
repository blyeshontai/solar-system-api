#Flask helpers:
    #Blueprint groups related routes together
    #request reads the incoming JSON
    #abort and make_response send error messages
    #Response builds an empty 204 response
from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db

#create the blueprint, start every route with /planets
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

#GET PLANET
@planets_bp.get("")
def get_all_planets():
    #builds the query 'select all planets, sorted by id' runs and returns Planet objects using 'db.dession.scalars it runs it and returns Planet objects
    planets = db.session.scalars(db.select(Planet).order_by(Planet.id))

    #turn each planet object into a dictionary and converted to JSON automatically with status 200
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
@planets_bp.get("/<planet_id>")             #grabs url and passes it into the function as a string
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)     #handles the loopup and error checking iwth validate_planet

    #return that single planet as a dictionary
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "color": planet.color,
    }

#PUT/UPDATE ONE PLANET
@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id) #find the planet or stop early with 400 or 404
    request_body = request.get_json()   #reads the JSON body the client sent

    #overwrite with new values, commit changes to the database
    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.color = request_body["color"]
    db.session.commit()

    #returns 204 No Content
    return Response(status=204, mimetype="application/json")

#DELETE ONE PLANET
@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    #finds the planet
    planet = validate_planet(planet_id)
    #mark it for delition then commit
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")



#POST A PLANET
@planets_bp.post("")
def create_planet():
    request_body = request.get_json()               #reads the JSON body

    new_planet = Planet(                            #build a new 'Planet' from the body. No id is given because database auto assigns
        name = request_body["name"],
        description = request_body["description"],
        color = request_body["color"],
    )
    db.session.add(new_planet)                      #stages the new row
    db.session.commit()                             #writes the new row, new_planet.id gets filled in

    #return new planet
    return {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "color": new_planet.color,
    }, 201



#VALIDATE PLANET
def validate_planet(planet_id):
    try: #try converting the URL value to an int
        planet_id = int(planet_id)
    except ValueError:
        response = {"message": f"planet {planet_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Planet).where(Planet.id == planet_id) #query for the planet with that id
    planet = db.session.scalar(query)                       #query for the planet with that id. scalar returns 1 object or None

    if not planet:
        response = {"message": f"planet {planet_id} not found"}
        abort(make_response(response, 404))                 #return 404 if nothing is found

    #otherwise return
    return planet
