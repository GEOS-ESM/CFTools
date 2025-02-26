from urllib.parse import urljoin

def url_builder(base_url: str, params: list=['']):
    """
    Use the list of parameters to build a CF API URL to be queried.

    Args:
        base_url (str): service base url, selected in cftools.core.api_call
        params (list): list of parameters provided by user

    Returns:
        base_url (str): Updated base_url with selected parameters
    """
    # Iterate over params to build URL
    for p in params:
        base_url += '/'
        base_url = urljoin(base_url, p)

    return base_url