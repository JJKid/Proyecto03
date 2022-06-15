from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from LagrangePolynomial import LagrangePolynomial
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
        lagrangePolynomial = LagrangePolynomial(self.n, self.t, self.integerKey, self.p)
        shares = lagrangePolynomial.generateShares();
        print("Integer key" , self.integerKey )
        print("Reconstructed secret:",  lagrangePolynomial.reconstruct_secret(shares))
        print(lagrangePolynomial.reconstruct_secret(shares) == self.integerKey)
        

    def writeCipheredFile(self, password):
        salt = get_random_bytes(32)
        self.integerKey = self.hashCodeToBase16(self.getPasswordHashcode(password))
        key = PBKDF2(str(self.integerKey), salt , dkLen=32)
        # Encrypt using the password converted into sha256 then to a number
        # Call encrypt_file using file_out provided        
        #print("Password en texto claro y su hash", password, self.getPasswordHashcode(password))        
        with open(self.file_in, 'rb') as input:
            encryptedData = self.encryptData(key, input.read())
            # print(encryptedData) 

            with open(self.file_out , 'wb') as output:
                output.write(encryptedData)
        #os.remove(self.file_in)

    def encryptData(self, key, data):
        cipher = AES.new(key, AES.MODE_CFB)
        ciphertext = cipher.encrypt(data)
        return ciphertext

    def getPasswordHashcode(self, password):
        hashcode = hashlib.sha256(password.encode()).digest()
        return hashcode

    def hashCodeToBase16(self, hashCode):
        secretInt = int(hashCode.hex(), base=16)
        return secretInt
    