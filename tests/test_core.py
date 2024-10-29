from src.cftools.core import url_builder

def test_cftools_url_builder():
    assert url_builder('https://fluid.nccs.nasa.gov/cfapi/', 'test','test','123') == 'https://fluid.nccs.nasa.gov/cfapi/test/test/123/'

def test_cftools_url_builder_multi():
    assert url_builder('https://fluid.nccs.nasa.gov/cfapi/', 'test',['test1', 'test2'], '123') == [
        'https://fluid.nccs.nasa.gov/cfapi/test/test1/123/',
        'https://fluid.nccs.nasa.gov/cfapi/test/test2/123/'
    ]