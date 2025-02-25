from src.cftools.client.utils import (
    url_builder
)

def test_cftools_url_builder():
    assert url_builder('https://fluid.nccs.nasa.gov/cfapi/', ['test','test','123']) == 'https://fluid.nccs.nasa.gov/cfapi/test/test/123'