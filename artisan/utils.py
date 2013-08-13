# stdlib
from copy import deepcopy


def merge(a, b):
    """
    Helper method to deep merge to dicts
    """

    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result
