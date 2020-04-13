""" these should eventually go into network/utils
but are here now for ease.
"""
from functools import reduce  # forward compatibility for Python 3
import operator


def get_from_dict(data_dict, keypath):
    """ get from dictionary
    """
    map_list = keypath.split('.')
    try:
        return reduce(operator.getitem, map_list, data_dict)
    except KeyError:
        return None


def compare_partial_dict(want, have, compare_keys):
    """ compare
    """
    rmkeys = [ckey[1:] for ckey in compare_keys if ckey.startswith('!')]
    kkeys = [ckey for ckey in compare_keys if not ckey.startswith('!')]

    wantd = {}
    for key, val in want.items():
        if key not in rmkeys or key in kkeys:
            wantd[key] = val

    haved = {}
    for key, val in have.items():
        if key not in rmkeys or key in kkeys:
            haved[key] = val

    return wantd == haved
