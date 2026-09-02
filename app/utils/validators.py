import re

def validate_password_strength(password: str) -> str:

    if len(password) < 8:
        raise ValueError("Password length should be at least 8 characters")

    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least 1 uppercase letter")

    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least 1 lowercase letter")

    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least 1 number")

    if not re.search(r"[!@#$%^&*]", password):
        raise ValueError("Password must contain at least 1 special character")

    return password