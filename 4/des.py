#!/bin/python3

import argparse
from keygen import gen_keys, split_key
from typing import List

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        metavar = 'in',
        dest = 'input',
        help = 'File that the input text is read from'
    )
    parser.add_argument(
        metavar = 'out',
        dest = 'output',
        help = 'File that the output text is written to'
    )
    parser.add_argument(
        '-k',
        '--key',
        metavar = 'key',
        dest = 'key',
        default = 'key.txt',
        help = 'File that the key is read from (default: key.txt)'
    )
    parser.add_argument(
        '-l',
        '--blocklength',
        metavar = 'blocklength',
        dest = 'blocklength',
        type = int,
        default = 128,
        help = 'The length of the blocks in bits (default: 128)'
    )
    parser.add_argument(
        '-S',
        '--Sbox',
        metavar = 's_box',
        dest = 's_box',
        default = 's-box.txt',
        help = 'File that the s-box is read from (default: s-box.txt)'
    )
    parser.add_argument(
        '-p',
        metavar = 'perm',
        dest = 'permutation',
        default = 'permutation.txt',
        help = 'File that the permutation for key generation is read from (default: permutation.txt)'
    )
    parser.add_argument(
        '-d',
        '--decrypt',
        dest = 'decrypt',
        action = 'store_true',
        default = 'false',
        help = 'decrypt from the input to the output instead of encrypting'
    )
    args = parser.parse_args()
    # read permutation
    with open(args.permutation, "r") as f:
        permutation = list(map(int, f.read()[1:-2].split(", ")))    # strip [*] and the line break
    # read key
    with open(args.key, "r") as f:
        key = int(f.read(), 16)
    # generate keys
    generated_keys = gen_keys(key, args.blocklength//2, permutation)
    # read s-box
    with open(args.s_box, "r") as f:
        s_box = [int(byte, 16) for byte in f.read()[1:-2].split(", ")]   # strip [*] and the line break
    # read input
    input = []
    with open(args.input, "rb") as f:
        while block := f.read(args.blocklength//8): # we need to read 2*keylength bits, so we need to 
            input.append(int(block) << (args.blocklength - len(block)))  # pad the block if it's not full (fill the right side with 0)
    print(input)
    # apply DES encryption or decryption
    if args.decrypt:
        #decrypted_bytes = decrypt(input, )
        pass
    else:
        #encrypt
        pass
    # write generated keys to output
    #with open(args.output, "w") as f:
    #    f.write(str(generated_keys))

def encrypt(block: int, keys: List[int], s_box: List[int], blocklength: int):
    pass

def encrypt_block(block: int, keys: List[int], s_box: List[int], blocklength: int):
    R, L = split_key(block, blocklength)  # use the split_key function from key_gen: turns a (keylength) Integer into 2 (keylength//2) Integers.
    for i in range(16):
        L, R = encryption_step(L, R, keys[i], s_box, blocklength)
    L, R = R, L # swap em one last time

def encryption_step(L: int, R: int, key: int, s_box: List[int], blocklength: int):
    next_L = R
    next_R = r_function(R, key, s_box, blocklength) ^ L
    return next_L, next_R

def r_function(R: int, key: int, s_box: List[int], blocklength: int):
    R = R ^ key # xor the R and the key
    s_box_input = make_byte_array(R, blocklength//16)  # split up R into a byte array of length (blocklength//2)//8 so we can properly apply the S-box
    s_box_output = [s_box[byte] for byte in s_box_input]    # apply the S-box
    return s_box_output


def make_byte_array(num: int, length: int): # make a byte array out of the R-nod for the s-box
    mask = 2**8 - 1 # mask for 1 byte
    byte_array = [(num & (mask << (i*8))) >> (i*8) for i in range(length)]  # apply the mask for the i-th byte and shift it to the right again
    return byte_array

if __name__ == "__main__":
    main()