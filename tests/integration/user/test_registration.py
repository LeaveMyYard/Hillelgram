from flask.testing import FlaskClient
from sqlite3 import Connection


def test_normal_registration(client: FlaskClient, conn: Connection) -> None:
    test_login = "TestUser"
    response = client.post(
        "/api/user",
        json={"login": test_login, "password": "hiadihdai"},
    )
    assert response.status_code == 201, response.data

    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM User WHERE login=?", (test_login,))
        count, *_ = cur.fetchone()
        assert count == 1
    finally:
        cur.close()


def test_registration_already_exists(client: FlaskClient) -> None:
    test_login = "TestUser"
    response = client.post(
        "/api/user",
        json={"login": test_login, "password": "hiadihdai"},
    )
    assert response.status_code == 201, response.data

    response = client.post(
        "/api/user",
        json={"login": test_login, "password": "fajojfoa"},
    )
    assert response.status_code == 409, response.data
