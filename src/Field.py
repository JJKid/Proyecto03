class Field():
    def __init__(self, p):
        self.p = p

    def extended_euclides(self, a, b):
        """
        Extended Euclide algorith to find the gcd from a and b

        Args:
            a (int): number to find gcd with b
            b (int): number to find gcd with a

        Returns:
            int : gcd(a,b)
        """
        x = 0
        last_x = 1
        y = 1
        last_y = 0
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y
        return last_x, last_y

    def divide(self, x, y):
        multiplicativeInverse, _ = self.extended_euclides(y, self.p)
        return x * multiplicativeInverse