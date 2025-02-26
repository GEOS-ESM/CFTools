import yaml

from cftools.util import get_cftools_path

def collection_prod_list(collection: str):
    """
    Retrieve the list of products available for a given collection.

    Args:
        collection (str): A collection ID given as <grp>_<vL>, i.e. chm_p23 or met_x1
    """
    cftools_path = get_cftools_path()
    with open((cftools_path + '/config/parameter_options.yml'), 'r') as f:
        data = yaml.safe_load(f)
    prod_list = data[collection] # Future plan is to let users retrieve this prod list
    return data