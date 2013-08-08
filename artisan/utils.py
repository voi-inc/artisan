# stdlib
from copy import deepcopy


#
# Helper method to deep merge to dicts
#
def merge(a, b):
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result