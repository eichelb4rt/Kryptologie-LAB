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

input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")
output.write(encrypt(input.read(), int(sys.argv[3]), 26))
input.close()
output.close()