import os
import sys
from LagrangeInterpolation import LagrangeInterpolation
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Polynomial import Polynomial
class Decipher:
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    def __init__(self, encryptedFile: str, sharesFile: str):
        self.encryptedFile = encryptedFile
        self.sharesFile = sharesFile
        self.shares = []
        
    def decipher(self):
        self.readSharesFile()
        recoveredIntegerKey = self.reconstructKey()
        salt = b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
        key = PBKDF2(str(recoveredIntegerKey), salt , dkLen=32)
        originalData = self.writeCipheredFile(key)
        
        try:
            with open(self.encryptedFile[:-4], 'wb') as f:
                f.write(originalData)
        except OSError:
                print("Could not write file:", self.encryptedFile[:-4])
                sys.exit()
        finally:
            os.remove(self.encryptedFile)

    def writeCipheredFile(self, key):
        try:
            with open(self.encryptedFile, 'rb') as f:
                iv = f.read(16)
                cipheredData = f.read()
                cipher = AES.new(key, AES.MODE_CFB, iv = iv)
                original_data = cipher.decrypt(cipheredData)
        except OSError:
                print("Could not read file:", self.encryptedFile)
                sys.exit()
        
        finally:
            return original_data

    def readSharesFile(self):
        shares = []
        try:            
            with open(self.sharesFile) as f:
                lines = f.readlines()
                for line in lines:
                    tmp = line.split(' ')
                    shares.append((int(tmp[0]), int(tmp[1])))
            self.shares = shares
        
        except OSError:
                print("Could not read file:", self.sharesFile)
                sys.exit()
        
        finally:
            os.remove(self.sharesFile)

    
    def reconstructKey(self):        
        lagrangeInterpolation = LagrangeInterpolation(self.p, self.shares)
        return lagrangeInterpolation.retrievePolynomialConstantTerm()
       