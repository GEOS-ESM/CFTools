import yaml

from cftools.util import get_cftools_path

def collection_prod_list(collection):
    cftools_path = get_cftools_path()
    with open((cftools_path + '/config/parameter_options.yml'), 'r') as f:
        data = yaml.safe_load(f)
    prod_list = data[collection]
    return data