from project.models import User


def test_user(client, app):
    data = {"username": "Stoyanov", "password": "Tt227588!"}
    response = client.post("/user", json=data)
    assert response.json == {"message": "User created successfully"}

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().username == "Stoyanov"


def test_user_login(client, app):
    data_reg = {"username": "Stoyanov", "password": "tesTpass!"}
    data_log = {"username": "Stoyanov", "password": "tesTpass!"}

    response_reg = client.post("/user", json=data_reg)
    response = client.post("/user/login", json=data_log)

    with app.app_context():
        assert User.query.first().username == "Stoyanov"
        assert User.query.first().password == "tesTpass!"
        assert response.status_code == 201

    assert response_reg.json == {"message": "User created successfully"}
