import os
import sys
from Cryptodome.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Polynomial import Polynomial
from getpass import getpass
import hashlib

class Cipher: 
    """
    Class to represent an Cipher object

    This object is used to handle all the encrypting procedure
    creating the shares of the original polynomial and writing
    an encrypted file from the original input file data
    ...

    Attributes
    ----------
    evaluationsOutputFile : str 
        file name where shares will be saved
    n : int
        number of shares to generate from this polynomial
    t : int
        minimum number of shares required to rebuild the polynomial
    inputFile : str
        file name with original data that will be encrypted
    
    """   
    integerKey = None
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    def __init__(self, evaluationsOutputFile: str, n: int, t: int, inputFile: str):
        self.evaluationsOutputFile = evaluationsOutputFile
        self.n = n
        self.t = t
        self.inputFile = inputFile
  
    def cipherFile(self):
        """
        Method that use a received password to encrypt the input file
        and the integer key asociated with this password is used as 
        constant term of a polynomial from shares are generated and
        written into a file
    
        """  
        password = getpass("Enter a password to encrypt: ")
        self.writeCipheredFile(password)
        polynomial = Polynomial(self.n, self.t, self.integerKey, self.p)
        shares = polynomial.generateShares();
        self.writeSharesFile(shares, self.evaluationsOutputFile)
        
    def writeCipheredFile(self, password):
        """
        
        Method that reads input file and encrypts into an .aes file
        using the entered password by the user. 

        Attributes
        ----------
        password : str 
            string entered as password by the user        
        
        """  
        self.integerKey = self.generateIntegerKey(password)
        salt = b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
        cipherMechanism = self.generateCipherMechanism(self.integerKey,salt, AES.MODE_CFB)
        
               
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
            print("Could not open/read input file:", self.inputFile)
            sys.exit()     
        
        
    def writeSharesFile(self, shares, outputFile):
        """
        Method that write the list of tuples that contain the shares
        of the polynomial into an output file

        Attributes
        ----------
        shares : list[tuples]
            list of shares of the polynomial

        outputFile : str 
            file name where shares will be saved
                
        """  
        try:
           with open(outputFile, 'w') as f:
            for tuple in shares:
                f.write(' '.join(str(s) for s in tuple) + '\n')
            
        except OSError:
            print("Could not write shares file:", outputFile)
            sys.exit()

        finally:
            print(outputFile + ' created')

    def generateCipherMechanism(self, integerKey, salt, mode):
        """
            Creates a new AES object built from an integer key and a bytes string used
            as salt, which is used to perform the encryption operation of data

            Attributes
            ----------
            integerKey : int
                integer key associated with the sha-256 of the original entered password 

            salt : str 
                addtional input to add to the key, to avoid that the result password could be
                found on a rainbow table
                https://en.wikipedia.org/wiki/Rainbow_table

            mode : str
                AES mode of encryption
            
            Returns
            -------
                An AES encrypter object 
                
        """
        key = PBKDF2(str(integerKey), salt , dkLen=32)
        return AES.new(key, mode)

    def encryptData(self, data, cipherMechanism):      
        """
            Method that encrypts data read from a file using an AES
            mechanism previously built

            Attributes
            ----------
            data : bytes
                stream of bytes read from an input file 

            cipherMechanism : AES 
                AES encrypter object
            
            Returns
            -------
                An encoded string of bytes as ciphertext
                
        """   
        return cipherMechanism.encrypt(data)

    def generateIntegerKey(self, password):
        """
            Method that converts a entered password to an integer key

            Attributes
            ----------
            password : str
                password string entered by the user

            Returns
            -------
                An integer associated with entered password
                
        """     
        return self.hashCodeToBase16(self.getPasswordHashcode(password))

    def getPasswordHashcode(self, password):
        """
            Method that generates a hash of the entered password
            using sha-256

            Attributes
            ----------
            password : str
                password string entered by the user 
            
            Returns
            -------
                An encoded string of bytes as the sha-256 for the entered password
                
        """   
        return hashlib.sha256(password.encode()).digest()

    def hashCodeToBase16(self, hashCode):
        """
            Method that receives a bytes string asocciated with a 
            password hashcode and convert it to an integer base 16

            Attributes
            ----------
            hashCode : bytes
                bytes string associated with a password hash
                       
            Returns
            -------
                An integer key associated with the hashCode
                
        """     
        return int(hashCode.hex(), base=16)