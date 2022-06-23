import unittest
import numpy as np
from Mink.griffin import PerformFits
from Mink.util import n_gaussian
import plotly.graph_objects as go
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
        peaks = np.genfromtxt("Mink/example_GriffinData/hardtestpeaks.dat",
                              delimiter=',', usecols=0)
        x, y = np.genfromtxt("Mink/example_GriffinData/hard_test.dat",
                             delimiter=' ', unpack=True)
        res, fits = PerformFits(["Mink/example_GriffinData/hardtestpeaks.dat"],
                                x, y, (0, 1), cut_off=3, charge_window=10)

        missed = 0

        for fit in fits:
            result = False
            for i, peak in enumerate(peaks):
                if abs(fit.pOpt[1]-peak) < 1:
                    result = True
                    peaks = np.delete(peaks, i)  # should not fit peaks twice
                    break

            if not result:
                message = f"PoorFit: incorrectly fit a peak {fit.pOpt[1]}"
                warnings.warn(message)
                missed += 1
        self.assertLess(missed, 5)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))
        fig.update_layout(template="simple_white")
        for fit in fits:
            fig.add_trace(go.Scatter(x=fit.charge,
                                     y=fit.f(fit.charge, *fit.pOpt),
                                     mode="lines", line=dict(color='red')))
        fig.show()

    @unittest.expectedFailure
    def test_impossible(self):
        '''more strict version of test above'''
        peaks = np.genfromtxt("Mink/example_GriffinData/hardtestpeaks.dat",
                              delimiter=',',
                              unpack=True)
        x, y = np.genfromtxt("Mink/example_GriffinData/hard_test.dat",
                             delimiter=' ', unpack=True)
        res, fits = PerformFits(["Mink/example_GriffinData/hardtestpeaks.dat"],
                                x, y, (0, 1), cut_off=3, charge_window=12)

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
