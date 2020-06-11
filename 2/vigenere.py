#!/bin/python3
# SHEBANG
from find_keylength import find_d
from decrypt_vigenere_known_d import crack_vigenere, get_language
import sys
import numpy as np

def main():
    offset = 0
    onlyKey = False
    if sys.argv[1] == "-k":
        onlyKey = True
        offset -=- 1
    # read input
    input = open(sys.argv[1 + offset], "r")
    text = input.read()
    input.close()
    # figure out m, ref language, keyspace, d
    m = int(sys.argv[3 + offset])
    language = get_language(sys.argv[2 + offset], m)
    keyspace = range(1,m)
    d = find_d(text)
    # (hacker voice): "I'm in!"
    print(crack_vigenere(text, language, m, keyspace, d, onlyKey))

if __name__ == "__main__":
    main()