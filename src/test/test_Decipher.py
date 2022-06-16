import random
import string
from unittest import TestCase

from Decipher import Decipher
from LagrangeInterpolation import LagrangeInterpolation

class test_Decipher(TestCase):
    decipher = Decipher('in.aes','shares.frg')
    randomPassword = ''.join(random.sample(string.ascii_lowercase, 8))
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481    
    lagrangeInterpolation = LagrangeInterpolation(p, [(random.randrange(100), random.randrange(100)) for i in range(100)])

    def test_reconstructKey(self):        
        assert isinstance(self.lagrangeInterpolation.retrievePolynomialConstantTerm(), int)

    