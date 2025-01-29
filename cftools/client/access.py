from urllib.request import urlopen

def query_api(url):
    # Query the CFAPI
    response = urlopen(url)

    return response