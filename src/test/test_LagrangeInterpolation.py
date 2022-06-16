import random
from unittest import TestCase
from LagrangeInterpolation import LagrangeInterpolation

from Polynomial import Polynomial

class test_LagrangeInterpolation(TestCase):
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481    
    lagrangeInterpolation = LagrangeInterpolation(p, [(random.randrange(100), random.randrange(100)) for i in range(100)])

    def test_evaluateLagrangePolynomial(self):
        x_points, _ = zip(*self.lagrangeInterpolation.shares)
        evaluationResult = self.lagrangeInterpolation.evaluateLagrangePolynomial(random.randrange(10), random.choice(x_points), x_points)
        assert isinstance(evaluationResult, int)

    def test_reconstruct_secret(self):
        assert isinstance(self.lagrangeInterpolation.reconstruct_secret(), int) 
        assert self.lagrangeInterpolation.reconstruct_secret() < self.p