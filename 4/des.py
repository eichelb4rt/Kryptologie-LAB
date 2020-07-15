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
    if args.decrypt:
        generated_keys.reverse()
    # read s-box
    with open(args.s_box, "r") as f:
        s_box = [int(byte[1:-1], 16) for byte in f.read()[1:-2].split(", ")]   # strip [*] and the line break, then strip the single quotes from every single entry
    # now we can process each block on its own
    with open(args.input, "rb") as f_in, open(args.output, "wb") as f_out:
        while block := f_in.read(args.blocklength//8): # read the blocks
            block = int.from_bytes(block, 'big') << (args.blocklength - len(block)*8)   # pad the block if it's not full (fill the right side with 0) (len(block) is in bytes)
            output = encrypt_block(block, generated_keys, s_box, args.blocklength)  # encrypt the block
            f_out.write(output.to_bytes(args.blocklength//8, 'big'))    # write it in binary

def encrypt_block(block: int, keys: List[int], s_box: List[int], blocklength: int):
    L, R = split_key(block, blocklength)  # use the split_key function from key_gen: turns a (keylength) Integer into 2 (keylength//2) Integers.
    for i in range(16):
        L, R = encryption_step(L, R, keys[i], s_box, blocklength)
    L, R = R, L # swap em one last time
    return (L << blocklength//2) | R

def encryption_step(L: int, R: int, key: int, s_box: List[int], blocklength: int):
    next_L = R
    next_R = r_function(R, key, s_box, blocklength) ^ L
    return next_L, next_R

def r_function(R: int, key: int, s_box: List[int], blocklength: int):   # function that is applied to the right side of the block
    R = R ^ key # xor the R and the key
    s_box_input = make_byte_array(R, blocklength // 16)  # split up R into a byte array of length (blocklength//2)//8 so we can properly apply the S-box
    substituted_R = 0   # prepare it for logical or
    for i, byte in enumerate(s_box_input):
        #print(f'byte: {byte}\ts: {s_box[byte]}\trs: {invert_array(s_box)[s_box[byte]]}')
        substituted_R |= s_box[byte] << ((blocklength//16 - 1 - i) * 8)    # apply the s_box on every byte
    return substituted_R

def make_byte_array(num: int, length: int): # make a byte array out of the R-nod for the s-box
    byte_mask = 2**8 - 1 # mask for 1 byte
    byte_array = [(num >> (((length-1) - i)*8)) & byte_mask for i in range(length)]  # shitft the i-th byte (counted from the left) to the right and apply the mask
    return byte_array

if __name__ == "__main__":
    main()