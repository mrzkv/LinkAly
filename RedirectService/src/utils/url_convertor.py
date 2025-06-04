
def url_convertor(url: str) -> str:
    """
    Deletes http:// or https:// from the given url
    >>> 'http://mrzkv.exmaple.com                     '
    'mrkzv.exmaple.com'
    >>> '         https://github.com/mrzkv'
    'github.com/mrzkv'
    """

    # removing spaces
    url = url.strip()
    # removing http(-s)://
    if url.startswith("http://"):
        url = url.replace("http://", "", 1)
    elif url.startswith("https://"):
        url = url.replace("https://", "", 1)

    return url

