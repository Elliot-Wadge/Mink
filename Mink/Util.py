import numpy as np
import pandas as pd


def local_max(arr, N=2, strict=False):
    '''find local maximums of an array where local is defined as M points on
    either side, if strict is truethen it will follow this process exactly if
    strict is false it will also count local maxes that are at least
    one space from the edge if they satisfy the requirement within the
    remaining array'''
    local_maxs = []
    M = int(N/2)+1
    # loop through the array
    if not strict:
        i = 1

    else:
        i = M

    indexes = []
    while i < len(arr) - 1:
        iterate = 1
        # flag
        local_max = True
        for j in range(M):
            try:
                # will make index error when your with M of the edges so except
                # index error
                if arr[i] < arr[i + j]:
                    local_max = False
                    iterate = j
                    break

            except IndexError:
                if strict:
                    # reproduce old behaviour
                    local_max = False
                    break
                # other wise search in the other direction
            try:
                if arr[i] < arr[i - j]:
                    local_max = False
                    break

            except IndexError:
                if strict:
                    local_max = False
                    break

        if local_max:
            local_maxs.append(arr[i])
            indexes.append(i)
        i += iterate
    return np.array(local_maxs), np.array(indexes)


def dec_noise(sigma=0):
    '''decorator add gaussian noise to a function with
     standard deviation sigma'''
    def decorator(func):
        def noisy_func(*args, **kwargs):
            modified = func(*args, **kwargs)
            modified += np.random.normal(scale=sigma, size=len(modified))
            return modified
        return noisy_func
    return decorator


def noise(func, sigma=0):
    '''add gaussian noise to func with standard deviation sigma'''
    def noisy_func(*args, **kwargs):
        modified = func(*args, **kwargs)
        modified += np.random.normal(scale=sigma, size=len(modified))
        return modified
    return noisy_func


def error_prop(f, args, errors, ind_var=[None], **kwargs):
    '''take function f, args, and errors in args and propegate the error using the
        method of calculus'''
    errors = np.array(errors)
    # array for storing derivatives
    d_arr = np.ones(len(args))
    prop_arr = []
    for x in ind_var:
        for i, arg in enumerate(args):
            # these are the smallest ratios that still improve in estimate
            lower_ratio = 0.99999999999
            upper_ratio = 1.00000000001
            # take a linspace of area surrounding
            if arg != 0:
                arg_space = np.linspace(lower_ratio*abs(arg),
                                        upper_ratio*abs(arg), 2)
                # reintroduce negative if it was removed
                arg_space *= abs(arg)/arg
            else:
                arg_space = np.linspace(lower_ratio - 1, upper_ratio - 1, 2)

            # call the function with x inserted in correct position
            if x is None:
                y = f(*args[:i], arg_space, *args[i+1:], **kwargs)
            else:
                y = f(x, *args[:i], arg_space, *args[i+1:], **kwargs)
            # get partial derivative of the function with respect to arg
            d_arr[i] = np.gradient(y, arg_space)[0]
        prop_err = np.sqrt(np.sum((d_arr*errors)**2))
        prop_arr.append(prop_err)
    return prop_arr


def csv_to_df(files, *args, **kwargs):
    '''function to load multiple csv files into a dataframe'''
    iterable = hasattr(files, "__iter__")
    df_lst = []
    if iterable and not isinstance(files, str):
        for file in files:
            df_lst.append(pd.read_csv(file, *args, **kwargs))
        df = pd.concat(df_lst)
    else:
        df = pd.read_csv(files, *args, **kwargs)
    return df
