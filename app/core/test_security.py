from security import hash_password, verify_password

plain_password = ""

hashed_password = hash_password(plain_password)

print("Hashed password:", hashed_password)
print("Correct:", verify_password("herminetincture", hashed_password))
print("Wrong:", verify_password("wrongpassword", hashed_password))