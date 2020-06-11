#!/bin/python3
# SHEBANG
from find_keylength import find_d
from decrypt_vigenere_known_d import crack_vigenere, get_language
import sys
import numpy as np

def main():
    # read input
    input = open(sys.argv[1], "r")
    text = input.read()
    input.close()
    # figure out m, ref language, keyspace, d
    m = int(sys.argv[3])
    language = get_language(sys.argv[2], m)
    keyspace = range(1,m)
    d = find_d(text)
    # (hacker voice): "I'm in!"
    print(crack_vigenere(text, language, m, keyspace, d, True))

if __name__ == "__main__":
    main()