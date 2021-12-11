from flask.testing import FlaskClient
from unittest.mock import ANY


def test_feed_functional(client: FlaskClient) -> None:
    # 1. Create 1st user
    test_login1 = "TestUser1"
    test_password = "hiadihdai"
    client.post(
        "/api/user",
        json={"login": test_login1, "password": test_password},
    )

    # 2. Create 2nd user
    test_login2 = "TestUser2"
    client.post(
        "/api/user",
        json={"login": test_login2, "password": test_password},
    )

    # 3. Check no posts in feed for 1st user
    response = client.get("api/posts", auth=(test_login1, test_password))
    assert response.status_code == 200
    assert response.json == []

    # 4. Create a post for user 2
    response = client.post(
        "/api/posts",
        json={
            "image": "http://example.com/images/1.png",
            "description": "It was such a great holiday!",
        },
        auth=(test_login2, test_password),
    )

    # 5. Check no posts in feed for 1st user
    response = client.get("api/posts", auth=(test_login1, test_password))
    assert response.status_code == 200
    assert response.json == []

    # 6. Follow user 2 for user 1
    client.post(
        f"/api/user/{test_login2}/follow",
        auth=(
            test_login1,
            test_password,
        ),
    )

    # 7. Check user 2's post in user 1's feed
    response = client.get("api/posts", auth=(test_login1, test_password))
    assert response.status_code == 200
    assert response.json == [ANY]
