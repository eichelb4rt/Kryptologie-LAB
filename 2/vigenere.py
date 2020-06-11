#!/bin/python3
# SHEBANG
from find_keylength import find_d
from decrypt_vigenere_known_d import crack_vigenere, get_language
import sys
import numpy as np

def main():
    input = open(sys.argv[1], "r")
    text = input.read()
    input.close()
    m = int(sys.argv[3])
    language = get_language(sys.argv[2], m)
    keyspace = range(1,m)
    d = find_d(text)
    print(crack_vigenere(text, language, m, keyspace, d))

if __name__ == "__main__":
    main()