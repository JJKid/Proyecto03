import enum
import random
from numpy.polynomial.polynomial import Polynomial as Poly
import numpy.polynomial.polynomial as polynomial
from Field import Field
class LagrangePolynomial:
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

    def lagrange_polynomial(self, i, x_points, x):
        """
        Reconstructs a Lagrange basis polynomial

        Args:
            i (int): [x_i]
            x_points (list): vector of x points
            x (int): value to find

        Returns:
            int: A Lagrange basis polynomial
        """
        num, dem = 1, 1 # We calculate each separately to avoid inexcat division
        for j in range(len(x_points)):
            if x_points[j] != i:
                num *= x - x_points[j] # X - x_j
                dem *= (i-x_points[j]) # x_i - x_j
                
        return self.field_p.divide(num, dem) # (X - x_j) (x_i - x_j)^-1 -> where (x_i - x_j)^-1 is the inverse multiplicative
    
    def reconstruct_secret(self, shares):
        """
        Reconstructs the secret from a given list of shares

        Args:
            shares (list): share to use to reconstruct the secret
            x (int): term to find

        Raises:
            ValueError: in case that the number of shares is not enough to reconstruct the secret

        Returns:
            int: the secret
        """
        res = 0
        x = 0        
        x_points, y_points = zip(*shares)
        for i in range(len(x_points)):
            poly = self.lagrange_polynomial(x_points[i], x_points, x)
            
            product = (poly * y_points[i]) % self.p
            
            res += product
            
        return res % self.p