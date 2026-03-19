from src.cftools.client.utils import (
    url_builder
)

def test_cftools_url_builder():
    """
    Test url_builder by supplying a dict of parameters and base_url
    """
    assert url_builder('https://fluid-dev.nccs.nasa.gov/cf/api/fcast', {'products': 'NO2', 'lat': '45.2', 'lon': '-85'}) == 'https://fluid-dev.nccs.nasa.gov/cf/api/fcast/?products=NO2&lat=45.2&lon=-85'