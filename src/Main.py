
import sys
import os
import argparse

from Cipher import Cipher
from Decipher import Decipher

def valid_file(path):
    root, ext = os.path.splitext(path)
    if not ext:
        raise argparse.ArgumentTypeError(path + ' is not a file name. ' 'File must have a extension')
    return path

def main():

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="option")
    cipher = subparser.add_parser('c')
    decipher = subparser.add_parser('d')
    

    cipher.add_argument('file_out', type=valid_file, help='output file name to store polynomial evaluations')
    cipher.add_argument('n', type=int, help='number of evaluations required (n > 2)')
    cipher.add_argument('t', type= int, help='minimum number of points required to cipher (1 < t <= n)')
    cipher.add_argument('file_in',  type=valid_file, help='input file name')    

    decipher.add_argument('eval_file_in',  type=valid_file, help='input file name with t polynomial evaluations')  
    decipher.add_argument('encrypted_file_in',  type=valid_file, help='encrypted input file name ')  
    
    args = parser.parse_args() 
    if args.option == 'c':
        print(args.n, args.t)
        if args.n <= 2:
            print("n should be bigger than 2")
            sys.exit()
        if args.t > args.n or args.t <= 1:
            print("t should be smaller or equal than n, and bigger than 1")
            sys.exit()
        cipher = Cipher(args.file_out, args.n, args.t, args.file_in)
        cipher.cipherFile()
    
    elif args.option == 'd':
        decipher = Decipher(args.encrypted_file_in, args.eval_file_in )
        decipher.decipher()

if __name__ == "__main__":
    main()