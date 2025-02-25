import os

def get_cftools_path() -> str:
    return os.path.dirname(os.path.split(__file__)[0])