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
    return [
        {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "color": planet.color,
        }
        for planet in planets
    ]

# WAVE 4 - GET ONE PLANET (from Wave 2)
@planets_bp.get("/<planet_id>")            
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)  

    #return that single planet as a dictionary
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "color": planet.color,
    }

#PUT/UPDATE ONE PLANET - WAVE 4
@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id) 
    request_body = request.get_json()   

   
    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.color = request_body["color"]
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

#DELETE ONE PLANET - WAVE 4
@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    
    planet = validate_planet(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")



#POST A PLANET - WAVE 3
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

    #return new planet
    return {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "color": new_planet.color,
    }, 201


# WAVE 2 VALIDATION - UPDATED FOR DATABASE IN WAVE 4
#VALIDATE PLANET
def validate_planet(planet_id):
    try: 
        #try converting the URL value to an int
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
