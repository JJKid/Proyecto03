from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from LagrangeInterpolation import LagrangeInterpolation
from Polynomial import Polynomial
from getpass import getpass
import hashlib
import random
import os

class Cipher:    
    integerKey = None
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    def __init__(self, file_out: str, n: int, t: int, file_in: str):
        self.file_out = file_out
        self.n = n
        self.t = t
        self.file_in = file_in
        self.printObject()
        # Agregar validaciones al construir el objeto


    def printObject(self):
        print("Cipher object: " + self.file_out, self.n, self.t, self.file_in)

    def cipherFile(self):
        password = getpass("Enter a password to encrypt: ")
        self.writeCipheredFile(password)
        polynomial = Polynomial(self.n, self.t, self.integerKey, self.p)
        shares = polynomial.generateShares();
        self.writeSharesFile(shares, self.file_out)
        print("Integer key" , self.integerKey )
       
    def writeSharesFile(self, shares, outputFile):
        with open('shares.frg', 'w') as f:
            for tuple in shares:
                f.write(' '.join(str(s) for s in tuple) + '\n')
        print('shrares.frg created', shares)

    def writeCipheredFile(self, password):
        self.generateIntegerKey(password)
        salt = b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
        key = PBKDF2(str(self.integerKey), salt , dkLen=32)
        cipher = AES.new(key, AES.MODE_CFB)
        # Encrypt using the password converted into sha256 then to a number
        # Call encrypt_file using file_out provided        
        #print("Password en texto claro y su hash", password, self.getPasswordHashcode(password))        
        with open(self.file_in, 'rb') as input:
            encryptedData = self.encryptData(input.read(), cipher)
            # print(encryptedData) 

            with open(self.file_out , 'wb') as output:
                output.write(cipher.iv)
                output.write(encryptedData)
        #os.remove(self.file_in)

    def encryptData(self, data, cipher):        
        ciphertext = cipher.encrypt(data)
        return ciphertext

    def generateIntegerKey(self, password):
        self.integerKey = self.hashCodeToBase16(self.getPasswordHashcode(password))

    def getPasswordHashcode(self, password):
        hashcode = hashlib.sha256(password.encode()).digest()
        return hashcode

    def hashCodeToBase16(self, hashCode):
        secretInt = int(hashCode.hex(), base=16)
        return secretInt
    