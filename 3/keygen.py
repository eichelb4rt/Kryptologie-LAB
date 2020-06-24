#!/bin/python3

import argparse
import math
from typing import List

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        metavar = 'in',
        dest = 'input',
        help = 'File that the key is read from'
    )
    parser.add_argument(
        metavar = 'out',
        dest = 'output',
        help = 'File that the generated keys are written to'
    )
    parser.add_argument(
        '-p',
        metavar = 'perm',
        dest = 'permutation',
        default = 'permutation.txt',
        help = 'File that the permutation is read from (default: permutation.txt)'
    )
    parser.add_argument(
        '-k',
        metavar = 'keylength',
        dest = 'keylength',
        type = int,
        default = 64,
        help = 'The length of the key (default: 64)'
    )
    parser.add_argument(
        '--hex',
        dest = 'binary',
        action = 'store_true',
        default = 'false',
        help = 'store the keys in hexadecimal numbers instead of ints'
    )
    args = parser.parse_args()
    # read permutation
    with open(args.permutation, "r") as f:
        permutation = list(map(int, f.read()[1:-2].split(", ")))    # strip [*] and the line break
    # read key
    with open(args.input, "r") as f:
        key = int(f.read())
    # generate keys and make em hexa if the user wants to
    generated_keys = gen_keys(key, args.keylength, permutation)
    if args.binary:
        generated_keys = [key.to_bytes(8, 'big').hex() for key in generated_keys]
    # write generated keys to output
    with open(args.output, "w") as f:
        f.write(str(generated_keys))

def gen_keys(key: int, keylength: int, permutation: List[int]):
    keys = []
    # split up the key
    key_high, key_low = split_key(key, keylength)
    for i in range(16):
        # shift the bits
        key_low = cycle_shift(key_low, keylength//2, 2)
        key_high = cycle_shift(key_high, keylength//2, 2)
        # generate key by shifting the high bits back to its place and combining them with the low bits and then permuting it
        generated_key = permute((key_high << (keylength//2)) | key_low, permutation)
        keys.append(generated_key)
    return keys

def cycle_shift(key: int, keylength: int, n: int): # cyclic shift left of key with length keylength by n
    bitmask = (2**n - 1) << keylength - n  # bitmask for the highest n bits
    return ((key & ~bitmask) << n) | ((key & bitmask) >> (keylength - n)) # this is ok because << is a logical shift

def permute(key: int, permutation: List[int]):  # returns a key permuted with a given permutation
    permuted = 0
    for permuted_index, index in enumerate(permutation):
        key_bit = (key >> index) & 1    # get a bit of the key at the index index
        permuted = permuted | key_bit << permuted_index # set the permutated key at the index permuted_index to the bit of the key at the index index
    return permuted

def split_key(key: int, keylength: int):    # split the key into a high and a low part
    bitmask_low = 2**(keylength//2)-1 # this is ok because the keylength is supposed to be even
    key_low = key & bitmask_low
    key_high = key >> (keylength//2)
    return key_high, key_low

if __name__ == "__main__":
    main()