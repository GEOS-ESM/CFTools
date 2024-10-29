from src.cftools.cftools import Cfout

def test_Cfout_class():
    api_call = Cfout(service='cfapi')
    assert api_call.cfapi() is None

def test_cfapi_root():
    api_call = Cfout(service='cfapi')
    assert api_call.cfapi_root() == 'https://fluid.nccs.nasa.gov/cfapi/'

def test_get_fcst_dict():
    api_call = Cfout(service='cfapi')
    data = api_call.get_fcst(output_format='dict')
    assert data['schema']['dataset'] == "chm_tavg_1hr_g1440x721_v1"
    assert data['schema']['longname'] == 'Nitrogen dioxide (NO2, MW = 46.00 g mol-1) volume mixing ratio dry air'

def test_get_fcst_dict_multi():
    assert 1 == 1