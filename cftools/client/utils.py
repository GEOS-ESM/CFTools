from urllib.parse import urljoin

def url_builder(base_url: str, params: list=['']):
    for p in params:
        base_url += '/'
        base_url = urljoin(base_url, p)
    return base_url