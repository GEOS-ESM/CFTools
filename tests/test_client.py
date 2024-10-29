from cftools.client import get_api_response

def test_get_fcast():
    api_call = get_api_response('https://fluid.nccs.nasa.gov/cfapi/')
    assert list(api_call.keys()) == ['Forecast and Replay Model Fields', 'Historical AQC Data Sets']