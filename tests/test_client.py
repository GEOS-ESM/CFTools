from src.cftools.client.utils import (
    url_builder
)

def test_cftools_url_builder():
    """
    Test url_builder by supplying a list of dummy parameters and base_url
    """
    assert url_builder('https://fluid.nccs.nasa.gov/cfapi/', ['test','test','123']) == 'https://fluid.nccs.nasa.gov/cfapi/test/test/123'