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

def test_duplicate_category_name_is_rejected(client):
    # Predefined variables for  user , to avoid repetions while chekcing 
    username = "category_user_2"
    email = "category_user_2@gmail.com"
    password = "Testing6789@"

    # Usder Registration  with the predefined 
    register_response = client.post(
        "/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
            
        },
    )
    assert register_response.status_code == 200

    user_data = register_response.json()
    assert user_data["username"] == username 
    assert user_data ["email"] == email
    assert "id" in user_data

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password" : password,

        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # First  Category = Study creation
    first_category_response = client.post(
        "/categories/",
        headers = headers,
        json={"name": "Study"},
    )
    assert first_category_response.status_code == 201

    data = first_category_response.json()
    assert data["name"] == "Study"
    assert "id" in data
    assert "user_id" in data


    # Second Category = Study creation

    second_category_response = client.post(
        "/categories/",
        headers=headers,
        json={"name": "Study"},
    )
    
    assert second_category_response.status_code == 409
    error_data =  second_category_response.json()
    expected_detail = "Category already exists"
    assert "detail" in error_data
    assert  error_data["detail"] == expected_detail

# TC-CAT-04 -- Authenticated user can list own categories 
# Expected : 200
def test_get_categories_for_authenticvated_user(client):
    username = "category_user_3"
    email = "category_user_123@gmail.com"
    password = "Testing4_1234@"


    register_response = client.post(
        "/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "auth/login",
        data={
            "username": username,
            "password": password
            
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",

    }

    study_category_creation = client.post(
        "/categories/",
        headers=headers,
        json={"name": "Study"},

    )
    assert study_category_creation.status_code == 201

    work_category_creation = client.post(
        "/categories/",
        headers=headers,
        json={"name": "Work"},
    )
    assert work_category_creation.status_code == 201


    categories = client.get(
        "/categories/",
        headers=headers
    )
    assert categories.status_code == 200



    data = categories.json()
    assert isinstance(data,list)


    category_names = []
    for category in data:
        category_names.append(category["name"])

    assert "Study" in category_names
    assert "Work" in category_names
        




    
   




