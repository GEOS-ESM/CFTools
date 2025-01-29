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
        product = cf_data['schema']['product']
        MIN_PARAMS=1
        if len(product) > MIN_PARAMS:
            #for p in product:
            cf_dict.update(cf_data['values'])
            #cf_dict.update({'product': [p]*len(cf_data['time'])})
        else:
            cf_dict.update(cf_data['values'])

        # Create a simple dataframe from cfapi dictionary
        df = pd.DataFrame(data=cf_dict)
        # Convert the time column from strings to datetimes
        df['time'] = pd.to_datetime(df['time'])
        return df