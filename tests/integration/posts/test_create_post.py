from flask.testing import FlaskClient


def test_create_post(client: FlaskClient) -> None:
    test_login = "TestUser"
    test_password = "hiadihdai"
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
        auth=(test_login, test_password),
    )
    assert response.status_code == 201, response.data


def test_create_post_validation_error(client: FlaskClient) -> None:
    test_login = "TestUser"
    test_password = "hiadihdai"
    client.post(
        "/api/user",
        json={"login": test_login, "password": test_password},
    )

    response = client.post(
        "/api/posts",
        json={
            "description": "It was such a great holiday!",
        },
        auth=(test_login, test_password),
    )
    assert response.status_code == 422, response.data
