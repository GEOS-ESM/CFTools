from urllib.request import urlopen

def query_api(url):
    """
    Query the CFAPI

    Args:
        url (str): URL based on requested user parameters

    Returns:
        response (http.client.HTTPResponse): CF API response

    """
    response = urlopen(url)

    return response