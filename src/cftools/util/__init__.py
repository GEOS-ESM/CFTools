import os

def get_cftools_path() -> str:
    """
    Return the install path of cftools

    Returns:
        cftools_path (str): Installation location of cftools
    """
    cftools_path = os.path.dirname(os.path.split(__file__)[0])

    return cftools_path