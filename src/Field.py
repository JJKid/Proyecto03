from egcd import egcd

class Field():
    def __init__(self, p):
        self.p = p

    def divide(self, x, y):       
        multiplicativeInverse = egcd(y, self.p)[1]
        return x * multiplicativeInverse