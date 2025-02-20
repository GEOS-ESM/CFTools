import json
import pandas as pd

def to_dict(response):
    # Load the data as a dictionary 
    data = json.loads(response.read())

    return data

def to_dataframe(response):
        cf_dict = {}
        cf_data = to_dict(response)
        cf_dict['time'] = cf_data['time']
        product_idx = 0
        product = cf_data['schema']['product'][product_idx]
        level = cf_data['schema']['lev']
        LEVEL_SWITCH = '23'
        
        if level == LEVEL_SWITCH:
            cf_dict.update({'product': [product]*len(cf_data['time'])})
            cf_dict.update(cf_data['values'][product])
        else:
            cf_dict.update(cf_data['values'])

        # Create a simple dataframe from cfapi dictionary
        df = pd.DataFrame(data=cf_dict)
        # Convert the time column from strings to datetimes
        df['time'] = pd.to_datetime(df['time'])
        return df