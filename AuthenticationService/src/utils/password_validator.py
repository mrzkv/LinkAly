import re

def check_password_vulnerability(password: str) -> str:
    """
    requires password with:
    1. at least 8 characters long
    2. at least one uppercase letter
    3. at least one lowercase letter
    4. at least one digit
    5. at least one special character

    :param password:
    :return password:
    :raises: ValueError:
    """

    if len(password) < 8:
        raise ValueError("Password must be at"
                         " least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at"
                         " least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at"
                         " least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at"
                         " least one digit")
    if not re.search(r'[!@#$%^&*(),.?"\':{}_+|<>/\\]', password):
        raise ValueError("Password must contain at"
                         " least one special character")

    return password
