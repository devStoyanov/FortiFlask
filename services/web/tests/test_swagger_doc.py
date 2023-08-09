import requests

ENDPOINT = "http://localhost:5001/swagger/#/"
HOME_ENDPOINT = "http://localhost:5001"

response = requests.get(ENDPOINT)
print(response)


def test_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_home():
    response = requests.get(HOME_ENDPOINT)
    assert response.status_code == 200
