import random
import string
from Cryptodome.Cipher import AES
from unittest import TestCase

from Cipher import Cipher

class test_Cipher(TestCase):
    cipher = Cipher('out.txt', random.randrange(10,20), random.randrange(1,9), 'in.txt')
    randomPassword = ''.join(random.sample(string.ascii_lowercase, 16))

    def test_generateIntegerKey(self):        
        assert isinstance(self.cipher.generateIntegerKey(self.randomPassword), int)

    def test_generateCipherMechanism(self):
        salt = b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
        integerKey = self.cipher.generateIntegerKey(self.randomPassword)
        cipherMechanism = self.cipher.generateCipherMechanism(integerKey, salt, AES.MODE_CFB)        
        assert cipherMechanism != None