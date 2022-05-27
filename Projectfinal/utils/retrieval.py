import numpy as np


def to_cat(x, arr_cat):
    try:
        ret = np.where(arr_cat[0]==x)[0][0]
    except:
        ret = 0
    return ret