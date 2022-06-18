import unittest
import numpy as np
from Mink.Util import local_max, csv_to_df, merge_delimiter, error_prop
import filecmp


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


class TestMergeDelimiter(unittest.TestCase):
    def test(self):
        '''test that delimiters have been merged correctly'''
        infile = "Mink/example_dataframes/MessedUpDelimiter.csv"
        outfile = "Mink/example_dataframes/FixedDelimiter.csv"
        answerfile = "Mink/example_dataframes/CorrectDelimiter.csv"
        merge_delimiter(infile, outfile)
        self.assertTrue(filecmp.cmp(answerfile, outfile, shallow=False))


class TestErrorPropagation(unittest.TestCase):
    precision: float = 0.001

    def test_ln(self):
        '''test that function properly propegates ln error'''
        args = [2]
        error_args = [2]
        prop = error_prop(np.log, args, error_args)
        self.assertLess(abs(1-prop[0]), self.precision)

    def test_ln_large(self):
        '''test that function works for large numbers'''
        args = [5e6]
        error_args = [1000]
        prop = error_prop(np.log, args, error_args)
        self.assertLess(abs(1000/5e6-prop[0]), self.precision)

    def test_ln_a(self):
        '''test proper propegation on slightly more complicated function'''
        def f(x, a):
            return a*np.log(x)
        args = [2, 1]
        error_args = [2, 1]
        prop = error_prop(f, args, error_args)
        calculated = np.sqrt(np.log(2)**2+1)
        self.assertLess(abs(calculated-prop[0]), self.precision)

    def test_independent_variable(self):
        "test error propegation on an array of independ variable x"
        x = np.array([1, 2, 3])
        a = 2
        error_a = 1

        def f(x, a):
            return a*np.log(x)

        prop = error_prop(f, [a], [error_a], ind_var=x)
        calculate = np.log(x)*error_a
        for i in range(len(x)):
            calc = calculate[i]
            p = prop[i]
            message = f"{calc} - {p} = {abs(calc-p)} not less than {self.precision}"
            self.assertLess(abs(calc-p), self.precision, message)


if __name__ == '__main__':
    unittest.main()
