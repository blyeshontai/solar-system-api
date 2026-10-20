#Wave 6
#write a test that checks GET/planets returns 200 as an empty list

def test_get_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []
