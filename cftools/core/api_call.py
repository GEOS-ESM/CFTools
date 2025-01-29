import pandas as pd

from cftools.client.utils import (
    url_builder
)
from cftools.client.access import (
    query_api
)
from cftools.common.utils import (
    to_dict,
    to_dataframe
)

class ApiCall():
    def __init__(self, service=''):
        if service == 'cfapi':
            self.base_url = self.cfapi_root()

        self.to_dataframe = to_dataframe
    
    def cfapi_root(self):
        root_url = 'https://fluid.nccs.nasa.gov/cfapi'

        return root_url

    def get_fcst(self, collection: str='chm_v1', product: str='NO2', lat: int | str=38.0, lon: int | str=-77.0, return_as: str='dict'):
        self.collection = collection
        if 'met' in collection:
            product = 'met'
        self.product = product.upper()
        self.lat = str(lat)
        self.lon = str(lon)

        self.dataset = collection.split('_')[0]
        self.level = collection.split('_')[1]
        self.base_url += '/fcast'
        params = [self.dataset,
                  self.level,
                  self.product,
                  (self.lat + 'x' + self.lon)
                  ]
        out_data = self.get_response(params, return_as)

        return out_data
    
    def get_rpl(self, collection: str='chm_v1', product: str='NO2', lat: int | str=38.0, lon: int | str=-77.0, start_date='latest', end_date='', return_as: str='dict'):
        self.collection = collection
        self.product = product.upper()
        self.lat = str(lat)
        self.lon = str(lon)

        self.dataset = collection.split('_')[0]
        self.level = collection.split('_')[1]
        self.start_date = start_date
        self.end_date = end_date
        self.base_url += '/assim'
        params = [self.dataset,
                  self.level,
                  self.product,
                  (self.lat + 'x' + self.lon),
                  self.start_date,
                  self.end_date
                  ]
        
        out_data = self.get_response(params, return_as)

        return out_data
        
    
    def get_response(self, params, return_as):
        req_url = url_builder(self.base_url, params)
        api_response = query_api(req_url)
        if return_as == 'dict':
            out_data = to_dict(api_response)
        elif return_as == 'dataframe':
            out_data = to_dataframe(api_response)

        return out_data
    
    