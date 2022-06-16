import random
import numpy as np 
from Field import Field
class Polynomial:
    """
    Class to represent a Polynomial

    This object is used to model a polinomial with random coefficients
    and constant equal to a integer key associated with a password used to encrypt
    ...

    Attributes
    ----------
    n : int
        number of shares to generate from this polynomial
    t : int
        minimum number of shares required to rebuild the polynomial
    integerKey : int
        key used as constant in the polynomial
    p : int
        prime number used to create a Field
    
    """
    def __init__(self, n: int, t: int, integerKey: int, p: int):        
        self.n = n
        self.t = t
        self.integerKey = integerKey
        self.p = p
        self.field_p = Field(self.p)
        self.polynomialCoefficients = self.generateCoefficients()
       
    def generateCoefficients(self):
        """ 
        Generate t random coefficients of the polynomial plus the constant at 
        the end
                          
        Returns
        -------
            A list of integers with the coefficients
        """
        coefficients = [random.randrange(self.p - 1) for _ in range(self.t)]
        coefficients.append(self.integerKey)
        return coefficients

    def evaluatePoint(self, x, coefficients):
        """ 
        Return the evaluation of a point x in the polynomial p

        Parameters
        ----------
        x : int
            Integer number to be evaluated
        
        coefficients : list[int]
            List of integers with the polynomial coefficients
                          
        Returns
        -------
            An integer corresponding to the evaluation of x in the polynomial
        """
        return np.polyval(np.poly1d(coefficients), x)

    def generateShares(self):
        """ 
        Generate n tuples corresponding to random x points
        evaluated on the polynomial modulo p, which is the prime we use for 
        our Field
                          
        Returns
        -------
            A list of tuples corresponding to (x, f(x)) where P(x) means evaluating
            x on this polynomial P
        """
        shares = []
        for i in range(1, self.n + 1):
            x = random.randrange(self.p - 1)
            shares.append((x, self.evaluatePoint(x, self.polynomialCoefficients) % self.p ))
        return shares
    