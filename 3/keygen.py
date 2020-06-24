import sys
import math
from typing import List

def main():
    input = open(sys.argv[1], "r")
    text = input.read()
    input.close()
    permutation = list(map(int, text[1:-2].split(", ")))
    key = 42

def gen_keys(key: int, keylength: int, permutation: List[int]):
    keys = []
    # split up the key
    key_high, key_low = split_key(key, keylength)
    for i in range(16):
        # shift the bits
        key_low = sla(key_low, keylength//2, 2)
        key_high = sla(key_high, keylength//2, 2)
        # generate key by shifting the high bits back to its place and combining them with the low bits and then permuting it
        generated_key = permute((key_high << (keylength//2)) | key_low, permutation)
        keys.append(generated_key)
    return keys

def cycle_shift(key: int, keylength: int, n: int): # cyclic shift left of key with length keylength by n
    bitmask = (2**n - 1) << keylength - n  # bitmask for the highest n bits
    return ((key & ~bitmask) << n) | ((key & bitmask) >> (keylength - n)) # this is ok because << is a logical shift

def permute(key: int, permutation: List[int]):  # returns a key permuted with a given permutation
    permuted = 0
    for permuted_index, index in enumerate(permuation):
        key_bit = (key >> index) & 1    # get a bit of the key at the index index
        permuted = permuted | key_bit << permuted_index # set the permutated key at the index permuted_index to the bit of the key at the index index
    return permuted

def split_key(key: int, keylength: int):    # split the key into a high and a low part
    bitmask_low = 2**(keylength//2)-1 # this is ok because the keylength is supposed to be even
    bitmask_high = bitmask_low << (keylength//2) # same here
    key_low = key & bitmask_low
    key_high = (key & bitmask_high) >> (keylength//2)
    return key_high, key_low

if __name__ == "__main__":
    main()