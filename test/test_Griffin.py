import unittest
import numpy as np
from Mink.Griffin import PerformFits
from Mink.Util import n_gaussian
import warnings


class TestFitter(unittest.TestCase):
    def test_easy(self):
        peaks = np.genfromtxt("Mink/example_GriffinData/easy_test.dat",
                              delimiter=',',
                              unpack=True)

        x = np.linspace(0, 70, 1000)
        y = n_gaussian(x, 10, peaks[0], 2, 20, peaks[1], 2, 5, peaks[2], 2, 0)
        res, fits = PerformFits(["Mink/example_GriffinData/easy_test.dat"], x,
                                y, (0, 1), cut_off=1, charge_window=6)
        message = "missed some peaks"
        self.assertEqual(len(fits), 3, message)

        for fit, peak in zip(fits, peaks):
            message = f"{fit.pOpt[1]}-{peak} is not less than 0.1"
            self.assertLess(abs(fit.pOpt[1]-peak), 0.1, message)

    def test_hard(self):
        '''test peak fitter on large array of peaks'''
        peaks = np.genfromtxt("Mink/example_GriffinData/allGamma.csv",
                              delimiter=',', usecols=0)
        x, y = np.genfromtxt("Mink/example_GriffinData/hard_test.dat",
                             delimiter=' ', unpack=True)
        print(len(x))
        res, fits = PerformFits(["Mink/example_GriffinData/allGamma.csv"], x,
                                y, (0, 1), cut_off=3, charge_window=10)
        message = "missed too many peaks (%40)"
        self.assertGreater(len(fits), len(peaks)*3/5, message)
        missed = 0

        for fit in fits:
            result = False
            for peak in peaks:
                if abs(fit.pOpt[1]-peak) < 1:
                    result = True
                    break

            if not result:
                message = f"PoorFit: incorrectly fit a peak {fit.pOpt[1]}"
                warnings.warn(message)
                missed += 1
        self.assertLess(missed, 6)

    @unittest.expectedFailure
    def test_impossible(self):
        '''more strict version of test above'''
        peaks = np.genfromtxt("Mink/example_GriffinData/allGamma.csv",
                              delimiter=',',
                              unpack=True)
        x, y = np.genfromtxt("Mink/example_GriffinData/hard_test.dat",
                             delimiter=' ', unpack=True)
        res, fits = PerformFits(["Mink/example_GriffinData/allGamma.csv"], x,
                                y, (0, 1), cut_off=3, charge_window=10)
        message = "missed too many peaks (%10): don't worry about this test"
        self.assertGreater(len(fits), len(peaks)*9/10, message)
        for fit in fits:
            result = False
            for peak in peaks:
                if abs(fit.pOpt[1]-peak) < 0.5:
                    result = True
                    break
            message = f"incorrectly fit a peak {fit.pOpt[1]}"
            self.assertTrue(result, message)


if __name__ == '__main__':
    unittest.main()
