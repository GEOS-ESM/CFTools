import json
import pandas as pd

def to_dict(response):
    """
    Use CFAPI response to read and return dictionary

    Args:
        response (http.client.HTTPResponse): API response to be read

    Returns:
        data (dict): Dictionary from loaded API JSON response
    """
    data = json.loads(response.read())

    return data

def to_dataframe(response):
    """
    Use CFAPI response to read and return as dataframe

    Args:
        response (http.client.HTTPResponse): API response to be read

    Returns:
        df (pandas.core.frame.DataFrame): Dataframe created from the dictionary
        returned from the API
    """
    # Create an empty dictionary, cf_dict
    cf_dict = {}
    # Get the API response into a new dictionary, cf_data
    cf_data = to_dict(response)
    # Add a time key to cf_dict from cf_data
    cf_dict['time'] = cf_data['time']
    # Select the product name from the schema
    product_idx = 0 # Index required because product is provided as list in schema
    product = cf_data['schema']['product'][product_idx]
    # Get vertical resolution from schema
    vL = cf_data['schema']['lev']
    # Create a switch for vertical resolution
    VL_SWITCH = '23'
    
    # Use switch to check vertical resoluion
    if vL == VL_SWITCH:
        # Create a column for product in the case of p23 vL
        cf_dict.update({'product': [product]*len(cf_data['time'])})
        cf_dict.update(cf_data['values'][product])
    else:
        # Add a dictionary with the product key and values to cf_dict
        cf_dict.update(cf_data['values'])

    # Create a simple dataframe from cf_dict
    df = pd.DataFrame(data=cf_dict)
    # Convert the time column from strings to pandas datetimes
    df['time'] = pd.to_datetime(df['time'])
    
    return df