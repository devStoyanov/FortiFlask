def test_contacts(client, app):
    response = client.get("/contacts")
    assert response.status_code == 401
    assert response.json == {"message": "A valid token is missing !"}


def test_contacts_create(client, app):
    response = client.post("/contacts")
    assert response.status_code == 401
    assert response.json == {"message": "A valid token is missing !"}


def test_contacts_delete(client, app):
    response = client.delete("/contacts")
    assert response.status_code == 401
    assert response.json == {"message": "A valid token is missing !"}


def test_contacts_update(client, app):
    response = client.put("/contacts/<id>")
    assert response.status_code == 401
    assert response.json == {"message": "A valid token is missing !"}
