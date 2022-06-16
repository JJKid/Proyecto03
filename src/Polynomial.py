import random
import numpy as np 
from Field import Field
class Polynomial:
    def __init__(self, n: int, t: int, integerKey: int, p: int):        
        self.n = n
        self.t = t
        self.integerKey = integerKey
        self.p = p
        self.field_p = Field(self.p)
        self.polynomialCoefficients = self.generateCoefficients()
       
    def generateCoefficients(self):
        coefficients = [random.randrange(self.p - 1) for _ in range(self.t)]
        coefficients.append(self.integerKey)
        return coefficients

    def evaluatePoint(self, x, coefficients):
        return np.polyval(np.poly1d(coefficients), x)

    def generateShares(self):
        shares = []
        for i in range(1, self.n + 1):
            x = random.randrange(self.p - 1)
            shares.append((x, self.evaluatePoint(x, self.polynomialCoefficients) % self.p ))
        return shares
    

    