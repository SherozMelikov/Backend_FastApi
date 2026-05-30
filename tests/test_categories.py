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


# TC-CAT-05--Authenticated user can get category by id     
# Expected: 200 
#         
def test_get_category_by_id(client):
    # Declared glocal variable to avoid repetition
    username = "category_user_4"
    email = "category_user_2312q@gmail.com"
    password = "Testing_1234@"

    # Mitigated user registration using global variable
    register_response = client.post(
        "/users/",
        json={
            "username": username,
            "email": email,
            "password": password,

        },
    )
    # Checked wheather it returned 200 ok
    assert register_response.status_code == 200

    # Mitigated user authentication using global variable
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },

    )
    # Checked is it correct or not 
    assert login_response.status_code == 200

    # Extracted token from json body response 
    token = login_response.json()["access_token"]

    # Token added  in headers 
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Header with authenticated header  using  in category_creeate 
    category_create = client.post(
        "/categories/",
        headers=headers,
        json={"name": "Study"},

    )

    # Make sure that it is returned 201
    assert category_create.status_code == 201

    # Extracter category id from json through parsing json arrray into python dictionary
    created_category_id = category_create.json()["id"]


    # Extracted category id is being used in get_category plus   with headers 
    get_category_response = client.get(
        f"/categories/{created_category_id}",
        headers=headers

    )
    # Checked that it returned  200 ok
    assert get_category_response.status_code == 200
    # Saved returned json body into  a varible that is converted python readable dictionary
    category_data = get_category_response.json()

    # Checked  that extracted category id is == to the original returned id 
    assert category_data["id"] == created_category_id

    # Checked that  name matches with the returned actual category name 
    assert category_data["name"] == "Study"


# TC-CAT-06-- Unknown category returns 404
# Expected : 404 Not Found 

def test_get_category_with_unknown_id(client):
    username = "category_user_6"
    email = "category_user_2312@gmail.com"
    password = "Testing_1234@"

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
        "/auth/login",
        data={
            "username": username,
            "password": password,
        }
    )

    assert login_response.status_code == 200



    token = login_response.json()["access_token"]

    header = {
        "Authorization": f"Bearer {token}",
    }

    unknown_category_id = 9999999

    get_category_response = client.get(
        f"/categories/{unknown_category_id}",
        headers=header
    )
   
    assert get_category_response.status_code == 404
    data =  get_category_response.json()
    assert "detail" in data
    assert data["detail"] == "Category not found"




#TC-CAT-7 -- Authenticated user can update own category
#Expected : 200 OK

def test_update_category(client):
    username = "category_user_7"
    email = "category_user_231@gmail.com"
    password = "Testing_1234@"

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
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },

    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    header = {
        "Authorization": f"Bearer {token}"
    }

    category_create_request = client.post(
        "/categories/",
        headers=header,
        json={
            "name": "Study",
        }
    )

    assert  category_create_request.status_code == 201

    category_id = category_create_request.json()["id"]

    update_category_request = client.put(
        f"/categories/{category_id}",
        headers=header,
        json={"name": "University"}
    )

    assert update_category_request.status_code == 200

    updated_data = update_category_request.json()

    assert updated_data["id"] == category_id
    assert updated_data["name"] == "University"


#TC-CAT-08 -- Updating to duplicate name rejected 
#Expected : 409 Conflict 


def test_update_category_rejected(client):
    username = "category_user_8"
    email = "category_user_231@gmail.com"
    password = "Testing_2312@"

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
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },

    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    header = {
        "Authorization": f"Bearer {token}"
    }

    study_category_create_request = client.post(
        "/categories/",
        headers=header,
        json={
            "name": "Study",
        }
    )
    assert study_category_create_request.status_code == 201

    work_category_create_request = client.post(
        "/categories/",
        headers=header,
        json = {
            "name": "Work",
        }
    )
    assert work_category_create_request.status_code == 201 

    work_id = work_category_create_request.json()["id"]

    update_work_request = client.put(
        f"/categories/{work_id}",
        headers= header,
        json = {
            "name": "Study",
        }
    )
    assert update_work_request.status_code == 409

    updated_data = update_work_request.json()

    assert "detail" in updated_data
    assert updated_data["detail"] == "Category already exists"
    


#TC-CAT-09 -- Authenticated user can delete own category
#Expected: 204 No Content
def test_delete_category(client):
    username = "category_user_9"
    email = "category_user_231da@gmail.com"
    password = "Testing_2312@"

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
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },

    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    study_category_create_request = client.post(
        "/categories/",
        headers=headers,
        json={
            "name": "Study",
        }
    )
    assert study_category_create_request.status_code == 201

    category_id = study_category_create_request.json()["id"]

    delete_study_request = client.delete(
        f"/categories/{category_id}",
        headers=headers
    )
    assert delete_study_request.status_code == 204 


    #TC-CAT -- Deleted categopry no londer exists
    #Expected : 404
    
    get_deleted_study_cat = client.get(
        f"/categories/{category_id}",
        headers=headers
    )
    assert get_deleted_study_cat.status_code == 404





 


    
   




