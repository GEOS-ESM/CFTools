from urllib.parse import urlencode

def url_builder(base_url: str, params: dict) -> str:
    """
    Build a query-string based CF API URL.

    Args:
        base_url (str): Full endpoint URL (e.g. '.../fcast/' or '.../assim/')
        params (dict): Query parameters to append as a query string.

    Returns:
        str: The full URL with query string appended.
    """
    query_string = urlencode(params)
    return f"{base_url.rstrip('/')}/?{query_string}"