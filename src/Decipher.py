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
            """
    Class to represent an Decipher object

    This object is used to handle all the decrypting procedure
    using the shares from the original polynomial and decrypting
    the encrypted file from the original input file data
    ...

    Attributes
    ----------
    encryptedFile : str 
        file name with the original data encrypted
    
    sharesFile : str
        file name with the shares of the polinomial as a list of tuples
    
    """   
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    def __init__(self, encryptedFile: str, sharesFile: str):
        self.encryptedFile = encryptedFile
        self.sharesFile = sharesFile
        self.shares = []
        
    def decipher(self):
        """
        Method that read the shares file and from this shares reconstruct
        the constant term of the associated polynomial which is the integer 
        key used for encrypting, then creates a decrypting mechanism with 
        this key, decrypt the .aes file and write out the result into a file
        with the same name as the original
            
        """  
        self.readSharesFile()
        recoveredIntegerKey = self.reconstructKey()
        salt = b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
        key = PBKDF2(str(recoveredIntegerKey), salt , dkLen=32)
        originalData = self.writeDecipheredFile(key)
        
        try:
            with open(self.encryptedFile[:-4], 'wb') as f:
                f.write(originalData)
        except OSError:
            print("Could not write deciphered file:", self.encryptedFile[:-4])
            sys.exit()
        finally:
            os.remove(self.sharesFile)
            os.remove(self.encryptedFile)

    def writeDecipheredFile(self, key):
        """
        Method that read the shares file and from this shares reconstruct
        the constant term of the associated polynomial which is the integer 
        key used for encrypting, then creates a decrypting mechanism with 
        this key, decrypt the .aes file and write out the result into a file
        with the same name as the original

        Attributes
        ----------
        key : bytes 
            bytes string with a key created from retrieved integer key and a salt
            
        """  
        try:
            with open(self.encryptedFile, 'rb') as f:
                iv = f.read(16)
                cipheredData = f.read()
                cipher = AES.new(key, AES.MODE_CFB, iv = iv)
                original_data = cipher.decrypt(cipheredData)
        except OSError:
            print("Could not write file:", self.encryptedFile)
            sys.exit()
        
        finally:
            return original_data

    def readSharesFile(self):
        """
        Method that reads a file with the shares of the polynomial
        and saves every tuple read into a list     
        """
        shares = []
        try:            
            with open(self.sharesFile) as f:
                lines = f.readlines()
                for line in lines:
                    tmp = line.split(' ')
                    shares.append((int(tmp[0]), int(tmp[1])))
            self.shares = shares
        
        except OSError:
            print("Could not read shares file:", self.sharesFile)
            sys.exit()      
           
    def reconstructKey(self):
        """
        Method that use a received password to encrypt the input file
        and the integer key asociated with this password is used as 
        constant term of a polynomial from shares are generated and
        written into a file
    
        """          
        lagrangeInterpolation = LagrangeInterpolation(self.p, self.shares)
        return lagrangeInterpolation.retrievePolynomialConstantTerm()
       