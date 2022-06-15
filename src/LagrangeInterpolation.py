from Field import Field


class LagrangeInterpolation:
    def __init__(self, p, shares):    
        self.p = p   
        self.shares = shares
        self.field_p = Field(p)
    

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
    
    def reconstruct_secret(self):
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
        x_points, y_points = zip(*self.shares)
        for i in range(len(x_points)):
            baseIPolynomial = self.createLagrangePolynomial(x, x_points[i], x_points)
            currProduct = (baseIPolynomial * y_points[i])
            res += currProduct
            
        return res % self.p