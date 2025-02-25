from src.cftools.common.configuration import (
    collection_prod_list
)

def test_collection_prod_list():
    data = collection_prod_list('chm_v1')

    assert data['chm_v1'][0] == 'no2'