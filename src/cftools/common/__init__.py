import pandas as pd

def to_dataframe(cf_data):
    cf_dict = {}
    cf_dict['time'] = cf_data['time']
    cf_dict.update(cf_data['values'])
    # Create a simple dataframe from cfapi dictionary
    df = pd.DataFrame(data=cf_dict)
    # Convert the time column from strings to datetimes
    df['time'] = pd.to_datetime(df['time'])
    return df

def data_cleaner(cf_data):
    output_data = {}
    if isinstance(cf_data, list):
        for i in len(cf_data):
            output_data['schema'+str(i)] = cf_data[i]['schema']
            if 'time' not in output_data.keys():
                output_data.update(cf_data[0]['time'])
            else:
                pass
            output_data.update(cf_data[i]['values'])
    else:
        output_data = cf_data
    return output_data