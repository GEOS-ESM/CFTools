def level_parser(level, product):
    params_dict = {}
    level_dict = {
        'sfc': {
            'chm': 'v1',
            'met': 'x1'
            }, 
        'xsec': {
            'chm': 'p23',
            'met':'p23'
            }
        }
    if isinstance(product, list):
        pass
    else:
        product = [product]
    for p in product:
        params_dict[p] = {}
        if p == 'MET':
            dataset = 'met'
        else:
            dataset = 'chm'
        params_dict[p]['dataset'] = dataset
        params_dict[p]['model_level'] = level_dict[level][dataset]

    return params_dict

def url_builder(base_url: str, collection: str, params: dict):
    request_url_list = [base_url]
    for param in args:
        tmp_url_list = []
        if isinstance(param, list):
            i = 0
            for p in param:
                for url in request_url_list:
                    tmp_url_list.insert(i, url+p+'/')
                    i += 1
        else:
            for i, url in enumerate(request_url_list):
                tmp_url_list.insert(i, url+param+'/')
        request_url_list = tmp_url_list

    if len(request_url_list) == 1:
        return request_url_list[0]
    else:
        return request_url_list