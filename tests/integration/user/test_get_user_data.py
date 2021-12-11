from flask.testing import FlaskClient
from sqlite3 import Connection


def test_get_user_data(client: FlaskClient) -> None:
    test_login = "TestUser"
    client.post(
        "/api/user",
        json={"login": test_login, "password": "hiadihdai"},
    )
    response = client.get(f"/api/user/{test_login}")
    assert response.status_code == 200, response.data


def test_no_such_user(client: FlaskClient) -> None:
    test_login = "capslock"
    response = client.get(f"/api/user/{test_login}")
    assert response.status_code == 404, response.data
