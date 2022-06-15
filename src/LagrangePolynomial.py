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

    def createLagrangePolynomial(self, x, x_i, x_points):
        """
        Reconstructs a Lagrange basis polynomial

        Args:
            x_i (int): [x_i] for the polynomial P_i(x)
            x_points (list): list of x points
            x (int): x value to evaluate for P_i(x)

        Returns:
            int: A Lagrange basis polynomial
        """
        dividend, divisor = 1, 1
        for j in range(len(x_points)):
            if x_points[j] != x_i:
                dividend *= x - x_points[j] 
                divisor *= (x_i-x_points[j])
                
        return self.field_p.divide(dividend, divisor) 
    
    def reconstruct_secret(self, shares):
        """
        Reconstructs the secret from a given list of shares
        Creates the base i polynomial evaluated on x = 0 for each x_i, 
        multiplies it by y_i and each of this products are added into
        res

        Args:
            shares (list): share to use to reconstruct the secret
            
        Raises:
            ValueError: in case that the number of shares is not enough to reconstruct the secret

        Returns:
            int: the secret
        """
        res = 0
        x = 0    
        x_points, y_points = zip(*shares)
        for i in range(len(x_points)):
            baseIPolynomial = self.createLagrangePolynomial(x, x_points[i], x_points)
            currProduct = (baseIPolynomial * y_points[i])
            res += currProduct
            
        return res % self.p