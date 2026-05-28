

# TC-CAT-01 -- Unautenticated user cannot list categories
# Expected: 401 Unauthorized
def test_read_categories_without_token(client):
    response = client.get("/categories/")
    assert response.status_code == 401

# TC-CAT-02 -- Authenticated user can create category
# Expected : 201 Createdrespo nse has id , name user_id ,name == "study"
def test_create_category(client):
    username = "category_user_1"
    email = "category_user_1@example.com"
    password = "Testing12345@"

    # 1. Register user
    register_response = client.post(
        "/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    print(register_response.json())
    assert register_response.status_code == 200

    user_data = register_response.json()
    assert user_data["username"] == username
    assert user_data["email"] == email
    assert "id" in user_data

    # 2. Login user
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # 3. Create auth header
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # 4. Create category
    category_response = client.post(
        "/categories/",
        headers=headers,
        json={"name": "category1"},
    )

    assert category_response.status_code == 201

    data = category_response.json()
    assert data["name"] == "category1"
    assert "id" in data
    assert "user_id" in data


# TC - CAT-03 -- Duplicate category name rejected 
# Expected : 409 Conflict 

# def test_duplicate_category_name_is_rejected():
#     return