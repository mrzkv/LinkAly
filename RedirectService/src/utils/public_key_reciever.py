import httpx


def get_public_key(url: str) -> str:
    """
    Function to get public key from auth-service

    :param url:
    :return: public_key
    """
    with httpx.Client() as client:
        response = client.get(url=url)
        return response.json()["public_key"]
