from __future__ import division
import random
from unittest import TestCase
from Field import Field

from Polynomial import Polynomial

class test_Field(TestCase):
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    field = Field(p)

    def test_divide(self):
        divisionResult = self.field.divide(random.randrange(self.p -1), random.randrange(self.p -1))
        assert isinstance(divisionResult, int)
       

    