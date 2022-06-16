from egcd import egcd

class Field():
    """
    Class to represent a Field to do operations modulo some prime p
    ...

    Attributes
    ----------
    p : int
        prime where we define our Field
    
    """
    def __init__(self, p):
        self.p = p

    def divide(self, x, y):   
        """ 
        Method to do modular division, x/y modulo p

        We use the Euclides GCD extended algorithm to find the
        multiplicative inverse of y. Then we multiply it with
        x to get the result

        Parameters
        ----------
        x : int
            Dividend 
        y : int
            Divisor      
        Returns
        -------
            The result of x/y modulo p

        """    
        multiplicativeInverse = egcd(y, self.p)[1]
        return x * multiplicativeInverse
        