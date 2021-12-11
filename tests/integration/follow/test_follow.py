from flask.testing import FlaskClient


def test_follow_normal(client: FlaskClient) -> None:
    test_login = "TestUser"
    test_password = "hiadihdai"
    client.post(
        "/api/user",
        json={"login": test_login, "password": test_password},
    )
    client.post(
        "/api/user",
        json={"login": f"{test_login}1", "password": f"{test_password}1"},
    )
    response = client.post(
        f"/api/user/{test_login}1/follow",
        auth=(
            test_login,
            test_password,
        ),
    )
    assert response.status_code == 200, response.data


def test_follow_self(client: FlaskClient) -> None:
    test_login = "TestUser"
    test_password = "hiadihdai"
    client.post(
        "/api/user",
        json={"login": test_login, "password": test_password},
    )

    response = client.post(
        f"/api/user/{test_login}/follow",
        auth=(
            test_login,
            test_password,
        ),
    )
    assert response.status_code == 403, response.data


def test_follow_twice(client: FlaskClient) -> None:
    test_login = "TestUser"
    test_password = "hiadihdai"
    client.post(
        "/api/user",
        json={"login": test_login, "password": test_password},
    )
    client.post(
        "/api/user",
        json={"login": f"{test_login}1", "password": f"{test_password}1"},
    )
    client.post(
        f"/api/user/{test_login}1/follow",
        auth=(
            test_login,
            test_password,
        ),
    )

    response = client.post(
        f"/api/user/{test_login}1/follow",
        auth=(
            test_login,
            test_password,
        ),
    )
    assert response.status_code == 409, response.data
