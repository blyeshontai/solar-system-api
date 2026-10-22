#Wave 6
#write a test that checks GET/planets returns 200 as an empty list

def test_get_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []



# Wave 6 - writing tests-  getting one planet
def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Mercury",
        "description": "The closest planet to the Sun",
        "color": "Gray",
        "moons": []
    }

#no fixture returns 404
def test_get_one_planet_not_found(client):

    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "planet 1 not found"
    }

# Wave 6 - all data (fixtures) returns 200 and a list of planets
def test_get_all_planets_with_records(client, two_saved_planets):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Mercury",
            "description": "The closest planet to the Sun",
            "color": "Gray",
            "moons": []
        },
        {
            "id": 2,
            "name": "Venus",
            "description": "The second planet from the Sun",
            "color": "Yellow",
            "moons": []
        }
    ]

# Wave 6 - create (post) new planet returns 201 and the new planet data
def test_create_planet(client):
    # Arrange
    new_planet = {
        "name": "Venus",
        "description": "The second planet from the Sun",
        "color": "Yellow"
    }

    # Act
    response = client.post("/planets", json=new_planet)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Venus",
        "description": "The second planet from the Sun",
        "color": "Yellow",
        "moons": []
    }