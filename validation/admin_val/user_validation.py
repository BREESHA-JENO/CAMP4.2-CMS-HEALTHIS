def validate_login(username, password):
    if not username or not isinstance(username, str):
        raise ValueError("Username cannot be empty")
    if not password or not isinstance(password, str):
        raise ValueError("Password cannot be empty")
    return True

print("hello")