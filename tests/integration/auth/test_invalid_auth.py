from flask.testing import FlaskClient


def test_invalid_password(client: FlaskClient) -> None:
    test_login = "test_name"
    test_password = "password"
    client.post(
        "/api/user",
        json={"login": test_login, "password": test_password},
    )

    response = client.post(
        "/api/posts",
        json={
            "image": "http://example.com/images/1.png",
            "description": "It was such a great holiday!",
        },
        auth=(test_login, "invalid"),
    )

    assert response.status_code == 401, response.data


def test_no_auth_headers(client: FlaskClient) -> None:
    test_login = "test_name"
    test_password = "password"
    client.post(
        "/api/user",
        json={"login": test_login, "password": test_password},
    )

    response = client.post(
        "/api/posts",
        json={
            "image": "http://example.com/images/1.png",
            "description": "It was such a great holiday!",
        },
    )

    assert response.status_code == 401, response.data


def test_no_such_user(client: FlaskClient) -> None:
    test_login = "test_name"
    test_password = "password"
    client.post(
        "/api/user",
        json={"login": test_login, "password": test_password},
    )

    response = client.post(
        "/api/posts",
        json={
            "image": "http://example.com/images/1.png",
            "description": "It was such a great holiday!",
        },
        auth=("invalid", test_password),
    )

    assert response.status_code == 401, response.data
