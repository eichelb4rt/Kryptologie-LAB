#!/bin/python3
# SHEBANG
from find_keylength import find_d
from decrypt_vigenere_known_d import crack_vigenere, get_language
import sys
import numpy as np

def decrypt():
    input = open(sys.argv[2], "r")
    text = input.read()
    input.close()
    m = int(sys.argv[4])
    language = get_language(sys.argv[3], m)
    keyspace = range(1,m)
    d = find_d(text)
    print(crack_vigenere(text, language, m, keyspace, d))

def encrypt():
    input = open(sys.argv[1], "r")
    text = input.read()
    input.close()
    m = int(sys.argv[3])
    key = [int(sys.argv[i]) for i in range(4,len(sys.argv))]
    crypto = encrypt_vigenere(text, m, key)
    output = open(sys.argv[2], "w")
    output.write(crypto)
    output.close()

def encrypt_vigenere(text: str, m: int, key: list):
    crypto = ""
    for i in range(0,len(text)):
        crypto += chr((ord(text[i]) + key[i%len(key)]) % m)
    return crypto

def main():
    if sys.argv[1] == "-d":
        decrypt()
    else:
        encrypt()

if __name__ == "__main__":
    main()