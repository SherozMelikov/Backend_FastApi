from app.core.security import (
    hash_password, verify_password, create_access_token , decode_access_token
)

def test_hash_password_does_not_store_plain_password():
    plain_password = "secret123"

    hashed_password = hash_password(plain_password)

    assert hashed_password != plain_password


def test_verify_password_with_correct_password():
    plain_password = "secret123"

    hashed_password = hash_password(plain_password )
    assert verify_password (plain_password, hashed_password) is True


def test_verify_password_with_wrong_password():

    plain_password = "secret123"


    hashed_password = hash_password(plain_password)

    assert verify_password("wrong-password", hashed_password) is False 



def  test_create_and_decode_access_token():
    token = create_access_token({"sub": "testuser"})
    payload = decode_access_token(token)

    assert payload["sub"] == "testuser"
    assert "exp" in payload