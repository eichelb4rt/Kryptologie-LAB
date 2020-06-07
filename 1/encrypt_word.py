#!/bin/python3
import numpy as np
import sys
def encrypt(text, key, m):
    crypt = ""
    for char in text:
        if char.isupper():
            crypt += chr((ord(char) - ord("A") + key)%m + ord("A"))
        elif char.islower():
            crypt += chr((ord(char) - ord("a") + key)%m + ord("a"))
        else:
            crypt += char
    return crypt
print(encrypt(sys.argv[1], int(sys.argv[2]), 26))