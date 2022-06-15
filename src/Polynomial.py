import enum
import random
from numpy.polynomial.polynomial import Polynomial as Poly
import numpy.polynomial.polynomial as polynomial
from Field import Field
class Polynomial:
    def __init__(self, n: int, t: int, integerKey: int, p: int):        
        self.n = n
        self.t = t
        self.integerKey = integerKey
        self.p = p
        self.field_p = Field(self.p)

    def horner(self, x, poly, n):
    
        # Initialize result
        result = poly[0] 
    
        # Evaluate value of polynomial
        # using Horner's method
        for i in range(1, n):    
            result = result*x + poly[i]
        print("horner", x, result)
        return result
   

    def generateCoefficients(self):
        coefficients = [random.randrange(self.p - 1) for _ in range(self.t)]
        coefficients[0] = self.integerKey
        print("COEFF", coefficients, self.t)
        self.polynomial = Poly(coefficients)
        

    def generateShares(self):
        self.generateCoefficients()
        shares = []

        for i in range(1, self.n + 1):
            x = random.randrange(self.p - 1)
            shares.append((x, polynomial.polyval(x, self.polynomial.coef) % self.p ))
        return shares
    

    