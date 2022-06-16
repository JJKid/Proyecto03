import random
from unittest import TestCase

from Polynomial import Polynomial

class test_Polynomial(TestCase):
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    polynomial = Polynomial(random.randrange(10,20), random.randrange(0,9), random.randrange(p), p)

    def test_generateCoefficients(self):
        coefficients = self.polynomial.generateCoefficients()
        assert all(isinstance(c, int) for c in coefficients)

    def test_evaluatePoint(self):
        assert isinstance(self.polynomial.evaluatePoint(random.randrange(100),
        self.polynomial.generateCoefficients()), int)

    def test_generateShares(self):
        shares = self.polynomial.generateShares()
        assert all(isinstance(t, tuple) for t in shares)