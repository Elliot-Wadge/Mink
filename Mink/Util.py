import numpy as np
import pandas as pd


def local_max(arr, N=2, strict=False):
    '''find local maximums of an array where local is defined as M points on
    either side, if strict is true then it will follow this process exactly if
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
                # otherwise search in the other direction
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


def gaussian(x, a, b, c):
    '''plain gaussian'''
    return a*np.exp(-(x-b)**2/(2*c**2))


def lin_gaussian(x, a, b, c, d, e):
    '''gaussian function with linear background'''
    return a*np.exp(-(x-b)**2/(2*c**2))+d*x+e


def n_gaussian(x, *args, poly=0):
    '''gaussian with n peaks specified using a1,b1,c1,a2,b2,c2... poly=n specifies
    the order of polynomial to add as background, the coefficients should be
    entered in ascending order after the gaussian arguments, if poly=1 then
    there should be a constant and a slope at the end of args, benefit of this
    design is that it is compatable with curve_fit, and backgrounds can be
    easily included in fit with use of lambda function'''
    poly_args = args[-(poly+1):]
    gaussian_args = args[poly+1:]
    poly = np.polynomial.Polynomial(poly_args)
    ret = poly(x)
    for i in range(len(gaussian_args)//3):
        ret += gaussian(x, *args[3*i:3*(i+1)])
    return ret


def merge_delimiter(filename1: str, filename2: str, delimiter: str = ' ',
                    remove=None, new_delimiter=','):
    new_row = ''
    # open two files the one to read from filename1 and the new filename2
    with open(filename2, 'w') as f2:
        with open(filename1, 'r') as f1:
            # parse through the rows
            rows = f1.readlines()

            for number, row in enumerate(rows):
                start = False
                # start_of_row = True
                for i in range(0, len(row)):
                    # don't keep delimiters at the start of a row
                    if start or row[i] != delimiter:
                        start = True
                    # this is equivalent to saying if it's a delimeter and a
                    # repeat don't include (just invert logic)
                    if (row[i] != delimiter or row[i] != row[i+1]) and start:
                        if row[i] == delimiter and row[i+1] == "\n":
                            continue
                        new_row += row[i]

            # replace the delimiter with new delimiter
            new_row = new_row.replace(delimiter, new_delimiter)
            # write to the output file
            f2.write(new_row)
