import unittest
import numpy as np
from Mink.Griffin import PerformFits
from Mink.Util import n_gaussian


class TestFitter(unittest.TestCase):
    def test_easy(self):
        peaks = np.genfromtxt("Mink/example_GriffinData/easy_test.dat",
                              delimiter=',',
                              unpack=True)

        x = np.linspace(0, 70, 1000)
        y = n_gaussian(x, 10, peaks[0], 2, 20, peaks[1], 2, 5, peaks[2], 2, 0)
        res, fits = PerformFits(["Mink/example_GriffinData/easy_test.dat"], x, y,
                                (0, 1), cut_off=1, charge_window=6)
        message = "missed some peaks"
        self.assertEqual(len(fits), 3, message)

        for fit, peak in zip(fits, peaks):
            message = f"{fit.pOpt[1]}-{peak} is not less than 0.1"
            self.assertLess(abs(fit.pOpt[1]-peak), 0.1, message)


if __name__ == '__main__':
    unittest.main()
