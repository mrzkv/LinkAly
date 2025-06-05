import requests


def get_public_key(url: str, default: str) -> str:
    """
    Function to get public key from auth-service

    :param default: Return default public key if cant get key from auth-service
    :param url: Url to endpoint with public key ( JWKS )
    :return: public_key
    """
    try:
        response = requests.get(url, timeout=20)
        return response.json()["public_key"]

    except Exception:
        return default
