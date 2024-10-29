import json

from urllib.request import urlopen

def get_api_response(url):
    if isinstance(url, list):
        data = []
        for u in url:
            data.append(query_api(u))
    else:
        data = query_api(url)

    return data

def query_api(url):
    # Query the CFAPI
    response = urlopen(url)
    # Load the data as a dictionary 
    data = json.loads(response.read())

    return data
    