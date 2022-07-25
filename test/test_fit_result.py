import unittest
from Mink import full_return
import numpy as np
from scipy.optimize import curve_fit


class TestFitResult(unittest.TestCase):
        
    def test_FitResultInitialization(self):
        my_curve_fit = full_return(curve_fit)
        
        def linear(x, a, b):
            return a*x + b
        
        x = np.linspace(0,10,200)
        y = 2*x + np.random.normal(scale=0.3, size=len(x))
        err = np.ones(len(x))*0.3
        res = my_curve_fit(linear, x, y, sigma=err, absolute_sigma=True)
        
        self.assertTrue(res.f == linear)
        self.assertAlmostEqual(res.chisq, 1, delta=0.5)
        self.assertAlmostEqual(res.pOpt[0], 2, delta=0.2)
        self.assertTrue(np.array_equal(res.y, y))
        self.assertTrue(np.array_equal(res.x, x))
        self.assertTrue(np.array_equal(res.yErr, err))
        
    def test_Comparison(self):
        my_curve_fit = full_return(curve_fit)
        
        def linear(x, a, b):
            return a*x + b
        
        def quadratic(x, a, b, c):
            return a*x**2 + b*x + c
        
        # will cause warning in pCov, 'Covariance of the parameters could not be estimated'
        def quadratic_unnecessary_term(x, a, b, c, d):
            return a*x**2 + b*x + c
        
        x = np.linspace(0,10,200)
        y = quadratic(x, 0.4, 1, 1) + np.random.normal(scale=0.3, size=len(x))
        err = np.ones(len(x))*0.3
        res1 = my_curve_fit(linear, x, y, sigma=err, absolute_sigma=True)
        res2 = my_curve_fit(quadratic, x, y, sigma=err, absolute_sigma=True)
        res3 = my_curve_fit(quadratic_unnecessary_term, x, y, sigma=err, absolute_sigma=True)
        
        self.assertLess(res2.chisq, res1.chisq)
        self.assertGreater(res3.chisq, res2.chisq)
        self.assertEqual(res2.chisq, res2.chisq)
        