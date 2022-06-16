from Field import Field

class LagrangeInterpolation:
    """
    Class to represent a LagrangeInterpolation

    This object is used to model a LagrangeInterpolation operation 
    where you need to create a multiple Langrange polynomials of base i
    using the shares provided and multiply them with the evaluations of P(x=0) 
    to recreate the constant term of the polynomial
    ...

    Attributes
    ----------
    p : int
        prime number used to create a Field
    shares : list[tuples]
        list of tuples corresponding to the points previously on the 
        polynomial
           
    """
    def __init__(self, p, shares):    
        self.p = p   
        self.shares = shares
        self.field_p = Field(p)
    

    def createLagrangeBaseIPolynomial(self, x, x_i, xPoints):
        """
        Create a Lagrange polinomial of base i from the points provided
        on the shares and evaluate it on x

        Uses Field artimetic to do the division required in the Lagrange
        Polynomial calculation

        Parameters
        ----------
        x : int
            x used on the P_i(x) construction
        x_i : int 
            x_i used on the P_i(x) construction

        xPoints : int 
            x_i used on the P_i(x) construction
                          
        Returns
        -------
            The result of the created Lagrange base i polinomial
            evaluated on x = 0

        """
        dividend, divisor = 1, 1
        for j in range(len(xPoints)):
            if xPoints[j] != x_i:
                dividend *= x - xPoints[j] 
                divisor *= (x_i-xPoints[j])
                
        return self.field_p.divide(dividend, divisor) 
    
    def retrievePolynomialConstantTerm(self):
        """
        Reconstructs the constant term of the polynomial from the list
        of shares        
                                
        Returns
        -------
            The constant term of the original polynomial modulo p,
            if the number of shares is equal to t

        """
        res = 0
        x = 0    
        xPoints, yPoints = zip(*self.shares)
            
        for i in range(len(xPoints)):
            baseIPolynomial = self.createLagrangeBaseIPolynomial(x, xPoints[i], xPoints)
            currProduct = (baseIPolynomial * yPoints[i])
            res += currProduct
            
        return res % self.p