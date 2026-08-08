import pytest


def register_user(
    client,
    username="testuser",
    email="testuser@example.com",
    password="password123",
):
    response = client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    return response.json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_calculation(client):
    token = register_user(client)

    response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15
    assert isinstance(data["user_id"], int)
    assert data["user_id"] > 0
    assert "id" in data


def test_browse_calculations(client):
    token = register_user(client)

    client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
        },
    )

    client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 8,
            "b": 2,
            "type": "Divide",
        },
    )

    response = client.get(
        "/calculations",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["result"] == 15
    assert data[1]["result"] == 4


def test_read_calculation(client):
    token = register_user(client)

    create_response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 20,
            "b": 4,
            "type": "Divide",
        },
    )

    calculation_id = create_response.json()["id"]

    response = client.get(
        f"/calculations/{calculation_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == calculation_id
    assert data["a"] == 20
    assert data["b"] == 4
    assert data["type"] == "Divide"
    assert data["result"] == 5


def test_update_calculation(client):
    token = register_user(client)

    create_response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
        },
    )

    calculation_id = create_response.json()["id"]

    response = client.put(
        f"/calculations/{calculation_id}",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 5,
            "type": "Multiply",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == calculation_id
    assert data["type"] == "Multiply"
    assert data["result"] == 50


def test_delete_calculation(client):
    token = register_user(client)

    create_response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 9,
            "b": 3,
            "type": "Sub",
        },
    )

    calculation_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/calculations/{calculation_id}",
        headers=auth_headers(token),
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/calculations/{calculation_id}",
        headers=auth_headers(token),
    )

    assert get_response.status_code == 404
    assert (
        get_response.json()["detail"]
        == "Calculation not found."
    )


def test_create_division_by_zero(client):
    token = register_user(client)

    response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 0,
            "type": "Divide",
        },
    )

    assert response.status_code == 422


def test_create_invalid_calculation_type(client):
    token = register_user(client)

    response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 5,
            "type": "SquareRoot",
        },
    )

    assert response.status_code == 422


def test_read_missing_calculation(client):
    token = register_user(client)

    response = client.get(
        "/calculations/99999",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Calculation not found."
    )


def test_update_missing_calculation(client):
    token = register_user(client)

    response = client.put(
        "/calculations/99999",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
        },
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Calculation not found."
    )


def test_delete_missing_calculation(client):
    token = register_user(client)

    response = client.delete(
        "/calculations/99999",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Calculation not found."
    )


def test_unauthorized_access(client):
    response = client.get("/calculations")

    assert response.status_code == 401


def test_user_cannot_access_another_users_calculation(client):
    first_token = register_user(
        client,
        username="firstuser",
        email="first@example.com",
    )

    second_token = register_user(
        client,
        username="seconduser",
        email="second@example.com",
    )

    create_response = client.post(
        "/calculations",
        headers=auth_headers(first_token),
        json={
            "a": 6,
            "b": 2,
            "type": "Multiply",
        },
    )

    calculation_id = create_response.json()["id"]

    response = client.get(
        f"/calculations/{calculation_id}",
        headers=auth_headers(second_token),
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "method,path",
    [
        ("get", "/calculations"),
        ("get", "/calculations/1"),
        ("delete", "/calculations/1"),
    ],
)
def test_invalid_token(client, method, path):
    response = getattr(client, method)(
        path,
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_create_power_calculation(client):
    token = register_user(client)

    response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 2,
            "b": 3,
            "type": "Power",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["a"] == 2
    assert data["b"] == 3
    assert data["type"] == "Power"
    assert data["result"] == 8


def test_create_modulus_calculation(client):
    token = register_user(client)

    response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 3,
            "type": "Modulus",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["a"] == 10
    assert data["b"] == 3
    assert data["type"] == "Modulus"
    assert data["result"] == 1


def test_create_modulus_by_zero(client):
    token = register_user(client)

    response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={
            "a": 10,
            "b": 0,
            "type": "Modulus",
        },
    )

    assert response.status_code == 422


def test_power_calculation_saved_in_history(client):
    token = register_user(client)
    headers = auth_headers(token)

    create_response = client.post(
        "/calculations",
        headers=headers,
        json={
            "a": 3,
            "b": 4,
            "type": "Power",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/calculations",
        headers=headers,
    )

    assert response.status_code == 200

    calculations = response.json()

    assert any(
        calculation["type"] == "Power"
        and calculation["result"] == 81
        for calculation in calculations
    )


def test_modulus_calculation_saved_in_history(client):
    token = register_user(client)
    headers = auth_headers(token)

    create_response = client.post(
        "/calculations",
        headers=headers,
        json={
            "a": 20,
            "b": 6,
            "type": "Modulus",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/calculations",
        headers=headers,
    )

    assert response.status_code == 200

    calculations = response.json()

    assert any(
        calculation["type"] == "Modulus"
        and calculation["result"] == 2
        for calculation in calculations
    )