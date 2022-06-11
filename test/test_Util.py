import unittest
import numpy as np
from Mink.Util import local_max, csv_to_df


class TestLocalMax(unittest.TestCase):
    def test_lm_sin(self):
        '''test that local max can find multiple maxes on a sin function'''
        x = np.arange(0, 5.25, 0.25)*np.pi
        y = np.sin(x)
        maxes, index = local_max(y, N=10)
        self.assertEqual(list(maxes), [1, 1, 1])
        self.assertEqual(list(index), [2, 10, 18])

    def test_lm_lin(self):
        '''test that local max correctly identifies that there are no maxima on
        a linear slope'''
        x = np.linspace(0, 10, 20)
        maxes, index = local_max(x)
        self.assertEqual(len(maxes), 0)
        self.assertEqual(len(index), 0)

    def test_lm_max(self):
        '''test the local max behaves properly when searching for the largest local
        max across the whole array'''
        x = np.linspace(0, np.pi, 51)
        y = np.sin(x)
        maxes, index = local_max(y, N=len(y))
        self.assertEqual(list(maxes), [1.])
        self.assertEqual(list(index), [25])


class TestCsvToDf(unittest.TestCase):
    def test_dtc_multiple(self):
        '''test that csv_to_df can load multiple files properly'''
        df = csv_to_df(["Mink/example_dataframes/df1.csv",
                       "Mink/example_dataframes/df2.csv"], comment="#")
        self.assertEqual(len(df), 5)
        self.assertEqual(len(df.columns), 2)

    def test_dtc_single(self):
        '''test that csv_to_df can load a single file'''
        df = csv_to_df("Mink/example_dataframes/df2.csv", comment="#")
        self.assertEqual(len(df), 3)
        self.assertEqual(len(df.columns), 2)


if __name__ == '__main__':
    unittest.main()
