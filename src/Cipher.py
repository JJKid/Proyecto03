import os
import sys
from Cryptodome.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Polynomial import Polynomial
from getpass import getpass
import hashlib

class Cipher:    
    integerKey = None
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    def __init__(self, file_out: str, n: int, t: int, file_in: str):
        self.evaluationsOutputFile = file_out
        self.n = n
        self.t = t
        self.inputFile = file_in
  
    def cipherFile(self):
        password = getpass("Enter a password to encrypt: ")
        self.writeCipheredFile(password)
        polynomial = Polynomial(self.n, self.t, self.integerKey, self.p)
        shares = polynomial.generateShares();
        self.writeSharesFile(shares, self.evaluationsOutputFile)
        
    def writeCipheredFile(self, password):
        self.integerKey = self.generateIntegerKey(password)
        salt = b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
        cipherMechanism = self.generateCipherMechanism(self.integerKey,salt, AES.MODE_CFB)
        
        # Encrypt using the password converted into sha256 then to a number
        # Call encrypt_file using file_out provided        
        #print("Password en texto claro y su hash", password, self.getPasswordHashcode(password)) 
        
        try:               
            with open(self.inputFile, 'rb') as input:
                encryptedData = self.encryptData(input.read(), cipherMechanism)
            try:
                with open(self.inputFile + '.aes' , 'wb') as output:
                    output.write(cipherMechanism.iv)
                    output.write(encryptedData)
                
            except OSError:
                print("Could not write file:", self.inputFile + '.aes')
                sys.exit()
            
            finally:
                print(self.inputFile + '.aes created')
                os.remove(self.inputFile)

        except OSError:
            print("Could not open/read file:", self.inputFile)
            sys.exit()     
        
        
    def writeSharesFile(self, shares, outputFile):
        try:
           with open(outputFile, 'w') as f:
            for tuple in shares:
                f.write(' '.join(str(s) for s in tuple) + '\n')
            
        except OSError:
            print("Could not open/read file:", outputFile)
            sys.exit()

        finally:
            print(outputFile + ' created')

    def generateCipherMechanism(self, integerKey, salt, mode):
        key = PBKDF2(str(integerKey), salt , dkLen=32)
        cipherMechanism = AES.new(key, mode)
        return cipherMechanism 

    def encryptData(self, data, cipherMechanism):        
        ciphertext = cipherMechanism.encrypt(data)
        return ciphertext

    def generateIntegerKey(self, password):
        return self.hashCodeToBase16(self.getPasswordHashcode(password))

    def getPasswordHashcode(self, password):
        hashcode = hashlib.sha256(password.encode()).digest()
        return hashcode

    def hashCodeToBase16(self, hashCode):
        secretInt = int(hashCode.hex(), base=16)
        return secretInt
    