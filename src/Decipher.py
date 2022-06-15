from LagrangeInterpolation import LagrangeInterpolation
from Crypto.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Polynomial import Polynomial
class Decipher:
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    def __init__(self, encryptedFile: str, sharesFile: str):
        self.encryptedFile = encryptedFile
        self.sharesFile = sharesFile
        self.shares = []
        # Agregar validaciones al construir el objeto

    def decipher(self):
        self.readSharesFile()
        recoveredIntegerKey = self.reconstructKey()
        print("Retrieved integer key", recoveredIntegerKey)
        salt = b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
        key = PBKDF2(str(recoveredIntegerKey), salt , dkLen=32)
        originalData = self.writeCipheredFile(key)
        with open('in2.txt', 'wb') as f:
            f.write(originalData)

    def writeCipheredFile(self, key):
        file_in = open(self.encryptedFile, 'rb')
        iv = file_in.read(16)
        cipheredData = file_in.read()
        file_in.close()

        cipher = AES.new(key, AES.MODE_CFB, iv = iv)
        original_data = cipher.decrypt(cipheredData)
        return original_data

    def readSharesFile(self):
        shares = []
        with open(self.sharesFile) as f:
            lines = f.readlines()
            for line in lines:
                tmp = line.split(' ')
                try:
                    shares.append((int(tmp[0]), int(tmp[1])))
                except: pass
        self.shares = shares

    
    def reconstructKey(self):        
        lagrangeInterpolation = LagrangeInterpolation(self.p, self.shares)
        # Use this one as test
        #print(lagrangeInterpolation.reconstruct_secret() == self.integerKey)
        return lagrangeInterpolation.reconstruct_secret()
       