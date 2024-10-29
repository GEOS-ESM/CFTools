import cftools.client as client
import cftools.common as common
import cftools.core as core

class Cfout:
    def __init__(self, service=''):
        if service == 'cfapi':
            self.cfapi()
    
    def cfapi(self):
        self.base_url = 'https://fluid.nccs.nasa.gov/cfapi/'

        return
    
    def cfapi_root(self):
        root_url = core.url_builder(self.base_url)
        return root_url
    
    def available_parameters():
        return

    def get_fcst(self, output_format: str='dict', level: str='sfc', product: str | list='NO2', lat: int | str=38.0, lon: int | str=-77.0):
        if isinstance(product, list):
            self.product = [p.upper() for p in product]
        else:
            self.product = product.upper() # look at enum type (in video)
        self.params_dict = core.level_parser(level, self.product)
        self.params_dict['coord_string'] = str(lat) + 'x' + str(lon)

        print(self.params_dict)

        req_url = core.url_builder(self.base_url, 'fcast', self.params_dict)
        print(req_url)
        fcst_response = client.get_api_response(req_url)

        fcst_dict = common.data_cleaner(fcst_response)

        if output_format == 'dict':
            fcst_data = fcst_dict
        elif output_format == 'dataframe':
            fcst_data = common.to_dataframe(fcst_dict)

        return fcst_data
