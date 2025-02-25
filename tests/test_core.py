from cftools.core.api_call import (
    ApiCall,
    CfFcst
)

def test_cfapi_root():
    api_call = ApiCall(service='cfapi')
    assert api_call.cfapi_root() == 'https://fluid.nccs.nasa.gov/cfapi'

def test_get_fcst_dict():
    call = CfFcst(collection='chm_v1', product='no2', lat = 45.2, lon=-85)
    data = call.get_data(return_as='dict')
    assert data['schema']['dataset'] == "chm_tavg_1hr_g1440x721_v1"
    assert data['schema']['longname'] == 'Nitrogen dioxide (NO2, MW = 46.00 g mol-1) volume mixing ratio dry air'

def test_get_xsec_fcst_dict():
    call = CfFcst(collection='chm_p23', product='no2', lat = 45.2, lon=-85)
    data = call.get_data(return_as='dict')
    assert data['schema']['dataset'] == 'chm_inst_1hr_g1440x721_p23'

def test_get_sfc_fcst_df():
    call = CfFcst(collection='chm_v1', product='no2', lat = 45.2, lon=-85)
    data = call.get_data(return_as='dataframe')
    assert data is not None