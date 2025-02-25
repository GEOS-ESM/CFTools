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
    """ApiCall class for storing methods shared by forecast and replay calls to the API.

    Methods
    -------
    __init__(self, service='cfapi'):
        Constructor
    cfapi_root(self):
        Get the root URL of the CFAPI.
    get_data(self, return_as: str='dict'):
        Retrieve data from the get_response class method. 
    get_response(self, params, return_as: str='dict'):
        Send a request to the API and process the response.
    vertical_profile(self):
        Call the vertical profile function from core.plotting
    """
    def __init__(self, service='cfapi'):
        """
        Initialize the instance with a base URL based on service. 
        Initialize date range, parameters, and data.

        Args:
            service (str, optional): The service type. Defaults to 'cfapi'. Future versions should
                                    include options for services like GEE.
                                    If 'cfapi', the base URL is set using `cfapi_root()`.

        Attributes:
            base_url (str): The base URL for the selected service.
            start_date (Any)): The start date for data retrieval (default: None).
            end_date (Any): The end date for data retrieval (default: None).
            params (list): A list to store query parameters.
            data (Any): Placeholder for retrieved data (default: None).
        """
        if service == 'cfapi':
            self.base_url = self.cfapi_root()
        self.start_date = None
        self.end_date = None
        self.params=[]
        self.data = None

    def cfapi_root(self):
        """
        Get the root URL of the CFAPI.
        """
        root_url = 'https://fluid.nccs.nasa.gov/cfapi'

        return root_url

    def get_data(self, return_as: str='dict'):
        """
        Retrieve data from the get_response class method.

        Args:
            return_as (str, optional): The format to return the data in. Defaults to 'dict'. 
                                   Option include 'dict' and 'dataframe'.

        Returns:
            out_data: The retrieved data formatted as specified.
        """
        params = self.params
        out_data = self.get_response(params, return_as)

        return out_data

    def get_response(self, params, return_as: str='dict'):
        """
        Send a request to the API and process the response.

        Args:
            params (list): The query parameters for the request. Provided in init.
            return_as (str, optional): The format to return the data in. Defaults to 'dict'. 
                                    Options include 'dict' and 'dataframe'.

        Returns:
            out_data: The API response formatted as specified.
        """
        req_url = url_builder(self.base_url, params)
        api_response = query_api(req_url)
        if return_as == 'dict':
            out_data = to_dict(api_response)
        elif return_as == 'dataframe':
            out_data = to_dataframe(api_response)

        return out_data
    
    def vertical_profile(self):
        """
        Call the vertical profile function from core.plotting

        Returns:
            fig (matplotlib.figure.Figure): The figure produced based on provided parameters.
        """
        data = self.get_data()

        # Call the verical profile function
        fig = vertical_profile(self.product, data)

        return fig


class CfFcst(ApiCall):
    """Child class of ApiCall for querying the API for forecast data

    Methods
    -------
    __init__(self, collection: str, product: str, lat: int | str, lon: int | str):
        Constructor
    """
    def __init__(self, collection: str, product: str, lat: int | str, lon: int | str):
        """
        Initialize the instance with a series of parameters required to query the
        CFAPI.

        Args:
            collection (str): Collection to request from. Possible values are
            chm_v1, chm_p23, chm_v72, met_x1, and met_v72.
            product (str): Chosen product. Possible values are shown for respective
            collections in config/parameter_options.yml
            lat (int, str): Selected latitude.
            lon (int, str): Selected longitude.

        Attributes:
            grp (str): A three-letter mnemonic for the type of fields in the collection.
            Possible values are chm and met.
            vL (str): Vertical resolution. Possible values are v1, x1, p23, and v72.
        """
        super().__init__()
        self.collection = collection
        self.product = product
        self.lat = str(lat)
        self.lon = str(lon)

        self.grp = self.collection.split('_')[0]
        self.vL = self.collection.split('_')[1]

        if 'met' in self.collection:
            self.product = 'met'
        self.product = self.product.upper()

        # Assemble the params list
        self.params = ['fcast',
                  self.grp,
                  self.vL,
                  self.product,
                  (self.lat + 'x' + self.lon)
                  ]

class CfRpl(ApiCall):
    """Child class of ApiCall for querying the API for replay data

    Methods
    -------
    __init__(self, collection: str, product: str, lat: int | str, lon: int | str):
        Constructor
    plume_rose(self, grid_res=0.1, show_bounds=True):
        Create a plume rose figure from core.plotting
    """
    def __init__(self, collection: str, product: str, lat: int | str, lon: int | str, start_date: str, end_date: str):
        """
        Initialize the instance with a series of parameters required to query the
        CFAPI.

        Args:
            collection (str): Collection to request from. Possible values are
            chm_v1, chm_p23, chm_v72, met_x1, and met_v72.
            product (str): Chosen product. Possible values are shown for respective
            collections in config/parameter_options.yml
            lat (int, str): Selected latitude.
            lon (int, str): Selected longitude.
            start_date (str): Start of replay window
            end_date (str): End of replay window

        Attributes:
            grp (str): A three-letter mnemonic for the type of fields in the collection.
            Possible values are chm and met.
            vL (str): Vertical resolution. Possible values are v1, x1, p23, and v72.
        """
        super().__init__()
        self.collection = collection
        self.product = product
        self.lat = str(lat)
        self.lon = str(lon)
        self.start_date = start_date
        self.end_date = end_date

        self.grp = self.collection.split('_')[0]
        self.vL = self.collection.split('_')[1]

        if 'met' in self.collection:
            self.product = 'met'
        self.product = self.product.upper()

        # Assemble the params list
        self.params = ['assim',
                  self.grp,
                  self.vL,
                  self.product,
                  (self.lat + 'x' + self.lon),
                  self.start_date,
                  self.end_date
                  ]

    def plume_rose(self, grid_res=0.1, show_bounds=True):
        """
        Create a plume rose figure from core.plotting

        Args:
            grid_res (float): Grid resolution of the interpolation
            show_bounds (bool): Toggle for the wind speed extents on the plot

        Returns:
            fig (matplotlib.figure.Figure): The figure produced based on provided parameters.
        """
        chm_data = self.get_data()
        self.params[1] = 'met'
        self.params[2] = 'x1'
        self.params[3] = 'MET'
        met_data = self.get_data()

        # Call the plume rose function
        fig = plume_rose(chm_data, met_data, self.product,
                   self.lat, self.lon,
                   self.start_date, self.end_date,
                   grid_res=grid_res, show_bounds=show_bounds)

        return fig

    
    