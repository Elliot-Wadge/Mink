import pytest
import numpy as np
from Mink.Util import local_max, csv_to_df


def test_lm_sin():
    '''test that local max can find multiple maxes on a sin function'''
    x = np.arange(0, 5.25, 0.25)*np.pi
    y = np.sin(x)
    maxes, index = local_max(y, N=10)
    assert list(maxes) == [1, 1, 1]
    assert list(index) == [2, 10, 18]


def test_lm_lin():
    '''test that local max correctly identifies that there are no maxima on
    a linear slope'''
    x = np.linspace(0, 10, 20)
    maxes, index = local_max(x)
    assert len(maxes) == 0
    assert len(index) == 0


def test_lm_max():
    '''test the local max behaves properly when searching for the largest local
    max across the whole array'''
    x = np.linspace(0, np.pi, 51)
    y = np.sin(x)
    maxes, index = local_max(y, N=len(y))
    assert list(maxes) == [1.]
    assert list(index) == [25]


def test_dtc_multiple():
    '''test that csv_to_df can load multiple files properly'''
    df = csv_to_df(["Mink/example_dataframes/df1.csv",
                   "Mink/example_dataframes/df2.csv"], comment="#")
    assert len(df) == 5
    assert len(df.columns) == 2


def test_dtc_single():
    '''test that csv_to_df can load a single file'''
    df = csv_to_df("Mink/example_dataframes/df2.csv", comment="#")
    assert len(df) == 3
    assert len(df.columns) == 2
