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
from cftools.core.plotting import (
    plume_rose,
    vertical_profile
)

class ApiCall():
    def __init__(self, service='cfapi'):
        if service == 'cfapi':
            self.base_url = self.cfapi_root()
        self.start_date = None
        self.end_date = None
        self.params=[]
        self.data = None

    def cfapi_root(self):
        root_url = 'https://fluid.nccs.nasa.gov/cfapi'

        return root_url

    def get_data(self, return_as: str='dict'):
        params = self.params
        out_data = self.get_response(params, return_as)

        return out_data

    def get_response(self, params, return_as: str='dict'):
        req_url = url_builder(self.base_url, params)
        api_response = query_api(req_url)
        if return_as == 'dict':
            out_data = to_dict(api_response)
        elif return_as == 'dataframe':
            out_data = to_dataframe(api_response)

        return out_data
    
    def vertical_profile(self):
        data = self.get_data()
        fig = vertical_profile(self.product, data)

        return fig


class CfFcst(ApiCall):
    def __init__(self, collection: str, product: str, lat: int | str, lon: int | str):
        super().__init__()
        self.collection = collection
        self.product = product
        self.lat = str(lat)
        self.lon = str(lon)

        self.dataset = self.collection.split('_')[0]
        self.level = self.collection.split('_')[1]

        if 'met' in self.collection:
            self.product = 'met'
        self.product = self.product.upper()

        self.params = ['fcast',
                  self.dataset,
                  self.level,
                  self.product,
                  (self.lat + 'x' + self.lon)
                  ]

class CfRpl(ApiCall):
    def __init__(self, collection: str, product: str, lat: int | str, lon: int | str, start_date: str, end_date: str):
        super().__init__()
        self.collection = collection
        self.product = product
        self.lat = str(lat)
        self.lon = str(lon)
        self.start_date = start_date
        self.end_date = end_date

        self.dataset = self.collection.split('_')[0]
        self.level = self.collection.split('_')[1]

        if 'met' in self.collection:
            self.product = 'met'
        self.product = self.product.upper()

        self.params = ['assim',
                  self.dataset,
                  self.level,
                  self.product,
                  (self.lat + 'x' + self.lon),
                  self.start_date,
                  self.end_date
                  ]

    def plume_rose(self, grid_res=0.1, show_bounds=True):
        chm_data = self.get_data()
        self.params[1] = 'met'
        self.params[2] = 'x1'
        self.params[3] = 'MET'
        met_data = self.get_data()
        fig = plume_rose(chm_data, met_data, self.product,
                   self.lat, self.lon,
                   self.start_date, self.end_date,
                   grid_res=grid_res, show_bounds=show_bounds)

        return fig

    
    